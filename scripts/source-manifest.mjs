import {readdir,readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const root=new URL('../projects/lanclo-lp/source/',import.meta.url);const files=[];
async function walk(dir,prefix=''){for(const item of (await readdir(dir,{withFileTypes:true})).sort((a,b)=>a.name.localeCompare(b.name))){if(['node_modules','dist'].includes(item.name))continue;const name=prefix+item.name,url=new URL(item.name+(item.isDirectory()?'/':''),dir);if(item.isDirectory())await walk(url,name+'/');else files.push({path:name,sha256:createHash('sha256').update(await readFile(url)).digest('hex')});}}
await walk(root);await writeFile(new URL('../projects/lanclo-lp/source-manifest.json',import.meta.url),JSON.stringify({algorithm:'sha256',files},null,2)+'\n');console.log(`Recorded ${files.length} source files.`);
