import {scoreColor} from '../simple/scoreColor.mjs';
import React from 'react';
import {dimensionKeys,validDimensions} from '../../shared/pronunciationDimensions.mjs';
import styles from './pronunciation.module.css';
export const lessonLabels={ja:{all:'すべて',sounds:'発音',stress:'アクセント',rhythm:'リズム',intonation:'抑揚',fluency:'流暢さ'},en:{all:'All',sounds:'Sounds',stress:'Stress',rhythm:'Rhythm',intonation:'Intonation',fluency:'Fluency'}};
export default function LessonRadar({dimensions,score,ui='en',showOverall=true,compact=false}){
 if(!validDimensions(dimensions))return null;
 const ja=ui==='ja',labels=lessonLabels[ja?'ja':'en'],point=(i,n)=>{const a=-Math.PI/2+i*2*Math.PI/5;return [160+Math.cos(a)*74*n/100,115+Math.sin(a)*74*n/100]};
 const color=score==null?'#0071e3':scoreColor(score);
 const polygon=n=>dimensionKeys.map((_,i)=>point(i,n).join(',')).join(' '),complete=dimensionKeys.every(key=>dimensions[key]!==null);
 return <div className={styles.lessonRadar} role="img" aria-label={`${showOverall?`${ja?'総合スコア':'Overall score'} ${score??'—'} / 100. `:''}${dimensionKeys.map(key=>`${labels[key]}: ${dimensions[key]??(ja?'未評価':'Not assessed')}`).join(', ')}`}><svg viewBox="0 -12 320 254" aria-hidden="true">
 {[25,50,75,100].map(n=><polygon key={n} points={polygon(n)} fill="none" stroke="#e0e5ec"/>)}
 {dimensionKeys.map((key,i)=>{const [x,y]=point(i,100),[lx,ly]=point(i,137);return <g key={key}><line x1="160" y1="115" x2={x} y2={y} stroke="#e0e5ec"/><text x={lx} y={ly-4} textAnchor="middle" fontSize={compact?16:14} fill="#1d1d1f">{labels[key]}</text><text x={lx} y={ly+12} textAnchor="middle" fontSize={compact?17:15} fontWeight="600" fill="#1d1d1f">{dimensions[key]??'—'}</text></g>})}
 {complete&&<polygon points={dimensionKeys.map((key,i)=>point(i,dimensions[key]).join(',')).join(' ')} fill={color} fillOpacity="0.1" stroke={color} strokeWidth="2"/>}
 {dimensionKeys.map((key,i)=>{if(dimensions[key]===null)return null;const [cx,cy]=point(i,dimensions[key]);return <circle key={key} cx={cx} cy={cy} r="3" fill={color}/>})}
 {showOverall&&<><text x="160" y="125" textAnchor="middle" fontSize="32" fontWeight="650" letterSpacing="-1" fill="#1d1d1f">{score??'—'}</text></>}
 </svg></div>;
}
