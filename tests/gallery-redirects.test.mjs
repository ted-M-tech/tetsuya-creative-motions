import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../server/media.mjs';
test('legacy completed artifacts resolve into the shared MaePace gallery',async()=>{
 const env={ASSETS:{fetch(){throw new Error('Redirect must not read assets');}}};
 for(const [path,target] of [['/','/works'],['/works/lanclo-lp/','/works/lanclo-lp'],['/films/lanclo-daily/','/works/lanclo-film'],['/slides/lanclo-making/','/works/lanclo-lp']]){
  for(const prefix of ['', '/en']){const response=await worker.fetch(new Request('https://videos.maepace.com'+prefix+path),env);assert.equal(response.status,302);const url=new URL(response.headers.get('location'));assert.equal(url.origin,'https://maepace.com');assert.equal(url.pathname,target);assert.equal(url.searchParams.get('lang'),prefix?'en':'ja');}
 }
});
