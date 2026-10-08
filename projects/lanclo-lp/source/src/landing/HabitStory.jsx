import React from 'react';
import {ArrowRight,ArrowDown,Play,Target,Sparkle} from '@phosphor-icons/react';
import PracticeStepArt from './PracticeStepArt.jsx';
import './habit-practice.css';
const copy={
 ja:{lead:'次の練習も、AIにおまかせ。',title:'あなたは、\n声に出すだけ。',body:'苦手な音と練習履歴から、復習する文と新しい文を組み合わせます。',focus:'今回の練習ポイント',plan:'次のレッスンへ',review:'もう一度',fresh:'別の文で',long:'少し長い文へ',note:'候補教材から組み立てるレッスンの例',habit:'まずは、1日10分から。',habitBody:'忙しい日は、一文からでも。自分のペースで、今日の練習へ。',bridge:'続けるきっかけは、好きな話題にも。'},
 en:{lead:'Let AI plan what comes next.',title:'You just\nkeep speaking.',body:'Sounds that need attention and your practice history shape a mix of review and new sentences.',focus:'Your practice focus',plan:'Your next lesson',review:'Try it again',fresh:'Another sentence',long:'A longer sentence',note:'Example lesson assembled from available material',habit:'Start with 10 minutes a day.',habitBody:'On busy days, start with one sentence. Practice at your own pace.',bridge:'And let your curiosity bring you back.'},
 ko:{lead:'다음 연습도 AI에게 맡기세요.',title:'나는 그저,\n소리 내어 말해요.',body:'어려운 소리와 연습 기록을 바탕으로 복습할 문장과 새로운 문장을 조합해요.',focus:'이번 연습 포인트',plan:'다음 레슨으로',review:'다시 한번',fresh:'다른 문장으로',long:'조금 더 긴 문장',note:'준비된 교재로 구성한 레슨 예시',habit:'하루 10분부터 시작해요.',habitBody:'바쁜 날엔 한 문장부터. 내 페이스로 오늘의 연습을 이어가세요.',bridge:'좋아하는 이야기도, 계속할 이유가 돼요.'}
};
const visualCopy={
 ja:{steps:['苦手分析','レッスン生成','ボタンを押して読むだけ'],focus:'練習したい音',lesson:'あなた向けの一文',read:'声に出して読もう',start:'練習をはじめる',example:'レッスン生成から練習までのイメージ'},
 en:{steps:['Analyse weak points','Generate a lesson','Press a button and read'],focus:'A sound to practise',lesson:'A sentence for you',read:'Read it out loud',start:'Start practising',example:'Illustration of lesson generation and practice'},
 ko:{steps:['취약점 분석','레슨 생성','버튼을 누르고 읽기만'],focus:'연습할 소리',lesson:'나를 위한 문장',read:'소리 내어 읽어요',start:'연습 시작',example:'레슨 생성부터 연습까지의 예시'}
};
export default function HabitStory({lang}){
 const c=copy[lang],v=visualCopy[lang];
 return <section className="habit-story" aria-labelledby="habit-title"><div className="wrap"><div className="habit-stage">
  <div className="habit-copy"><p>{c.lead}</p><h2 id="habit-title">{c.title}</h2><p className="habit-body">{c.body}</p></div>
  <figure className="habit-practice">
   <ol className="habit-flow">
    <li><div className="habit-flow-heading"><span>01</span><Target size={24} aria-hidden="true"/><h3>{v.steps[0]}</h3></div><div className="habit-flow-scene"><PracticeStepArt step={0}/><div className="habit-analysis"><small>{v.focus}</small><strong>/θ/</strong><span><mark>th</mark>ink · <mark>th</mark>ree</span></div></div><ArrowDown className="habit-flow-arrow" size={24} aria-hidden="true"/></li>
    <li><div className="habit-flow-heading"><span>02</span><Sparkle size={24} aria-hidden="true"/><h3>{v.steps[1]}</h3></div><div className="habit-flow-scene"><PracticeStepArt step={1}/><div className="habit-generated"><small>{v.lesson}</small><p>I <mark>think</mark> the meeting starts at <mark>three</mark>.</p></div></div><ArrowDown className="habit-flow-arrow" size={24} aria-hidden="true"/></li>
    <li><div className="habit-flow-heading"><span>03</span><Play size={24} aria-hidden="true"/><h3>{v.steps[2]}</h3></div><div className="habit-flow-scene"><PracticeStepArt step={2}/><div className="habit-read"><span className="habit-demo-start"><Play size={18} weight="fill" aria-hidden="true"/>{v.start}</span><p>{v.read}</p></div></div></li>
   </ol>
  </figure>
 </div><div className="habit-daily"><h3>{c.habit}</h3></div><p className="habit-bridge">{c.bridge}<ArrowDown size={24}/></p></div></section>
}
