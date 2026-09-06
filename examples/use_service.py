import argparse,json,time
from urllib.request import Request,urlopen
from urllib.error import HTTPError
p=argparse.ArgumentParser();p.add_argument('--operator-test',action='store_true');args=p.parse_args()
origin='https://time-commons.carbaj0.chatgpt.site'
headers={'Content-Type':'application/json','User-Agent':'PublicUtilityExample/1.0','X-Discovery-Source':'public-repository'}
if args.operator_test:headers['X-Experiment-Cohort']='operator-tests'
def request(path,body=None):
 req=Request(origin+path,headers=headers,data=json.dumps(body).encode() if body is not None else None)
 try:r=urlopen(req,timeout=20)
 except HTTPError as e:r=e
 return r.status,json.loads(r.read()),r.headers
status,result,_=request('/api/resolve',{'local':'2026-11-01T01:30','zone':'America/New_York','compare':['Europe/Madrid','Asia/Tokyo']})
if status!=200:raise RuntimeError(result)
print(json.dumps(result,indent=2))
