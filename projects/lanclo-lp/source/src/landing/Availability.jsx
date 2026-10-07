import React from 'react';
import {Globe,ArrowUpRight} from '@phosphor-icons/react';
export default function Availability({lang='ja',action=false}){
 const c={ja:{web:'Webアプリ',status:'先行モニター体験中',soon:'近日リリース',cta:'Webで先行体験する'},en:{web:'Web app',status:'Early access pilot',soon:'Coming soon',cta:'Try the web pilot'},ko:{web:'웹 앱',status:'얼리 액세스 체험 중',soon:'출시 예정',cta:'웹에서 먼저 체험하기'}}[lang];
 return <div className="availability"><div className="availability-web"><Globe size={20}/><span>{c.web}<strong>{c.status}</strong></span></div>{action&&<a className="action" href="https://voice.maepace.com/">{c.cta}<ArrowUpRight size={20}/></a>}<p className="availability-store"><span>App Store</span><small>{c.soon}</small></p></div>;
}
