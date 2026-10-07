// Adapted from ObsidianUI loaders-gooey-blobs (MIT, see ./LICENSE).
// https://www.obsidianui.dev/r/loaders-gooey-blobs.json
// Adaptations: JSX, plain styles (no Tailwind), decorative semantics because
// VoicePreparation provides the localized status; original motion preserved.
import './loader-gooey-blobs.css';
import React,{useId} from 'react';
import {motion,useReducedMotion} from 'motion/react';
export default function LoaderGooeyBlobs({size=40,color='#0071e3',duration=2.4,height=152}){
 const filterId=`gooey-${useId().replace(/:/g,'')}`;
 const reducedMotion=useReducedMotion();
 return <div aria-hidden="true" style={{display:'flex',alignItems:'center',justifyContent:'center',height,position:'relative'}}>
  <svg aria-hidden="true" focusable="false" width="0" height="0" style={{position:'absolute'}}><defs><filter id={filterId}>
   <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>
   <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="gooey"/>
   <feBlend in="SourceGraphic" in2="gooey"/>
  </filter></defs></svg>
  <span style={{display:'flex',gap:4,filter:`url(#${filterId})`}}>
   {[0,1,2].map(index=><motion.span className="obsidian-gooey-dot" key={`${index}-${reducedMotion}`} style={{display:'block',borderRadius:'50%',width:size,height:size,backgroundColor:color}}
    animate={reducedMotion?{x:0,scale:1}:{x:[0,15,0,-15,0],scale:[1,1.2,1,1.2,1]}}
    transition={reducedMotion?{duration:0}:{duration,ease:'easeInOut',repeat:Infinity,delay:index*.2}}/>)}
  </span>
 </div>;
}
