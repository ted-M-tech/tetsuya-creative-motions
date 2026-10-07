// Adapted from ObsidianUI Flip Text (MIT, see ./LICENSE).
// Source: https://www.obsidianui.dev/docs/flip-text (2026-10-05).
// Reveal letters in sequence on mount, with optional hover/focus replay. No loop.
import React,{useEffect,useRef,useState} from 'react';
import {motion,useReducedMotion} from 'motion/react';
import './flip-text.css';
export default function FlipText({children}){
 const reduced=useReducedMotion(),ref=useRef(null);
 const [hovered,setHovered]=useState(null),[focused,setFocused]=useState(false);
 useEffect(()=>{
  const link=ref.current?.closest('a,button');if(!link)return;
  const focus=()=>setFocused(link.matches(':focus-visible')),blur=()=>setFocused(false);
  link.addEventListener('focus',focus);link.addEventListener('blur',blur);
  return()=>{link.removeEventListener('focus',focus);link.removeEventListener('blur',blur)};
 },[]);
 return <span className="obsidian-flip-text" ref={ref}>
  <span className="obsidian-flip-accessible">{children}</span>
  <span aria-hidden="true">{children.split('').map((char,index)=><motion.span className="obsidian-flip-char" key={index} onMouseEnter={()=>setHovered(index)} onMouseLeave={()=>setHovered(null)} initial={reduced?false:{rotateX:0,y:0}} animate={{rotateX:reduced?0:(hovered===index||focused?720:360),y:!reduced&&(hovered===index||focused)?-3:0}} transition={{duration:reduced?0:.6,delay:reduced||hovered===index||focused?0:.2+index*.1,ease:'easeOut'}}>{char===' '?'\u00a0':char}</motion.span>)}</span>
 </span>;
}
