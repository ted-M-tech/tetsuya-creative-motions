import React,{useRef,useState} from 'react';
import {Play,X} from '@phosphor-icons/react';
import poster from './assets/practice-film-poster.webp?url';

const copy={
 ja:{action:'12秒で、練習の流れを見る',title:'録音して、聴いて、声に出す。',note:'無音・日本語の紹介映像。画面と発音は利用イメージで、学習者の実測結果ではありません。初回は声の登録・同意が必要です。',close:'動画を閉じる',error:'動画を読み込めませんでした。下のページでも練習の流れをご覧いただけます。'},
 en:{action:'See the practice flow in 12 seconds',title:'Record. Listen. Say it yourself.',note:'Silent video with Japanese text. Screens and pronunciation are illustrative, not measured learner results. Voice setup and consent are required first.',close:'Close video',error:'The video could not load. Explore the practice flow on the page below.'},
 ko:{action:'12초로 보는 연습 과정',title:'녹음하고, 듣고, 말해 보세요.',note:'일본어 화면의 무음 소개 영상입니다. 화면과 발음은 이용 예시이며 실제 학습 결과가 아닙니다. 처음에는 목소리 등록과 동의가 필요합니다.',close:'영상 닫기',error:'영상을 불러오지 못했습니다. 아래 페이지에서 연습 과정을 확인해 주세요.'}
};
// Only an independently reviewed excerpt may be configured here, never the full r26.
const filmUrl=import.meta.env.VITE_LP_PRACTICE_FILM_URL||'';
export default function PracticeFilm({lang}){
 const dialog=useRef(null),video=useRef(null),trigger=useRef(null);
 const [active,setActive]=useState(false),[failed,setFailed]=useState(false);const c=copy[lang];
 if(!filmUrl)return null;
 function trapTab(e){if(e.key!=='Tab')return;const buttons=dialog.current.querySelectorAll('button');const first=buttons[0],last=buttons[buttons.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}else{requestAnimationFrame(()=>{if(dialog.current?.open&&!dialog.current.contains(document.activeElement))last.focus();});}}
 function open(){setFailed(false);setActive(true);dialog.current.showModal();dialog.current.querySelector('button').focus();}
 function close(){video.current?.pause();dialog.current.close();setActive(false);trigger.current?.focus();}
 return <><button ref={trigger} className="practice-film-trigger" onClick={open}><Play size={18} weight="fill" aria-hidden="true"/>{c.action}</button>
 <dialog ref={dialog} className="practice-film-dialog" aria-labelledby="practice-film-title" aria-describedby="practice-film-note" onKeyDown={trapTab} onCancel={e=>{e.preventDefault();close();}} onClick={e=>{if(e.target===e.currentTarget)close();}}>
 <div className="practice-film-content"><div className="practice-film-heading"><h2 id="practice-film-title">{c.title}</h2><button autoFocus onClick={close} aria-label={c.close}><X size={24}/></button></div>
 {active&&<video ref={video} width="1280" height="720" controls playsInline preload="none" poster={poster} src={filmUrl} aria-label={c.title} onError={()=>setFailed(true)}/>}
 {failed&&<p role="status">{c.error}</p>}<p id="practice-film-note">{c.note}</p><button className="practice-film-close" onClick={close}>{c.close}</button></div></dialog></>;
}
