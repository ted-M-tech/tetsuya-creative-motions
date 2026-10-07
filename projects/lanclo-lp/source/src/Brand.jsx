import React from 'react';
import './brand.css';
import FlipText from './ui/obsidian/FlipText.jsx';

export default function Brand({animate=false}) {
 return <span className="vt-brand"><img className="vt-brand-icon" src={import.meta.env.BASE_URL+"brand/mark.svg?v=lanclo-2"} width="32" height="32" alt="" aria-hidden="true"/>{animate?<FlipText>Lanclo</FlipText>:<span>Lanclo</span>}</span>;
}
