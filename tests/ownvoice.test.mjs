// ownvoice.py config guards (E10). Every case runs --dry-run against a temporary HOME: no provider call is ever made.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync,mkdirSync,writeFileSync,symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
const script=fileURLToPath(new URL('../kits/mimi-short/scripts/ownvoice.py',import.meta.url));
function setup({internal,dedicated,lines=1}={}){
 const home=mkdtempSync(join(tmpdir(),'ownvoice-')),cfg=join(home,'.config/lanclo');mkdirSync(cfg,{recursive:true});
 if(dedicated!==undefined)writeFileSync(join(cfg,'gemini-dedicated.env'),dedicated);
 if(internal==='symlink')symlinkSync(join(cfg,'gemini-dedicated.env'),join(cfg,'gemini-internal.env'));
 else if(internal!==undefined)writeFileSync(join(cfg,'gemini-internal.env'),internal);
 const spec=join(home,'own-voice.json');
 writeFileSync(spec,JSON.stringify({lines:Array.from({length:lines},(_,i)=>({id:`l${i}`,text:'Hello.'}))}));
 return {home,spec};
}
function run({home,spec},...args){
 const r=spawnSync('python3',[script,spec,'--dry-run',...args],{env:{...process.env,HOME:home},encoding:'utf8'});
 return {code:r.status,out:r.stdout+r.stderr};
}
const ok='GEMINI_API_KEY=test-internal\nGEMINI_PROJECT_ID=lanclo-internal-tools\n';
test('refuses without the internal env file, with no fallback to the production file',()=>{
 const r=run(setup({dedicated:'GEMINI_API_KEY=test-prod\n'}));
 assert.notEqual(r.code,0);assert.match(r.out,/gemini-internal\.env is missing.*O6/s);
});
test('refuses the production project id',()=>{
 const r=run(setup({internal:'GEMINI_API_KEY=test-internal\nGEMINI_PROJECT_ID=myvoicetutor-production-01\n'}));
 assert.notEqual(r.code,0);assert.match(r.out,/production project myvoicetutor-production-01; refusing/);
});
test('refuses a missing project id',()=>{
 const r=run(setup({internal:'GEMINI_API_KEY=test-internal\n'}));
 assert.notEqual(r.code,0);assert.match(r.out,/GEMINI_PROJECT_ID is not set/);
});
test('refuses an internal env file that is a symlink to the production key file',()=>{
 const r=run(setup({dedicated:ok,internal:'symlink'}));
 assert.notEqual(r.code,0);assert.match(r.out,/production key file gemini-dedicated\.env; refusing/);
});
test('refuses the production key copied into the internal file, without printing it',()=>{
 const r=run(setup({dedicated:'GEMINI_API_KEY=test-internal\n',internal:ok}));
 assert.notEqual(r.code,0);assert.match(r.out,/is the production key/);assert.doesNotMatch(r.out,/test-internal/);
});
test('refuses a plan over the 20-call default budget, allows it with an explicit --max-calls',()=>{
 const s=setup({internal:ok,lines:20});
 const r=run(s);assert.notEqual(r.code,0);assert.match(r.out,/21 planned calls exceed the budget of 20/);
 const r2=run(s,'--max-calls','21');assert.equal(r2.code,0,r2.out);assert.match(r2.out,/dry run, config valid/);
});
test('valid internal config passes the dry run and prints the planned call count',()=>{
 const r=run(setup({internal:ok,lines:2}),'--force','l0');
 assert.equal(r.code,0,r.out);assert.match(r.out,/project lanclo-internal-tools; 2 line\(s\).*= 3 planned provider call\(s\); budget 20/);
 assert.doesNotMatch(r.out,/test-internal/);
});
