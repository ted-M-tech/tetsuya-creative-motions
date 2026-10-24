// The internal tools Gemini key (project lanclo-internal-tools) from ~/.config/lanclo/gemini-internal.env, with the same
// guards as ownvoice.py: GEMINI_PROJECT_ID must be lanclo-internal-tools; the file must be a regular 0600 file (no symlink),
// not the same file as another ~/.config/lanclo/*.env (hard link), and its key must not appear in any GEMINI*/MVT_GEMINI*
// value of another env file (production, legacy, renamed copies); no other file may declare the project as MVT_GOOGLE_PROJECT.
// Throws with a message that never contains a key. No fallback to gemini-dedicated.env (owner step O6 creates the file).
import {readFileSync,readdirSync,lstatSync,statSync,existsSync} from 'node:fs';
import {homedir} from 'node:os';
import {join} from 'node:path';
export const INTERNAL_PROJECT='lanclo-internal-tools';
const NAME='gemini-internal.env';
export function readEnv(path){
 const env={};
 for(const raw of readFileSync(path,'utf8').split('\n')){
  const l=raw.replace(/^\s*export\s+/,'').trim();if(!l||l.startsWith('#')||!l.includes('='))continue;
  const i=l.indexOf('=');env[l.slice(0,i).trim()]=l.slice(i+1).trim().replace(/^(['"])(.*)\1$/,'$2');
 }
 return env;
}
export function internalGeminiKey(home=homedir()){
 const dir=join(home,'.config/lanclo'),path=join(dir,NAME),fail=m=>{throw new Error(`internal-gemini-key: ${m}`)};
 let ls;try{ls=lstatSync(path)}catch{fail(`~/.config/lanclo/${NAME} is missing. The owner creates it for project ${INTERNAL_PROJECT} (Gemini capacity architecture, step O6) with GEMINI_API_KEY and GEMINI_PROJECT_ID=${INTERNAL_PROJECT}, mode 0600. There is no fallback to gemini-dedicated.env.`)}
 if(ls.isSymbolicLink()||!ls.isFile())fail(`~/.config/lanclo/${NAME} must be a regular file, not a symlink; refusing.`);
 if(ls.mode&0o077)fail(`~/.config/lanclo/${NAME} is readable by group/others (mode ${(ls.mode&0o777).toString(8)}); chmod 600 it.`);
 const env=readEnv(path),project=env.GEMINI_PROJECT_ID||'',key=env.GEMINI_API_KEY||'';
 if(project!==INTERNAL_PROJECT)fail(`GEMINI_PROJECT_ID in ~/.config/lanclo/${NAME} must be ${INTERNAL_PROJECT}; refusing.`);
 if(!key)fail(`GEMINI_API_KEY is not set in ~/.config/lanclo/${NAME}.`);
 for(const name of readdirSync(dir).filter(n=>n.endsWith('.env')&&n!==NAME).sort()){
  const other=join(dir,name);if(!existsSync(other))continue;
  const st=statSync(other);if(st.dev===ls.dev&&st.ino===ls.ino)fail(`~/.config/lanclo/${NAME} is the same file as ${name}; refusing.`);
  let o;try{o=readEnv(other)}catch{continue}
  if(Object.entries(o).some(([n,v])=>/^(GEMINI|MVT_GEMINI)/.test(n)&&v===key))fail(`the key in ~/.config/lanclo/${NAME} is also in ${name}; refusing.`);
  if(o.MVT_GOOGLE_PROJECT===project)fail(`${name} declares MVT_GOOGLE_PROJECT=${project} too; refusing.`);
 }
 return key;
}
