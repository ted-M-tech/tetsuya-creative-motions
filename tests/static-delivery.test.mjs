import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
test('delivery has no billable Worker entrypoint or worker-first routing',()=>{
 const config=JSON.parse(readFileSync(new URL('../wrangler.jsonc',import.meta.url)));
 assert.equal(config.main,undefined);
 assert.equal(config.assets.run_worker_first,undefined);
 assert.equal(config.assets.binding,undefined);
});
test('legacy links retain language and section via static redirects',()=>{
 const rules=new Map(readFileSync(new URL('../site/_redirects',import.meta.url),'utf8').split('\n').filter(x=>x&&!x.startsWith('#')).map(x=>{const [from,to,status]=x.split(/\s+/);assert.equal(status,'302');return [from,to]}));
 for(const [path,target] of [['/','/works'],['/works/lanclo-lp/','/works/lanclo-lp'],['/films/lanclo-daily/','/works/lanclo-film'],['/slides/lanclo-making/','/works/lanclo-lp']])for(const prefix of ['', '/en']){const url=new URL(rules.get(prefix+path));assert.equal(url.origin,'https://maepace.com');assert.equal(url.pathname,target);assert.equal(url.searchParams.get('lang'),prefix?'en':'ja');if(path.startsWith('/slides/'))assert.equal(url.hash,'#making');}
});
