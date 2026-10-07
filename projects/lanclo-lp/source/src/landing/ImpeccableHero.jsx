import React from 'react';
import {ArrowUpRight} from '@phosphor-icons/react';
import {VoiceMotion} from './StoryMotion.jsx';
const copy={
 ja:{pain:'シャドーイング、その先へ。',frustration:'',title:'自分の声が、\nネイティブのお手本に。',body:'あなたの声質で、ネイティブの発音を聴く。',pause:'映像を止める',play:'映像を動かす',caption:'録音 → お手本 → 発音練習'},
 en:{pain:'Beyond shadowing.',frustration:'',title:'Your voice.\nA native-pronunciation model.',body:'A model in your voice. Practice shaped by your needs.',pause:'Pause film',play:'Play film',caption:'Record your voice. Listen. Practice. Illustrative film.'},
 ko:{pain:'쉐도잉, 그다음으로.',frustration:'',title:'내 목소리가,\n원어민 발음의 모델로.',body:'발음 예시도, 다음 연습도.\n나에게 맞추는 AI 발음 트레이닝.',pause:'영상 멈추기',play:'영상 재생',caption:'목소리를 등록하고, 듣고, 연습해요. 이용 예시 영상'}
};
export default function ImpeccableHero({lang,cta}){
 const c=copy[lang];
 return <section className="im-hero"><div className="wrap im-opening"><p className="im-pain">{c.pain}{c.frustration&&<span>{c.frustration}</span>}</p><h1><span>{c.title.split("\n")[0]}</span><strong>{c.title.split("\n")[1]}</strong></h1><a className="action" href="https://voice.maepace.com/">{cta}<ArrowUpRight size={20}/></a></div><div className="im-film"><VoiceMotion lang={lang}/></div></section>;
}
