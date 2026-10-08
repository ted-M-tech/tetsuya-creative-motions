import React, {useEffect, useRef} from 'react';

// Decorative voice-like traces, independently drawn; no audio or microphone input.
export default function HeroWave() {
 const ref = useRef(null);
 useEffect(() => {
  const canvas = ref.current;
  const ctx = canvas.getContext('2d');
  if (!ctx) return undefined;
  const surface = canvas.parentElement;
  const pointer = {x: 0.5, y: 0.5, targetX: 0.5, targetY: 0.5, strength: 0, targetStrength: 0};
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let width = 0, height = 0, frame = 0, visible = true, phase = 0, last = 0;
  function draw() {
   ctx.clearRect(0, 0, width, height);
   for (let layer = 1; layer >= 0; layer--) {
    const layerPhase = phase * (layer ? 0.82 : 1) + layer * 1.15;
    ctx.globalAlpha = layer ? 0.5 : 1;
   for (let line = 0; line < 7; line++) {
    ctx.beginPath();
    for (let x = 0; x <= width + 4; x += 4) {
     const u = x / width;
     const envelope = Math.sin(Math.PI * Math.min(u, 1)) ** 0.7;
     const wave = Math.sin(u * Math.PI * 3.5 + layerPhase + line * 0.24);
     const overtone = Math.sin(u * Math.PI * 6 - layerPhase * 0.6 + line * 0.35);
     const distance = (u - pointer.x) / 0.26;
     const influence = Math.exp(-distance * distance) * pointer.strength * envelope;
     const bend = influence * height * ((pointer.y - 0.5) * 0.42 + 0.055 * Math.sin(phase * 2 + line * 0.3));
     const y = bend * (layer ? 0.75 : 1) + height * (0.59 + layer * 0.065) + envelope * height * (layer ? 0.85 : 1) * (0.19 * wave + 0.055 * overtone) * (1 - line * 0.07);
     if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    const ink = ctx.createLinearGradient(0, 0, width, 0);
    ink.addColorStop(0, 'rgba(204,233,223,0)');
    ink.addColorStop(0.15, 'rgba(204,233,223,0.28)');
    ink.addColorStop(0.4, 'rgba(204,233,223,0.055)');
    ink.addColorStop(0.6, 'rgba(204,233,223,0.055)');
    ink.addColorStop(0.85, 'rgba(204,233,223,0.28)');
    ink.addColorStop(1, 'rgba(204,233,223,0)');
    ctx.strokeStyle = ink;
    ctx.lineWidth = line === 0 ? 1.6 : 1;
    ctx.stroke();
   }
   }
   ctx.globalAlpha = 1;
  }

  function tick(now) {
   const elapsed = last ? Math.min(now - last, 50) : 16;
   phase += elapsed * 0.00085;
   const ease = 1 - Math.exp(-elapsed / 110);
   pointer.x += (pointer.targetX - pointer.x) * ease;
   pointer.y += (pointer.targetY - pointer.y) * ease;
   pointer.strength += (pointer.targetStrength - pointer.strength) * ease;
   last = now;
   draw();
   frame = requestAnimationFrame(tick);
  }
  function sync() {
   cancelAnimationFrame(frame);
   last = 0;
   if (motion.matches || !visible || document.hidden) pointer.strength = pointer.targetStrength = 0;
   draw();
   if (visible && !document.hidden && !motion.matches) frame = requestAnimationFrame(tick);
  }
  function move(event) {
   if (event.pointerType !== 'mouse' || motion.matches) return;
   const box = surface.getBoundingClientRect();
   pointer.targetX = Math.max(0, Math.min(1, (event.clientX - box.left) / box.width));
   pointer.targetY = Math.max(0, Math.min(1, (event.clientY - box.top) / box.height));
   pointer.targetStrength = 1;
  }
  function leave() { pointer.targetStrength = 0; }
  surface.addEventListener('pointermove', move, {passive: true});
  surface.addEventListener('pointerleave', leave);
  surface.addEventListener('pointercancel', leave);
  const resize = new ResizeObserver(() => {
   const box = canvas.getBoundingClientRect();
   width = box.width; height = box.height;
   const scale = Math.min(window.devicePixelRatio || 1, 2);
   canvas.width = Math.round(width * scale);
   canvas.height = Math.round(height * scale);
   ctx.setTransform(scale, 0, 0, scale, 0, 0);
   sync();
  });
  const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); });
  resize.observe(canvas);
  observer.observe(canvas);
  motion.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  return () => {
   cancelAnimationFrame(frame);
   resize.disconnect(); observer.disconnect();
   surface.removeEventListener('pointermove', move);
   surface.removeEventListener('pointerleave', leave);
   surface.removeEventListener('pointercancel', leave);
   motion.removeEventListener('change', sync);
   document.removeEventListener('visibilitychange', sync);
  };
 }, []);
 return <canvas ref={ref} className="im-hero-wave" aria-hidden="true"/>;
}
