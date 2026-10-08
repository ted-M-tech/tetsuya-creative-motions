import React from 'react';

// Original vector scenes: sound inspection, lesson assembly, and one-tap reading.
export default function PracticeStepArt({step}) {
 return <svg className="practice-step-art" viewBox="0 0 220 140" aria-hidden="true" focusable="false">
  {step===0?<>
   <rect x="16" y="31" width="158" height="86" rx="13" fill="#172e3e"/>
   {[18,30,45,25,58,36,20,43,26,15].map((h,i)=><rect key={i} x={30+i*13} y={75-h/2} width="5" height={h} rx="2.5" fill={i===4?'#cce9df':'#5b7f9f'}/>)}
   <path d="M154 88l35 32" stroke="#fffaf0" strokeWidth="12" strokeLinecap="round"/>
   <circle cx="129" cy="64" r="36" fill="#0b1722" stroke="#cce9df" strokeWidth="5"/>
   <path d="M107 65h8l5-16 9 33 8-27 5 10h10" fill="none" stroke="#cce9df" strokeWidth="4" strokeLinejoin="round"/>
   <circle cx="184" cy="30" r="12" fill="#cce9df"/><path d="m178 30 4 4 7-8" fill="none" stroke="#182f42" strokeWidth="2.5"/>
  </>:step===1?<>
   <rect x="16" y="21" width="64" height="42" rx="7" fill="#244456" transform="rotate(-9 48 42)"/>
   <path d="M29 35h28m-26 10h18" stroke="#8cafbd" strokeWidth="4" strokeLinecap="round"/>
   <rect x="20" y="82" width="64" height="39" rx="7" fill="#244456" transform="rotate(8 52 101)"/>
   <path d="M33 96h29m-27 10h18" stroke="#8cafbd" strokeWidth="4" strokeLinecap="round"/>
   <path d="M78 46q25 0 30 24M81 99q22 0 27-23" fill="none" stroke="#5b7f9f" strokeWidth="2" strokeDasharray="4 4"/>
   <rect x="112" y="18" width="83" height="109" rx="9" fill="#fffaf0"/>
   <rect x="125" y="36" width="41" height="9" rx="3" fill="#5b7f9f"/>
   <path d="M125 60h55m-55 13h45m-45 13h51m-51 13h34" stroke="#bbcdd0" strokeWidth="5" strokeLinecap="round"/>
   <path d="m104 49 4 10 10 4-10 4-4 10-4-10-10-4 10-4Z" fill="#cce9df"/>
   <rect x="132" y="68" width="24" height="10" rx="2" fill="#a5d7c9"/>
  </>:<>
   <rect x="37" y="11" width="105" height="120" rx="15" fill="#172e3e" stroke="#5b7f9f" strokeWidth="2"/>
   <path d="M54 33h64m-64 12h49m-49 12h59" stroke="#cce9df" strokeWidth="4" strokeLinecap="round"/>
   <rect x="54" y="78" width="70" height="31" rx="8" fill="#cce9df"/><path d="m83 86 13 8-13 8Z" fill="#182f42"/>
   <path d="m113 99 5 31 7-9 12-1Z" fill="#fffaf0" stroke="#0b1722" strokeWidth="2"/>
   <path d="m105 91-5-6m11 0v-8m-15 22h-8" stroke="#fffaf0" strokeWidth="2" strokeLinecap="round"/>
   <rect x="165" y="37" width="20" height="35" rx="10" fill="#cce9df"/><path d="M157 58v5a18 18 0 0 0 36 0v-5m-18 23v16m-10 0h20" fill="none" stroke="#8cafbd" strokeWidth="3" strokeLinecap="round"/>
   <path d="M200 42q10 13 0 26" fill="none" stroke="#5b7f9f" strokeWidth="3" strokeLinecap="round"/>
  </>}
 </svg>;
}
