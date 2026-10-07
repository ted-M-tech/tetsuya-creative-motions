import React,{useEffect,useRef,useState} from 'react';
import {interestTopics} from '../../shared/newsInterests.mjs';
import technology from './assets/photos/technology.jpg';
import world from './assets/photos/travel.jpg';
import culture from './assets/photos/culture.jpg';
import science from './assets/photos/science.jpg';
import ai from './assets/photos/ai.jpg';
import society from './assets/photos/society.jpg';
import business from './assets/photos/business.jpg';
import sports from './assets/photos/sports.jpg';
const photos={ai,culture,technology,science,society,business,sports,world};
const titles={ja:['AIニュース','カルチャー','テクノロジー','サイエンス','社会','ビジネス','スポーツ','世界'],en:['AI','Culture','Technology','Science','Society','Business','Sports','World'],ko:['AI 뉴스','문화','테크놀로지','과학','사회','비즈니스','스포츠','세계']};
const labels={ja:'興味から広がるニュース',en:'News inspired by your interests',ko:'관심사로 만나는 뉴스'};
const notes={ja:'ジャンルのイメージ写真 · Pexels',en:'Genre photographs · Pexels',ko:'장르별 이미지 사진 · Pexels'};
// Two identical sets keep the shelf seamless; repeated items are hidden from assistive technology.
export default function NewsCarousel({lang}){
 const ref=useRef(null),[running,setRunning]=useState(false);
 useEffect(()=>{let visible=false;const sync=()=>setRunning(visible&&!document.hidden);const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;sync()});observer.observe(ref.current);document.addEventListener('visibilitychange',sync);return()=>{observer.disconnect();document.removeEventListener('visibilitychange',sync)}},[]);
 return <div ref={ref} className="news-carousel" data-running={running} role="region" aria-label={labels[lang]}>
  <div className="news-carousel-window" tabIndex={0} aria-label={labels[lang]}>
   <div className="news-carousel-track">{[0,1].map(copy=><div className="news-carousel-set" key={copy} aria-hidden={copy===1?true:undefined}>{interestTopics.map((topic,index)=><article className="news-genre" key={topic} data-topic={topic}>
    <div className="news-genre-art" style={{backgroundImage:`url(${photos[topic]})`,backgroundPosition:topic==='ai'?'center 65%':topic==='world'?'center 35%':topic==='culture'?'center 20%':'center'}} aria-hidden="true"/>
    <div className="news-genre-copy"><span lang="en">{topic.toUpperCase()}</span><h3>{titles[lang][index]}</h3></div>
   </article>)}</div>)}</div>
  </div>
  <div className="news-carousel-caption wrap"><p>{notes[lang]}</p></div>
 </div>;
}
