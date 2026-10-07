import React from 'react';
const segmenter=new Intl.Segmenter('ja',{granularity:'word'});
// Keep Japanese words intact in engines without CSS auto-phrase support.
export default function ReadableText({children}){
 if(typeof children!=='string'||!/[ぁ-んァ-ヶ一-龠]/.test(children))return children;
 return [...segmenter.segment(children)].map(({segment,index,isWordLike})=>isWordLike?<span className="text-word" key={index}>{segment}</span>:segment);
}
