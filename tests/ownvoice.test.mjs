// Config guards for the internal tools Gemini project (E10): ownvoice.py and the JS helper used by the compose probes.
// Every case uses a temporary HOME. No case reaches the provider: dry runs make no call, real runs are refused before any
// call (HTTPS_PROXY points at a closed port, so a call would fail rather than leave the machine), and the budget test
// stubs urlopen.
import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync,mkdirSync,writeFileSync,symlinkSync,linkSync,chmodSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {internalGeminiKey} from '../kits/mimi-short/scripts/internal-gemini-key.mjs';
const script=fileURLToPath(new URL('../kits/mimi-short/scripts/ownvoice.py',import.meta.url));
const homes=[];after(()=>{for(const h of homes)rmSync(h,{recursive:true,force:true})});
const OK='GEMINI_API_KEY=test-internal\nGEMINI_PROJECT_ID=lanclo-internal-tools\n';
const PROD='GEMINI_API_KEY=test-prod\n';
// files: {name: text}; internal: text | 'symlink' | 'hardlink' (both to gemini-dedicated.env) | 'none'; mode of the internal file
function setup({internal=OK,files={'gemini-dedicated.env':PROD},mode=0o600,lines=1}={}){
 const home=mkdtempSync(join(tmpdir(),'ownvoice-'));homes.push(home);
 const cfg=join(home,'.config/lanclo');mkdirSync(cfg,{recursive:true});
 for(const [n,t] of Object.entries(files)){writeFileSync(join(cfg,n),t);chmodSync(join(cfg,n),0o600);}
 const path=join(cfg,'gemini-internal.env');
 if(internal==='symlink')symlinkSync(join(cfg,'gemini-dedicated.env'),path);
 else if(internal==='hardlink')linkSync(join(cfg,'gemini-dedicated.env'),path);
 else if(internal!=='none'){writeFileSync(path,internal);chmodSync(path,mode);}
 const spec=join(home,'source/own-voice.json');mkdirSync(join(home,'source'));
 writeFileSync(spec,JSON.stringify({lines:Array.from({length:lines},(_,i)=>({id:`l${i}`,text:'Hello.'}))}));
 return {home,spec};
}
function run({home,spec},...args){
 const r=spawnSync('python3',[script,spec,...args],{env:{...process.env,HOME:home,HTTPS_PROXY:'http://127.0.0.1:9',https_proxy:'http://127.0.0.1:9'},encoding:'utf8'});
 return {code:r.status,out:r.stdout+r.stderr};
}
function js({home}){try{return {key:internalGeminiKey(home)}}catch(e){return {error:e.message}}}
// [name, setup options, expected refusal]; each case runs on ownvoice.py (dry run and real run) and on the JS helper.
const refusals=[
 ['missing internal file, no fallback to the production file',{internal:'none'},/gemini-internal\.env is missing.*O6.*no fallback/s],
 ['production project id',{internal:'GEMINI_API_KEY=test-internal\nGEMINI_PROJECT_ID=myvoicetutor-production-01\n'},/must be lanclo-internal-tools/],
 ['typo in the project id',{internal:'GEMINI_API_KEY=test-internal\nGEMINI_PROJECT_ID=lanclo-internal-tool\n'},/must be lanclo-internal-tools/],
 ['missing project id',{internal:'GEMINI_API_KEY=test-internal\n'},/must be lanclo-internal-tools/],
 ['symlink to the production file',{internal:'symlink',files:{'gemini-dedicated.env':OK}},/regular file, not a symlink/],
 ['hard link of the production file',{internal:'hardlink',files:{'gemini-dedicated.env':OK}},/same file as gemini-dedicated\.env/],
 ['group/other readable file',{mode:0o644},/readable by group\/others \(mode 644\)/],
 ['production key copied in',{files:{'gemini-dedicated.env':'GEMINI_API_KEY=test-internal\n'}},/also in gemini-dedicated\.env/],
 ['key in a renamed production file under another variable name, original absent',{files:{'gemini-prod-2026.env':'export MVT_GEMINI_API_KEY="test-internal"\n'}},/also in gemini-prod-2026\.env/],
 ['key in the legacy gemini.env',{files:{'gemini.env':'GEMINI_LEGACY_KEY=test-internal\n'}},/also in gemini\.env/],
 ['project declared by another file',{files:{'seed.env':'MVT_GOOGLE_PROJECT=lanclo-internal-tools\n'}},/seed\.env declares MVT_GOOGLE_PROJECT/],
];
for(const [name,opts,re] of refusals){
 test(`refuses: ${name}`,()=>{
  const s=setup(opts);
  for(const args of [['--dry-run'],[]]){
   const r=run(s,...args);assert.notEqual(r.code,0,r.out);assert.match(r.out,re);assert.doesNotMatch(r.out,/test-internal|test-prod/);
  }
  assert.ok(!existsSync(join(s.home,'source/assets')),'nothing generated');
  const j=js(s);assert.equal(j.key,undefined);assert.match(j.error,re);assert.doesNotMatch(j.error,/test-internal|test-prod/);
 });
}
test('refuses an unparsable internal file cleanly (no traceback)',()=>{
 const r=run(setup({internal:OK+'GEMINI_NOTE="unbalanced\n'}),'--dry-run');
 assert.equal(r.code,1);assert.match(r.out,/line 3 .* cannot be parsed/);assert.doesNotMatch(r.out,/Traceback/);
});
test('valid internal config: dry run prints the plan, JS helper returns the key; production file absent is fine',()=>{
 for(const files of [{'gemini-dedicated.env':PROD},{}]){
  const s=setup({files,lines:2});
  const r=run(s,'--dry-run','--force','l0');
  assert.equal(r.code,0,r.out);assert.match(r.out,/project lanclo-internal-tools; 2 line\(s\).*= 3 planned provider call\(s\); budget 20/);
  assert.doesNotMatch(r.out,/test-internal/);assert.equal(js(s).key,'test-internal');
 }
});
test('refuses a plan over the 20-call default budget before any call; an explicit --max-calls allows it',()=>{
 const s=setup({lines:20});
 for(const args of [['--dry-run'],[]]){const r=run(s,...args);assert.equal(r.code,1,r.out);assert.match(r.out,/21 planned calls exceed the budget of 20/);}
 assert.ok(!existsSync(join(s.home,'source/assets')));
 const r=run(s,'--dry-run','--max-calls','21');assert.equal(r.code,0,r.out);assert.match(r.out,/dry run, config valid/);
});
test('runtime budget stops a paginated voice list before the call past the cap (stubbed urlopen)',()=>{
 const py=`
import importlib.util, io, json, sys, urllib.request
spec = importlib.util.spec_from_file_location('ownvoice', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
calls = []
class R(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): pass
def fake(req, timeout=None):
    calls.append(req.full_url); return R(json.dumps({'voices': [], 'next_page_token': f'p{len(calls)}'}).encode())
urllib.request.urlopen = fake
try:
    m.voice_id({}, m.Budget(3))
except SystemExit as e:
    print(e.code); print('calls', len(calls))
`;
 const r=spawnSync('python3',['-c',py,script],{encoding:'utf8'});
 assert.equal(r.status,0,r.stderr);assert.match(r.stdout,/call budget of 3 reached/);assert.match(r.stdout,/calls 3\n/);
});
