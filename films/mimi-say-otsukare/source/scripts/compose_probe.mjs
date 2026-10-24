// Calls Lanclo's real server compose handler (voice-web/cloudflare/vocabulary.ts, origin/main) with the internal tools Gemini key
// (lanclo-internal-tools, kits/mimi-short/scripts/internal-gemini-key.mjs; GEMINI_STATELESS_PROJECT is routing only).
// Never prints the key. usage: node compose.mjs <nvc worktree> <input> [runs]
import {internalGeminiKey} from '../../../../kits/mimi-short/scripts/internal-gemini-key.mjs';
const [repo, input, runs='1'] = process.argv.slice(2);
const key = internalGeminiKey();
const {vocabularyApi} = await import(repo+'/voice-web/cloudflare/vocabulary.ts');
const owner = {env:{GEMINI_STATELESS_PROJECT:'dedicated',GEMINI_DEDICATED_API_KEY:key},
  state:{storage:{get:async()=>undefined},waitUntil:()=>{}}};
for (let i=0;i<Number(runs);i++){
  const body = JSON.stringify({purpose:'compose',input,language:'en',meaningLocale:'ja',consent:true});
  const res = await vocabularyApi(owner,new Request('https://lanclo.local/api/daily/vocabulary',{method:'POST',body}));
  console.log(JSON.stringify({run:i+1,status:res.status,at:new Date().toISOString(),body:await res.json()}));
}
