import React from 'react';
import photo from './assets/developer-beach.webp?url';
import secondPhoto from './assets/developer-ballpark.webp?url';
import './developer-voices.css';

const voices = {
 ja: {
  title: '開発者の声',
  first: { body: 'シャドーイングで、自分に似た声のお手本を探すのが大変でした。海外で暮らしていても、発音が伝わらないことがある。自分が目指す英語を、自分の声で聴いてみたい。それが、Lancloの始まりです。' },
  second: { body: 'カナダに住んでて実際にネイティブに何回も発音を指摘されもどかしい気持ちを体験しました。自分が毎日使いたくなるアプリを自分で開発して作った。そしてそれをいろんな人に使ってもらいたい。' },
  role: 'Lanclo 開発者', alt: '海辺で撮影したLanclo開発者', secondAlt: '球場で撮影したLanclo開発者の横顔',
 },
 en: {
  title: 'From the people building Lanclo',
  first: { body: 'Finding a shadowing model with a voice like mine was difficult. Even while living abroad, there are times when my pronunciation is not understood. I wanted to hear the English I aspire to speak in my own voice. That is where Lanclo began.' },
  second: { body: 'Living in Canada, I experienced the frustration of having my pronunciation corrected by native speakers many times. I developed an app that I would want to use every day. And I want many people to use it.' },
  role: 'Lanclo developer', alt: 'A Lanclo developer photographed at the beach', secondAlt: 'A Lanclo developer photographed in profile at a baseball stadium',
 },
 ko: {
  title: 'Lanclo를 만드는 사람들의 이야기',
  first: { body: '쉐도잉을 할 때 나와 목소리가 비슷한 발음 예시를 찾기가 어려웠습니다. 해외에 살고 있어도 발음이 통하지 않을 때가 있습니다. 내가 목표로 하는 영어를 내 목소리로 들어 보고 싶었습니다. 그것이 Lanclo의 시작입니다.' },
  second: { body: '캐나다에 살면서 실제로 원어민에게 여러 번 발음을 지적받아 답답함을 느꼈습니다. 제가 매일 쓰고 싶은 앱을 직접 개발해 만들었습니다. 그리고 많은 사람들이 사용해 주었으면 합니다.' },
  role: 'Lanclo 개발자', alt: '해변에서 촬영한 Lanclo 개발자', secondAlt: '야구장에서 촬영한 Lanclo 개발자의 옆모습',
 },
};

export default function DeveloperVoices({lang}: {lang: keyof typeof voices}) {
 const c = voices[lang];
 return <section className="developer-voices" aria-labelledby="developer-voices-title">
  <div className="wrap">
   <h2 id="developer-voices-title">{c.title}</h2>
   <div className="developer-stories">
   <figure className="developer-story developer-story-photo">
    <div className="developer-portrait"><img src={photo} width="1114" height="1484" loading="lazy" decoding="async" alt={c.alt}/></div>
    <div className="developer-story-copy"><blockquote><p>{c.first.body}</p></blockquote><figcaption>{c.role}</figcaption></div>
   </figure>
   <figure className="developer-story developer-story-letter">
    <div className="developer-portrait developer-portrait-ballpark"><img src={secondPhoto} width="768" height="1024" loading="lazy" decoding="async" alt={c.secondAlt}/></div>
    <div className="developer-story-copy"><blockquote><p>{c.second.body}</p></blockquote><figcaption>{c.role}</figcaption></div>
   </figure>
   </div>
  </div>
 </section>;
}
