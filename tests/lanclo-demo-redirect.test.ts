import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../workers/lanclo-demo-redirect.ts';
test('demo entrypoints permanently redirect with their query for GET and HEAD',async()=>{
 const env={DEMO_ASSETS:{async fetch(){throw Error('must not call asset service')}}};
 for(const path of ['/demos/lanclo-lp','/demos/lanclo-lp/','/demos/lanclo-lp/index.html'])for(const query of ['','?lang=ja','?lang=en&utm_source=demo'])for(const method of ['GET','HEAD']){
  const res=await worker.fetch(new Request('https://videos.maepace.com'+path+query,{method}),env);
  assert.equal(res.status,301);assert.equal(res.headers.get('Location'),'https://lanclo.app/lp/'+query);
 }
});
test('assets, unrelated paths and hosts preserve the original service response and Range',async()=>{
 for(const url of ['https://videos.maepace.com/demos/lanclo-lp/assets/model.wav','https://videos.maepace.com/demos/lanclo-lp-other','https://example.com/demos/lanclo-lp/']){
  const request=new Request(url,{headers:{Range:'bytes=0-99'}}),response=new Response('asset',{status:206});
  const env={DEMO_ASSETS:{async fetch(seen:Request){assert.equal(seen,request);assert.equal(seen.headers.get('Range'),'bytes=0-99');return response}}};
  assert.equal(await worker.fetch(request,env),response);
 }
});
