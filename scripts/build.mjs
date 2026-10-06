import {cp, mkdir, rm, stat} from 'node:fs/promises';
import {resolve} from 'node:path';
const root = resolve(import.meta.dirname, '..');
const includeMedia = process.argv.includes('--include-media');
if (includeMedia) for (const id of ['lanclo','lanclo-osaka','lanclo-daily-r26']) await stat(`${root}/site/media/${id}.mp4`);
await rm(`${root}/dist`, {recursive:true,force:true});
await mkdir(`${root}/dist`, {recursive:true});
await cp(`${root}/site`, `${root}/dist`, {recursive:true,filter:path => includeMedia || !path.startsWith(`${root}/site/media`)});
console.log(includeMedia ? 'Built dist/ with finished MP4s.' : 'Built dist/ without MP4s. Add licensed media before publishing.');
