// Keep the existing preference key/string wire shape; older single-topic values remain valid.
export const interestTopics=['ai','culture','technology','science','society','business','sports','world'];
export function newsInterests(value){return [...new Set((Array.isArray(value)?value:typeof value==='string'?value.split(','):[]).filter(topic=>interestTopics.includes(topic)))].slice(0,3)}
export function encodeNewsInterests(value){return newsInterests(value).sort().join(',')||'all'}
export function validNewsInterests(value){return typeof value==='string'&&(value==='all'||value.length>0&&value.split(',').length<=3&&value.split(',').every(topic=>interestTopics.includes(topic)))}
export function matchesNewsInterests(story,value){const selected=newsInterests(value);return !selected.length||selected.some(topic=>story.topics?.includes(topic))}
