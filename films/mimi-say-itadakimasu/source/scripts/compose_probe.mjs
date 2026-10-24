// Calls Lanclo's real server vocabulary handler (voice-web/cloudflare/vocabulary.ts, origin/main) with the internal tools Gemini key
// (lanclo-internal-tools, kits/mimi-short/scripts/internal-gemini-key.mjs; GEMINI_STATELESS_PROJECT is routing only).
// Never prints the key. Prints only the {run} lines (the handler's own telemetry lines go to stdout too: filter with grep '"run"').
// usage: node compose_probe.mjs <nvc worktree> <input> [runs]                 -> purpose compose (what フレーズを作成 sends)
//        node compose_probe.mjs <nvc worktree> <term> [runs] <meaning>        -> purpose example (what the draft's example sends, ja translation)
import {internalGeminiKey} from '../../../../kits/mimi-short/scripts/internal-gemini-key.mjs';
const [repo, input, runs='1', meaning] = process.argv.slice(2);
const key = internalGeminiKey();
const {vocabularyApi} = await import(repo+'/voice-web/cloudflare/vocabulary.ts');
const owner = {env:{GEMINI_STATELESS_PROJECT:'dedicated',GEMINI_DEDICATED_API_KEY:key},
  state:{storage:{get:async()=>undefined},waitUntil:()=>{}}};
const req = meaning === undefined
  ? {purpose:'compose',input,language:'en',meaningLocale:'ja',consent:true}
  : {purpose:'example',term:input,meaning,language:'en',translationLocale:'ja',consent:true};
for (let i=0;i<Number(runs);i++){
  const res = await vocabularyApi(owner,new Request('https://lanclo.local/api/daily/vocabulary',{method:'POST',body:JSON.stringify(req)}));
  console.log(JSON.stringify({run:i+1,status:res.status,at:new Date().toISOString(),request:req,body:await res.json()}));
}
