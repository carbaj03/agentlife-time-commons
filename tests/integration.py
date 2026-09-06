import argparse, concurrent.futures, datetime as dt, json, uuid
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from pathlib import Path
from zoneinfo import ZoneInfo

p=argparse.ArgumentParser();p.add_argument('origin');p.add_argument('kind',choices=['fault-lab','time-commons']);p.add_argument('output');args=p.parse_args()
assert args.origin.startswith(('http://localhost:300','https://fault-lab.','https://time-commons.')),'Explicit pilot origin required'
checks=[]
def check(name,value):
 checks.append({'check':name,'passed':bool(value)})
 if not value:raise AssertionError(name)
def req(path,body=None,token=None,key=None,method=None):
 h={'User-Agent':'UtilityPilotValidation/1.0','X-Experiment-Cohort':'operator-tests'}
 if body is not None:h['Content-Type']='application/json'
 if token:h['Authorization']='Bearer '+token
 if key:h['Idempotency-Key']=key
 r=Request(args.origin+path,data=json.dumps(body).encode() if body is not None else None,headers=h,method=method)
 try:resp=urlopen(r,timeout=30)
 except HTTPError as e:resp=e
 raw=resp.read().decode()
 try:val=json.loads(raw)
 except ValueError:val=raw
 return resp.status,val,dict(resp.headers)

baseline=req('/api/stats')[1]
check('Health and storage',req('/api/health')[1]=={'status':'ok','storage':True})
for path in ['/','/protocol','/method','/cases','/observatory','/openapi.json','/robots.txt','/sitemap.xml','/llms.txt']:
 s,b,h=req(path);check('Accessible '+path,s==200)
 if path=='/robots.txt':check('Crawling allowed','Allow: /' in b)
 if path=='/openapi.json':check('Machine schema available',b.get('openapi')=='3.0.3')
cases=req('/api/cases')[1]['cases']
for c in cases:
 for prefix in ['/cases/','/guides/']:check(prefix+c['id'],req(prefix+c['id'])[0]==200)
check('Invalid case is 404',req('/cases/invalid')[0]==404)
check('Unknown API is 404',req('/api/unknown')[0]==404)
check('CORS preflight',req('/api/reports',method='OPTIONS')[0]==204)
check('Reject invalid registration',req('/api/actors',{'discovery':'fabricated'})[0]==400)
actors=[]
for _ in range(2):
 s,a,h=req('/api/actors',{'discovery':'operator-test'});check('Operator credential',s==201 and a['cohort']=='operator-tests');actors.append(a)
case=cases[0]['id'];b={'public':True,'case_id':case,'body':'Operator validation: synthetic fixture reproduced. This is a test, not independent participation.'};key=str(uuid.uuid4())
check('Publication needs credential',req('/api/reports',b,key=key)[0]==401)
check('Invalid credential rejected',req('/api/reports',b,token='invalid',key=key)[0]==401)
check('Publication needs explicit public consent',req('/api/reports',{**b,'public':False},actors[0]['token'],key)[0]==400)
check('Publication validates case',req('/api/reports',{**b,'case_id':'unknown'},actors[0]['token'],key)[0]==400)
check('Missing idempotency key rejected',req('/api/reports',b,actors[0]['token'])[0]==400)
check('Oversized body rejected',req('/api/reports',{**b,'body':'a'*5000},actors[0]['token'],key)[0]==413)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(lambda _:req('/api/reports',b,actors[0]['token'],key),range(3)))
check('Concurrent publication creates one record',len({r[1].get('id') for r in results})==1 and sum(r[0]==201 for r in results)==1)
report=results[0][1]['id'];check('Conflicting replay is 409',req('/api/reports',{**b,'body':'Different test content'},actors[0]['token'],key)[0]==409)
reply={**b,'body':'Operator validation reply from a second credential; same operator.','parent':report}
check('Reply from second credential',req('/api/reports',reply,actors[1]['token'],str(uuid.uuid4()))[0]==201)
check('Invalid parent rejected',req('/api/reports',{**reply,'parent':str(uuid.uuid4())},actors[1]['token'],str(uuid.uuid4()))[0]==400)
check('Operator reports excluded from public JSON',report not in json.dumps(req('/api/reports')[1]))
check('Operator reports excluded from case HTML',report not in str(req('/cases/'+case)[1]))

if args.kind=='fault-lab':
 check('Invalid scenario rejected',req('/api/runs',{'scenario':'invalid'})[0]==400)
 for scenario,expected in [('rate-limit',[429,429,200]),('transient',[503,200])]:
  s,r,h=req('/api/runs',{'scenario':scenario});check('Create '+scenario,s==201);observed=[]
  for target in expected:
   s,b,h=req(r['step_url']);observed.append(s);check('Scenario response '+str(target),s==target and b['synthetic'])
   if s!=200:check('Retry-After seconds',h.get('retry-after',h.get('Retry-After'))=='1')
  check('Expected sequence '+scenario,observed==expected)
 r=req('/api/runs',{'scenario':'rate-limit'})[1]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rs=list(ex.map(lambda _:req(r['step_url']),range(4)))
 check('Concurrent steps are atomic',sorted(x[1]['attempt'] for x in rs)==[1,2,3,4] and sorted(x[0] for x in rs)==[200,200,429,429])
 r=req('/api/runs',{'scenario':'pagination'})[1];a=req(r['step_url'])[1];b=req(a['next_url'])[1]
 check('Pagination complete without duplicates',[x['id'] for x in a['records']+b['records']]==['alpha','beta','gamma'] and b['next_url'] is None)
 check('Pagination stable on repeated reads',req(r['step_url'])[1]==a)
 check('Unknown cursor rejected',req(r['step_url']+'?cursor=invalid')[0]==400)
 check('Unknown run rejected',req('/api/runs/'+str(uuid.uuid4())+'/step')[0]==404)
else:
 fixtures=[('2026-11-01T01:30','America/New_York'),('2026-03-29T02:30','Europe/Madrid'),('2026-04-05T01:45','Australia/Lord_Howe'),('2026-10-04T02:15','Australia/Lord_Howe'),('2026-09-06T09:15','Asia/Kathmandu'),('2011-12-30T12:00','Pacific/Apia'),('2024-02-29T12:00','UTC'),('2026-10-25T02:30','Europe/Madrid'),('2026-03-08T02:30','America/New_York'),('2026-01-01T00:00','Pacific/Kiritimati'),('2000-01-01T00:00','America/St_Johns'),('2035-12-31T23:59','Asia/Tokyo')]
 for local,zone in fixtures:
  naive=dt.datetime.fromisoformat(local);tz=ZoneInfo(zone);expected=set()
  for fold in [0,1]:
   utc=naive.replace(tzinfo=tz,fold=fold).astimezone(dt.timezone.utc)
   if utc.astimezone(tz).replace(tzinfo=None)==naive:expected.add(utc.isoformat(timespec='milliseconds').replace('+00:00','Z'))
  s,b,h=req('/api/resolve',{'local':local,'zone':zone,'compare':['Europe/Madrid','Asia/Tokyo']})
  check('zoneinfo agreement: '+zone+' '+local,s==200 and {x['utc'] for x in b['candidates']}==expected)
  check('Ambiguity classification',b['status']==('nonexistent' if len(expected)==0 else 'unique' if len(expected)==1 else 'ambiguous'))
  for c in b['candidates']:
   instant=dt.datetime.fromisoformat(c['utc'].replace('Z','+00:00'))
   check('Comparison-zone conversion',all(t['local']==instant.astimezone(ZoneInfo(t['zone'])).replace(tzinfo=None).isoformat(timespec='seconds') for t in c['compare']))
 for b in [{'local':'2026-02-30T12:00','zone':'UTC'},{'local':'2036-01-01T00:00','zone':'UTC'},{'local':'2026-09-06T24:00','zone':'UTC'},{'local':'2026-09-06T10:00','zone':'EST'},{'local':'2026-09-06T10:00','zone':'Invalid/Zone'},{'local':'2026-09-06T10:00','zone':'UTC','compare':['UTC']*7},{'local':'2026-09-06T10:00','zone':'UTC','compare':'UTC'}]:check('Invalid time input rejected',req('/api/resolve',b)[0]==400)

after=req('/api/stats')[1]
check('Validation leaves unattributed actor/report counts unchanged',[x for x in baseline['records'] if x['cohort']=='unattributed']==[x for x in after['records'] if x['cohort']=='unattributed'])
check('No claim of verified autonomy',after['confirmed_independent_agents'] is None)
out={'as_of':dt.datetime.now(dt.timezone.utc).isoformat(),'origin':args.origin,'kind':args.kind,'cohort':'operator-tests','checks':checks,'passed':sum(x['passed'] for x in checks),'stats_after':after}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'origin':args.origin,'passed':len(checks),'failed':0}))
