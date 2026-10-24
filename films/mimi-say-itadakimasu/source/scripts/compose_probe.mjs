// Calls Lanclo's real server vocabulary handler (voice-web/cloudflare/vocabulary.ts, origin/main) with the dedicated Gemini key.
// Never prints the key. Prints only the {run} lines (the handler's own telemetry lines go to stdout too: filter with grep '"run"').
// usage: node compose_probe.mjs <nvc worktree> <input> [runs]                 -> purpose compose (what フレーズを作成 sends)
//        node compose_probe.mjs <nvc worktree> <term> [runs] <meaning>        -> purpose example (what the draft's example sends, ja translation)
import {readFileSync} from 'node:fs';
import {homedir} from 'node:os';
const [repo, input, runs='1', meaning] = process.argv.slice(2);
const env = Object.fromEntries(readFileSync(homedir()+'/.config/lanclo/gemini-dedicated.env','utf8').split('\n')
  .map(l=>l.replace(/^export\s+/,'').trim()).filter(l=>l.includes('=')&&!l.startsWith('#'))
  .map(l=>{const i=l.indexOf('=');return [l.slice(0,i),l.slice(i+1).replace(/^['"]|['"]$/g,'')]}));
const {vocabularyApi} = await import(repo+'/voice-web/cloudflare/vocabulary.ts');
const owner = {env:{GEMINI_STATELESS_PROJECT:'dedicated',GEMINI_DEDICATED_API_KEY:env.GEMINI_API_KEY},
  state:{storage:{get:async()=>undefined},waitUntil:()=>{}}};
const req = meaning === undefined
  ? {purpose:'compose',input,language:'en',meaningLocale:'ja',consent:true}
  : {purpose:'example',term:input,meaning,language:'en',translationLocale:'ja',consent:true};
for (let i=0;i<Number(runs);i++){
  const res = await vocabularyApi(owner,new Request('https://lanclo.local/api/daily/vocabulary',{method:'POST',body:JSON.stringify(req)}));
  console.log(JSON.stringify({run:i+1,status:res.status,at:new Date().toISOString(),request:req,body:await res.json()}));
}
