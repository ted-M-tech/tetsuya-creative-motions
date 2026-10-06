import {test} from 'node:test';
import assert from 'node:assert/strict';
import worker from '../server/media.mjs';
const content='0123456789';
async function fetchMedia(range, extra={}, method='GET') {
  return worker.fetch(new Request('https://example.test/media/film.mp4', {method,headers:{...(range?{range}:{}),...extra}}), {
    ASSETS:{fetch: async request => { assert.equal(request.headers.has('range'),false); return new Response(method==='HEAD'?null:content,{headers:{'content-type':'video/mp4','content-length':'10',etag:'"film-v1"'}}); }},
  });
}
test('closed, open and suffix ranges return exact bytes',async()=>{
  for(const [range,body,contentRange] of [['bytes=2-4','234','bytes 2-4/10'],['bytes=8-','89','bytes 8-9/10'],['bytes=-3','789','bytes 7-9/10'],['bytes=8-99','89','bytes 8-9/10']]){
    const r=await fetchMedia(range);assert.equal(r.status,206);assert.equal(await r.text(),body);assert.equal(r.headers.get('content-range'),contentRange);assert.equal(r.headers.get('content-length'),String(body.length));
  }
});
test('unsatisfiable ranges have 416 and size',async()=>{
 for(const range of ['bytes=10-','bytes=9-2','bytes=-0','bytes=-']){const r=await fetchMedia(range);assert.equal(r.status,416);assert.equal(r.headers.get('content-range'),'bytes */10');}
});
test('HEAD, full response and stale If-Range are not sliced',async()=>{
 for(const [range,extra,method] of [[null,{},'GET'],['bytes=2-4',{'if-range':'"old"'},'GET'],['bytes=2-4',{},'HEAD']]){const r=await fetchMedia(range,extra,method);assert.equal(r.status,200);assert.equal(r.headers.get('accept-ranges'),'bytes');assert.equal(await r.text(),method==='HEAD'?'':content);}
});

test('asset bindings without a Content-Length still support seeking',async()=>{
 const r=await worker.fetch(new Request('https://example.test/media/film.mp4',{headers:{range:'bytes=2-4'}}),{ASSETS:{fetch:async()=>new Response(content)}});
 assert.equal(r.status,206);assert.equal(await r.text(),'234');assert.equal(r.headers.get('content-range'),'bytes 2-4/10');
});
