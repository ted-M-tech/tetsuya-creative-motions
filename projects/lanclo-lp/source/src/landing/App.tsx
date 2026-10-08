import React, {useEffect, useState, type PropsWithChildren} from 'react';
type Language = 'ja' | 'en' | 'ko';
import {motion, useReducedMotion} from 'motion/react';
import {ArrowUpRightIcon as ArrowUpRight, PlusIcon as Plus} from '@phosphor-icons/react';
import Brand from '../Brand.jsx';
import Select from '../ui/Select.jsx';
import {copy} from './copy.js';
import {narrative} from './narrative.js';
import {LessonExperience,NewsExperience} from './Experience.jsx';
import {FilmHero, VoiceStory, FilmClosing} from './FilmStory.jsx';
import PremiumDevices from './PremiumDevices.jsx';
import ResearchEvidence from './ResearchEvidence.jsx';
import Comparison from './Comparison.jsx';

import './styles.css';
import './premium.css';
import './film-story.css';
import './taste.css';
import ImpeccableHero from './ImpeccableHero.jsx';
import VoiceMechanism from './VoiceMechanism.jsx';
import HabitStory from './HabitStory.jsx';
import ShadowingProblem from './ShadowingProblem.jsx';
import Pricing from './Pricing.jsx';
import DeveloperVoices from './DeveloperVoices';
import './impeccable.css';
import './palette.css';

const referenceSummaries={ja:['77研究・2,573人を統合。特定の音やリズムに焦点を当てた発音指導で、改善が報告されました。','15の実験・準実験を統合。音声認識を使った発音練習の効果を調べた研究です。','別の音声クローンツールを使った21人・8週間の研究。練習後の流暢さと理解しやすさの改善を報告しています。'],en:['77 studies and 2,573 learners. Pronunciation instruction targeting particular sounds and rhythm showed improvement.','A synthesis of 15 experimental and quasi-experimental studies of speech-recognition pronunciation practice.','21 learners over eight weeks using a different voice-cloning tool. Improvements in fluency and comprehensibility were reported after practice.'],ko:['77개 연구·2,573명을 통합. 특정 소리와 리듬에 집중한 발음 지도에서 개선이 보고됐습니다.','음성 인식 발음 연습을 다룬 15개 실험·준실험 연구를 통합했습니다.','다른 음성 복제 도구를 사용한 21명·8주 연구. 연습 후 유창성과 이해 용이성의 개선을 보고했습니다.']};
const ids=['voice','lessons','news','research'];
function Reveal({children, className=''}: PropsWithChildren<{className?: string}>) {
 const reduce=useReducedMotion();
 return <motion.div className={className} initial={reduce?false:{opacity:0,y:24}} animate={reduce?{opacity:1,y:0}:undefined} whileInView={{opacity:1,y:0}} viewport={{once:true,amount:.12}} transition={{duration:reduce?0:.55,ease:[.2,.7,.2,1]}}>{children}</motion.div>;
}
export default function App(){
 const [lang,setLang]=useState<Language>('ja');
 const [impeccable,setImpeccable]=useState(true);
 useEffect(()=>{const params=new URLSearchParams(location.search);const value=params.get('lang');if(value==='ja'||value==='en'||value==='ko')setLang(value);setImpeccable(params.get('design')!=='taste');},[]);
 const t=copy[lang],n=narrative[lang];
 useEffect(()=>{document.documentElement.dataset.lpDesign=impeccable?'impeccable':'taste';return()=>{delete document.documentElement.dataset.lpDesign;};},[impeccable]);
 useEffect(()=>{document.documentElement.lang=lang;document.title=`Lanclo — ${n.heroTitle}`;document.querySelector('meta[name="description"]')?.setAttribute('content',n.heroIntro);},[lang,n]);
 useEffect(()=>{
  if(!impeccable)return;
  const media=window.matchMedia('(prefers-reduced-motion: reduce)');
  const animations=new Set<Animation>();
  const observer=new IntersectionObserver(entries=>{for(const entry of entries){
   if(!entry.isIntersecting)continue;
   observer.unobserve(entry.target);
   if(media.matches)continue;
   const parts=[...entry.target.children];
   parts.forEach((part,index)=>{
    const animation=part.animate([{opacity:0,transform:'translateY(44px)'},{opacity:1,transform:'translateY(0)'}],{duration:950,delay:Math.min(index*100,200),easing:'cubic-bezier(.22,.65,.25,1)',fill:'backwards'});
    animations.add(animation);animation.onfinish=()=>animations.delete(animation);
   });
  }}, {threshold:0,rootMargin:'0px 0px -16% 0px'});
  document.querySelectorAll('#main > section:not(.im-hero), #main > .wrap').forEach(el=>observer.observe(el));
  const stop=()=>{if(media.matches)for(const animation of animations)animation.cancel();};media.addEventListener('change',stop);
  return()=>{observer.disconnect();media.removeEventListener('change',stop);for(const animation of animations)animation.cancel();};
 },[impeccable,lang]);
 function changeLanguage(value: string){if(value!=='ja'&&value!=='en'&&value!=='ko')return;setLang(value);const url=new URL(location.href);url.searchParams.set('lang',value);history.replaceState(null,'',url);}
 return <><a className="skip" href="#main">{lang==='ja'?'本文へ':lang==='ko'?'본문으로':'Skip to content'}</a>
 <header className="header"><a className="brand-link" href="#" aria-label="Lanclo"><Brand/></a><nav aria-label="Main">{ids.map((id,i)=><a key={id} href={`#${id}`}>{t.nav[i]}</a>)}<a href="#pricing">{{ja:"料金",en:"Pricing",ko:"요금"}[lang]}</a></nav><div className="header-tools"><label className="sr-only" htmlFor="language">Language</label><Select ref={undefined} variant="quiet" id="language" value={lang} onChange={(e: React.ChangeEvent<HTMLSelectElement>)=>changeLanguage(e.target.value)}><option value="ja">日本語</option><option value="en">English</option><option value="ko">한국어</option></Select><a className="return-link" href="https://voice.maepace.com/practice">{t.login}<ArrowUpRight size={16}/></a></div></header>
 <main id="main">
 {impeccable?<ImpeccableHero lang={lang} cta={t.cta}/>:<FilmHero lang={lang} cta={t.cta}/>}
 {impeccable&&<ShadowingProblem lang={lang}/>}
 {impeccable?<VoiceMechanism lang={lang}/>:<VoiceStory lang={lang}/>}
 <LessonExperience lang={lang} compact={impeccable}/>{impeccable&&<HabitStory lang={lang}/>}<NewsExperience lang={lang}/><PremiumDevices lang={lang}/>
 <section id="research" className="section wrap"><Reveal className="section-heading"><h2>{impeccable?(lang==='ja'?'自分の声を、お手本に。':lang==='ko'?'내 목소리를 발음의 모델로.':'Your voice. Your model.'):n.researchTitle}</h2>{!impeccable&&<p>{t.researchIntro}</p>}</Reveal><ResearchEvidence lang={lang} compact={impeccable}/><details className="further"><summary>{impeccable?({ja:"参考にした研究",en:"Research references",ko:"참고 연구"}[lang]):t.moreResearch}<Plus size={22}/></summary><div>{(impeccable?t.otherStudies.slice(0,3):t.otherStudies).map((s,i)=><article key={s.title}><h3><a href={s.url} target="_blank" rel="noreferrer">{impeccable&&lang==='ja'&&i===2?<><span className="phrase">AIでつくった自声</span><span className="phrase">による練習 · 2026</span></>:s.title}<ArrowUpRight size={16}/></a></h3><p>{impeccable?referenceSummaries[lang][i]:s.body}</p></article>)}</div></details></section>
 <DeveloperVoices lang={lang}/><Comparison lang={lang}/><Pricing lang={lang}/><section id="faq" className="section faq-section wrap"><div className="section-heading"><h2>{t.faqTitle}</h2></div><div>{t.faqs.map(f=><details key={f.q}><summary>{f.q}<Plus size={22}/></summary><p>{f.a}</p></details>)}</div></section>

 <FilmClosing lang={lang} cta={t.cta}/>
 </main><footer className="wrap"><Brand/><p>{t.footer}</p><span>© {new Date().getFullYear()} Lanclo</span></footer></>;
}
