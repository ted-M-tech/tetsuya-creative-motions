import {cp, mkdir, rm, stat, readdir} from 'node:fs/promises';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
const root = resolve(import.meta.dirname, '..');
const includeMedia = process.argv.includes('--include-media');
if (includeMedia) for (const id of ['lanclo','lanclo-osaka','lanclo-daily-r26']) await stat(`${root}/site/media/${id}.mp4`);
if (includeMedia) for (const file of await readdir(`${root}/site/media`)) {
 const info=await stat(`${root}/site/media/${file}`);
 if(info.isFile() && info.size>25*1024*1024) throw new Error(`Static asset exceeds 25 MiB: ${file}`);
}
await rm(`${root}/dist`, {recursive:true,force:true});
await mkdir(`${root}/dist`, {recursive:true});
await cp(`${root}/site`, `${root}/dist`, {recursive:true,filter:path => includeMedia || !path.startsWith(`${root}/site/media`)});
console.log(includeMedia ? 'Built dist/ with finished MP4s.' : 'Built dist/ without MP4s. Add licensed media before publishing.');

execFileSync('npm',['run','build'],{cwd:resolve(root,'projects/lanclo-lp/source'),stdio:'inherit',env:{...process.env,LP_BASE:'/demos/lanclo-lp/'}});
await cp(resolve(root,'projects/lanclo-lp/source/dist'),resolve(root,'dist/demos/lanclo-lp'),{recursive:true});
