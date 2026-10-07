import React from 'react';
import {ArrowRight} from '@phosphor-icons/react';

const content={
 ja:{
  title:'声に込めた意図が、もっと伝わる。',
  body:'自分の声にネイティブの抑揚を移して練習。話し手の意図が伝わる割合が高まりました。',
  gain:'+26.4',unit:'ポイント',outcome:'発話意図の正識別率の前後差',chart:'話し手の意図を、母語話者が正しく判別した割合',labels:['練習前','練習後'],
  limit:'日本人イタリア語学習者7人、評価者17人。2文・3種類の意図による前後比較で、対照群はありません。外国語訛りの有意な改善はなく、英語やLancloの効果を示すものではありません。',
  metaTitle:'磨くところを決めて、発音を練習する。',metaBody:'発音指導を受けた学習者に、改善の報告。特定の音やリズムに焦点を当てた課題で、効果が明確でした。',metaUnit:'研究を統合',metaPeople:'2,573人を含むメタ分析',metaLimit:'発音指導一般の研究です。自声の効果を示すものではなく、自由な会話全体への効果はまだ明確ではありません。',
 },
 en:{
  title:'Help your intention come through.',
  body:'Practice with native prosody in the learner’s own voice was followed by clearer communication of intended meanings.',
  gain:'+26.4',unit:'percentage points',outcome:'Pre–post difference in correctly identified intentions',chart:'Intended meanings correctly identified by native listeners',labels:['Before practice','After practice'],
  limit:'7 Japanese learners of Italian; 17 listeners. A pre–post comparison using 2 sentences and 3 intentions, with no control group. Foreign accent did not significantly improve. This is not evidence of English-learning or Lanclo outcomes.',
  metaTitle:'Choose a focus. Work on your pronunciation.',metaBody:'Pronunciation instruction was associated with gains. Effects were clearest in tasks targeting particular sounds or prosody.',metaUnit:'studies combined',metaPeople:'A meta-analysis including 2,573 learners',metaLimit:'Research on pronunciation instruction in general, not the effect of own-voice models. Effects on overall spontaneous speech remain less clear.',
 },
 ko:{
  title:'목소리에 담은 의도가 더 잘 전달되도록.',
  body:'내 목소리에 원어민의 운율을 입혀 연습한 뒤, 의도가 정확히 전달된 비율이 높아졌습니다.',
  gain:'+26.4',unit:'퍼센트포인트',outcome:'발화 의도 정답 식별률의 연습 전후 차이',chart:'원어민 청자가 화자의 의도를 정확히 식별한 비율',labels:['연습 전','연습 후'],
  limit:'일본인 이탈리아어 학습자 7명, 평가자 17명. 2개 문장과 3가지 의도의 전후 비교로, 대조군은 없습니다. 외국어 억양의 유의한 개선은 없었으며, 영어 학습이나 Lanclo의 효과를 보여주는 결과가 아닙니다.',
  metaTitle:'연습할 부분을 정하고, 발음을 다듬으세요.',metaBody:'발음 지도를 받은 학습자의 향상이 보고되었습니다. 특정 소리나 운율에 초점을 맞춘 과제에서 효과가 뚜렷했습니다.',metaUnit:'개 연구 통합',metaPeople:'2,573명이 포함된 메타분석',metaLimit:'일반적인 발음 지도에 관한 연구이며, 자기 목소리의 효과를 보여주는 것은 아닙니다. 자유로운 대화 전반에 대한 효과는 아직 명확하지 않습니다.',
 },
};

export default function ResearchEvidence({lang='ja',compact=false}){
 const c=content[lang]||content.ja;
 if(compact)return <div className="evidence-single"><IntonationEvidence lang={lang}/></div>;
 return <div className="evidence-grid">
  {compact?<IntonationEvidence lang={lang}/>:<article className="research-comparison">
   <p className="eyebrow" lang="en">SELF-IMITATION / SLaTE 2015</p>
   <h3>{c.title}</h3><p>{c.body}</p>
   <div className="evidence-gain"><strong>{c.gain}</strong><span>{c.unit}</span><p>{c.outcome}</p></div>
   <figure className="pitch-chart"><figcaption>{c.chart}</figcaption>
    {[33.61,60.04].map((value,i)=><div className={`pitch-row ${i===1?'own':''}`} key={value}><span>{c.labels[i]}</span><div className="pitch-track" aria-hidden="true"><div style={{width:`${value}%`}}/></div><strong>{value.toFixed(2)}%</strong></div>)}
    <div className="pitch-axis" aria-hidden="true"><span>0%</span><span>50%</span><span>100%</span></div>
   </figure>
   <p className="study-limit">{lang==='ja'?'イタリア語学習者7人の前後比較・対照群なし。Lancloの効果検証ではありません。':lang==='ko'?'이탈리아어 학습자 7명의 전후 비교·대조군 없음. Lanclo의 효과 검증이 아닙니다.':'7 learners of Italian; pre–post study without a control group. Not a test of Lanclo.'}</p><details className="research-detail"><summary>{lang==='ja'?'実験の条件':lang==='ko'?'실험 조건':'Study conditions'}</summary><p>{c.limit}</p></details>
   <a href="https://www.isca-archive.org/slate_2015/pellegrino15_slate.pdf" target="_blank" rel="noreferrer" lang="en">Pellegrino &amp; Vigliano · Table 3 <ArrowRight size={16}/></a>
  </article>}
  <article className="research-practice">
   <p className="eyebrow" lang="en">THE UNIVERSITY OF TOKYO ET AL. / SLaTE 2025</p>
   <h3>{lang==='ja'?'自分に近い声が、まねる手がかりに。':lang==='ko'?'내게 익숙한 목소리가 모방의 단서로.':'A familiar voice. A closer model.'}</h3>
   {!compact&&<p>{lang==='ja'?'自分に聞こえる声に近づけたお手本で、声の好みと発音の模倣を調べた研究。':lang==='ko'?'평소 자신에게 들리는 목소리에 가까운 예시로 선호도와 발음 모방을 살펴본 연구.':'Researchers tested voice preference and imitation using models adjusted to the voice learners hear as their own.'}</p>}
   <div className="tokyo-finding">{!compact&&<span>{lang==='ja'?'研究の着眼点':lang==='ko'?'연구의 초점':'THE IDEA'}</span>}<strong>{lang==='ja'?'ネイティブの発音':lang==='ko'?'원어민의 발음':'Native pronunciation'}</strong><b aria-hidden="true">×</b><strong>{lang==='ja'?'自分に近い声質':lang==='ko'?'나와 비슷한 음색':'A voice closer to yours'}</strong><p>{lang==='ja'?'好まれ、より正確にまねられた特徴も。':lang==='ko'?'더 선호되며 일부 특징은 더 정확하게 모방됐습니다.':'Preferred by learners, with closer imitation of some features.'}</p></div>
   <p className="study-limit">{lang==='ja'?'日本語話者15人の短期実験。通常の録音クローンとは方式が異なり、Lancloの効果検証ではありません。':lang==='ko'?'일본어 화자 15명의 단기 실험. 일반 음성 복제와 방식이 다르며 Lanclo의 효과 검증은 아닙니다.':'A short-term study of 15 Japanese speakers. Different from ordinary voice cloning; not a test of Lanclo.'}</p>
   <a href="https://www.isca-archive.org/slate_2025/yamanaka25_slate.html" target="_blank" rel="noreferrer" lang="en">Yamanaka et al. · SLaTE 2025 <ArrowRight size={16}/></a>
  </article>
 </div>;
}

function IntonationEvidence({lang}){
 const c={ja:{title:'抑揚テストの伸び、約1.3倍。',metric:'得点の上昇幅を比較',labels:['ネイティブのお手本','自分の声のお手本'],limit:'66人・12週間の英語抑揚研究。Lancloの効果検証ではありません。',more:'研究の条件と計算',detail:'各群33人。自声群は213.48→300.09点、ネイティブ群は210.00→275.52点。伸び86.61÷65.52＝約1.32倍。最終得点や学習速度の比ではありません。自声にネイティブの抑揚を移した教材を用いた研究です。'},en:{title:'About 1.3× the intonation score gain.',metric:'Comparison of score gains',labels:['Native-speaker model','Own-voice model'],limit:'66 learners, 12 weeks, English intonation. Not a test of Lanclo.',more:'Study conditions and calculation',detail:'33 learners per group. Own-voice: 213.48→300.09; native model: 210.00→275.52. Gains of 86.61÷65.52≈1.32. Not a ratio of final scores or learning speed. The study transferred native prosody into learners’ voices.'},ko:{title:'억양 점수 상승 폭, 약 1.3배.',metric:'점수 상승 폭 비교',labels:['원어민 목소리 예시','내 목소리 예시'],limit:'66명·12주 영어 억양 연구. Lanclo의 효과 검증은 아닙니다.',more:'연구 조건과 계산',detail:'각 그룹 33명. 자기 목소리 213.48→300.09점, 원어민 목소리 210.00→275.52점. 상승 폭 86.61÷65.52≈1.32배. 최종 점수나 학습 속도의 비율이 아닙니다. 자기 목소리에 원어민의 운율을 입힌 연구입니다.'}}[lang];
 return <article className="research-comparison intonation-evidence"><p className="eyebrow" lang="en">Li et al. / GEMA 2020</p><div className="research-big-result"><h3>{lang==='ja'?<><span className="phrase">英語の抑揚テスト、</span><span className="phrase">得点の伸び。</span></>:lang==='ko'?'영어 억양 테스트 점수 상승 폭.':'English intonation test score gains.'}</h3><p><span>{lang==='ja'?'約':lang==='ko'?'약':'About'}</span><strong>1.3</strong><span>{lang==='ja'?'倍':lang==='ko'?'배':'×'}</span></p></div><figure className="pitch-chart"><figcaption>{c.metric}</figcaption>{[65.52,86.61].map((value,i)=><div className={`pitch-row ${i?'own':''}`} key={value}><span>{c.labels[i]}</span><div className="pitch-track" aria-hidden="true"><div style={{width:`${value}%`}}/></div><strong>+{value.toFixed(2)}</strong></div>)}<div className="pitch-axis" aria-hidden="true"><span>0</span><span>50</span><span>100</span></div></figure><p className="study-limit">{c.limit}</p><details className="research-detail"><summary>{c.more}</summary><p>{c.detail}</p></details><a href="https://ejournal.ukm.my/gema/article/download/35992/10245" target="_blank" rel="noreferrer" lang="en">Li, Lian &amp; Yodkamlue · Tables 2–5 <ArrowRight size={16}/></a></article>;
}
