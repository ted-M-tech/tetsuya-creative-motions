import React from 'react';
import {motion, useReducedMotion} from 'motion/react';
import {narrative} from './narrative.js';

const labels = {
  ja: {
    caption: 'Lanclo の実際の画面 · 表示内容はデモデータです。',
    note: '同じアカウントでログインし、保存と同期を有効にしたデータを引き継げます。',
    desktop: 'パソコンで表示した Lanclo の練習画面',
    tablet: 'タブレットで表示した Lanclo の練習画面',
    phone: 'スマートフォンで表示した Lanclo の練習画面',
  },
  en: {
    caption: 'Actual Lanclo screens · Illustrative demo data.',
    note: 'Sign in to the same account to continue with data you have chosen to save and sync.',
    desktop: 'Lanclo practice on a computer',
    tablet: 'Lanclo practice on a tablet',
    phone: 'Lanclo practice on a phone',
  },
  ko: {
    caption: '실제 Lanclo 화면 · 표시 내용은 데모 데이터입니다.',
    note: '같은 계정으로 로그인하면 저장 및 동기화를 선택한 데이터를 이어서 사용할 수 있습니다.',
    desktop: '컴퓨터에서 보는 Lanclo 연습 화면',
    tablet: '태블릿에서 보는 Lanclo 연습 화면',
    phone: '스마트폰에서 보는 Lanclo 연습 화면',
  },
};

export default function PremiumDevices({lang}) {
  const n = narrative[lang];
  const c = labels[lang];
  const reduce = useReducedMotion();
  return <section id="devices" className="section premium-devices">
    <div className="wrap">
      <div className="device-introduction">
        <div className="section-heading">

          <h2>{lang==='ja'?<><span className="phrase">スマホでも、PCでも。</span><span className="phrase">いつもの声で、</span><span className="phrase">練習の続きへ。</span></>:n.devicesTitle}</h2>
        </div>
      </div>
      <motion.figure className="hardware-figure"
        initial={reduce ? false : {opacity: 0, y: 32}}
        animate={reduce ? {opacity: 1, y: 0} : undefined}
        whileInView={{opacity: 1, y: 0}}
        viewport={{once: true, amount: .2}}
        transition={{duration: reduce ? 0 : .8, ease: [.2, .7, .2, 1]}}>
        <div className="hardware-stage">
          <div className="hardware-laptop">
            <div className="laptop-lid">
              <i className="hardware-camera" aria-hidden="true"/>
              <div className="hardware-screen">
                <img src={`${import.meta.env.BASE_URL}screens/device-desktop.webp`} width="1280" height="800" alt={c.desktop} loading="lazy"/>
              </div>
            </div>
            <div className="laptop-base" aria-hidden="true"><span/></div>
          </div>
          <div className="hardware-tablet">
            <div className="tablet-rim">
              <i className="hardware-camera" aria-hidden="true"/>
              <div className="hardware-screen">
                <img src={`${import.meta.env.BASE_URL}screens/device-tablet.webp`} width="820" height="1100" alt={c.tablet} loading="lazy"/>
              </div>
            </div>
          </div>
          <div className="hardware-phone">
            <span className="phone-side-button" aria-hidden="true"/>
            <div className="phone-rim">
              <div className="phone-glass">
                <div className="phone-top" aria-hidden="true"><span className="phone-island"/></div>
                <div className="hardware-screen">
                  <img src={`${import.meta.env.BASE_URL}screens/device-phone.webp`} width="390" height="844" alt={c.phone} loading="lazy"/>
                </div>
                <div className="phone-bottom" aria-hidden="true"><span/></div>
              </div>
            </div>
          </div>
        </div>
        <figcaption>{c.caption}</figcaption>
      </motion.figure>
      <p className="device-sync-note">{c.note}</p>
    </div>
  </section>;
}
