export const dimensionKeys=['sounds','stress','rhythm','intonation','fluency'];
export const dimensionLabels={ja:{sounds:'音の明瞭さ',stress:'アクセント',rhythm:'リズム',intonation:'イントネーション',fluency:'流暢さ'},en:{sounds:'Sounds',stress:'Word stress',rhythm:'Rhythm',intonation:'Intonation',fluency:'Fluency'}};
export function validDimensions(value){return !!value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).length===dimensionKeys.length&&dimensionKeys.every(key=>value[key]===null||Number.isInteger(value[key])&&value[key]>=0&&value[key]<=100);}
// Comparisons never combine models/configurations, legacy scores, or repeated rechecks.
export function dimensionSummary(attempts,evaluations,{ids,language='en',since=0,lessonId}={}){
 const allowed=new Set(attempts.filter(a=>a.language===language&&a.recordedAt>=since&&(!lessonId||a.conditions?.lessonId===lessonId)&&(!ids||ids.includes(a.contentId))).map(a=>a.id));
 const latest=new Map();
 for(const e of evaluations){if(!allowed.has(e.attemptId))continue;const old=latest.get(e.attemptId);if(!old||(e.requestedAt??e.evaluatedAt)>(old.requestedAt??old.evaluatedAt))latest.set(e.attemptId,e);}
 const rows=[...latest.values()].filter(e=>e.result?.status==='scored'&&validDimensions(e.result.dimensions)).sort((a,b)=>b.evaluatedAt-a.evaluatedAt);
 if(!rows.length)return null;
 const reference=rows[0],same=rows.filter(e=>e.model===reference.model&&e.rubric===reference.rubric&&e.assessmentConfigId===reference.assessmentConfigId).slice(0,20);
 return {count:same.length,dimensions:Object.fromEntries(dimensionKeys.map(key=>{const values=same.map(e=>e.result.dimensions[key]).filter(v=>v!==null);return [key,values.length?Math.round(values.reduce((a,b)=>a+b,0)/values.length):null]}))};
}

export function validCategoryFeedback(value){return !!value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).length===dimensionKeys.length&&dimensionKeys.every(key=>value[key]===null||typeof value[key]==='string'&&value[key].trim().length>0&&value[key].length<=260);}
