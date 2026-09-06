import {common} from '@/lib/community';
import {utility} from '@/lib/utility';
import {ApiError} from '@/lib/storage';
export async function handler(r:Request){let response:Response;try{const path=new URL(r.url).pathname.replace(/^\/api\/?/,'');response=await common(r,path)||await utility(r,path)||Response.json({error:'Unknown route or method'},{status:404});}catch(e){response=Response.json({error:e instanceof ApiError?e.message:'Service unavailable'},{status:e instanceof ApiError?e.status:503});}response.headers.set('Cache-Control','no-store');response.headers.set('Access-Control-Allow-Origin','*');response.headers.set('X-Content-Type-Options','nosniff');return response;}
export const GET=handler;export const POST=handler;
export function OPTIONS(){return new Response(null,{status:204,headers:{'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'Content-Type,Authorization,Idempotency-Key,X-Experiment-Cohort,X-Discovery-Source','Access-Control-Max-Age':'600'}});}
