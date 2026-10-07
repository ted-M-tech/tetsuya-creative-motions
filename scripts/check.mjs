import {execFileSync} from 'node:child_process';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {dirname,resolve,extname} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const files=execFileSync('git',['ls-files','--cached','--others','--exclude-standard','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean);
const errors=[];
for(const file of files){
 const path=resolve(root,file);if(!existsSync(path)||!statSync(path).isFile())continue;
 if(/\.(mp4|wav|mp3|m4a)$/.test(file))errors.push(`Media should be ignored: ${file}`);
 if(!['.md','.json','.html','.js','.mjs','.py','.css','.jsx','.ts'].includes(extname(file)))continue;
 const text=readFileSync(path,'utf8');
 for(const pattern of [new RegExp('/'+'Users/'),new RegExp('voice_'+'[a-z0-9]{10,}'),new RegExp('AIza'+'[A-Za-z0-9_-]{30,}')])if(pattern.test(text))errors.push(`Private value/path in ${file}`);
 if(file.endsWith('.md'))for(const match of text.matchAll(/\]\(([^)]+)\)/g)){
  const link=match[1].split('#')[0];if(!link||/^(https?:|mailto:)/.test(link))continue;
  if(!existsSync(resolve(dirname(path),decodeURIComponent(link))))errors.push(`Broken link ${file}: ${link}`);
 }
}
for(const item of JSON.parse(readFileSync(resolve(root,'films/catalog.json'),'utf8')).flatMap(item=>[item,...(item.extras||[]),...(item.history||[])])){
 for(const file of ['README.md','PROMPT.md','NARRATION.md','CREDITS.md','TIMING.json','TTS-PROMPTS.json','source/index.html'])if(!existsSync(resolve(root,'films',item.path||item.id,file)))errors.push(`${item.id}: missing ${file}`);
 if(!existsSync(resolve(root,'site/posters',item.poster||item.id+'.jpg')))errors.push(`${item.id}: missing poster`);
}
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log(`Checked ${files.length} public files: links, film records and private-data exclusions passed.`);
