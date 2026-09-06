import {body,metric,ApiError} from './storage';
import {resolveTime} from './time';
export async function utility(r:Request,path:string):Promise<Response|undefined>{if(r.method==='POST'&&path==='resolve'){const input=await body(r);let result;try{result=resolveTime(input);}catch(e){throw new ApiError(400,e instanceof Error?e.message:'Invalid input');}await metric(r,'utility_success');return Response.json(result);}}
