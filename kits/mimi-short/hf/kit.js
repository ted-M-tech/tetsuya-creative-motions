// Mimi shorts kit: markup builders and motion helpers shared by every episode.
// Load after GSAP; an episode creates its paused timeline, calls these, then registers window.__timelines["main"].
(function () {
  const STAR = '<path d="M5 0 6 4 10 5 6 6 5 10 4 6 0 5 4 4Z" fill="FILL"/>';

  // Five-axis radar into <svg class="radar" viewBox="0 0 360 380">. values 0..1, warn: index of the axis in red.
  function radar(svg, { labels, values, score, warn = -1 }) {
    const cx = 180, cy = 190, R = 118, pt = (i, r) => {
      const a = -Math.PI / 2 + (i * 2 * Math.PI) / 5;
      return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
    };
    const poly = (r) => [0, 1, 2, 3, 4].map((i) => pt(i, r).map((v) => v.toFixed(1)).join(",")).join(" ");
    let s = "";
    for (const k of [1 / 3, 2 / 3, 1]) s += `<polygon points="${poly(R * k)}" fill="none" stroke="#ccd8df" stroke-width="2"/>`;
    for (let i = 0; i < 5; i++) { const [x, y] = pt(i, R); s += `<line x1="${cx}" y1="${cy}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="#ccd8df" stroke-width="2"/>`; }
    const shape = values.map((v, i) => pt(i, R * v).map((n) => n.toFixed(1)).join(",")).join(" ");
    s += `<g class="r-shape" style="transform-origin:${cx}px ${cy}px"><polygon points="${shape}" fill="rgba(91,127,159,0.30)" stroke="#5b7f9f" stroke-width="5" stroke-linejoin="round"/></g>`;
    labels.forEach((l, i) => {
      const [x, y] = pt(i, R + 34);
      s += `<text x="${x.toFixed(1)}" y="${y.toFixed(1)}" text-anchor="middle" dominant-baseline="middle" font-size="22" font-weight="700" fill="${i === warn ? "#e5484d" : "#273b4b"}">${l}</text>`;
    });
    s += `<circle cx="${cx}" cy="${cy}" r="44" fill="#ffffff"/><text class="r-score" x="${cx}" y="${cy + 2}" text-anchor="middle" dominant-baseline="middle" font-size="46" font-weight="700" fill="#344f69">${score}</text>`;
    svg.innerHTML = s;
  }

  function sparkles(el, spots) {
    el.innerHTML = spots.map(([x, y, c]) => `<svg viewBox="0 0 10 10" style="left:${x}px;top:${y}px">${STAR.replace("FILL", c || "#ffd84a")}</svg>`).join("");
  }

  function bars(el, n = 13) { el.innerHTML = "<i></i>".repeat(n); }

  function kit(tl) {
    return {
      pop: (sel, at) => tl.fromTo(sel, { scale: 0.86, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.18, ease: "back.out(2)" }, at),
      tagIn: (sel, at) => tl.fromTo(sel, { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.2, ease: "power2.out" }, at),
      ripple: (sel, at) => tl.fromTo(sel, { scale: 0.3, opacity: 1 }, { scale: 2.2, opacity: 0, duration: 0.25, ease: "power2.out" }, at),
      press: (sel, at, s = 0.88) => tl.fromTo(sel, { scale: 1 }, { scale: s, duration: 0.1, yoyo: true, repeat: 1 }, at),
      wave: (sel, at, dur, seed = 0) => document.querySelectorAll(sel + " i").forEach((b, i) =>
        tl.fromTo(b, { height: 8 }, { height: 14 + 24 * Math.abs(Math.sin(i * 1.3 + seed)), duration: 0.16, yoyo: true,
          repeat: Math.max(1, Math.round(dur / 0.16)), ease: "sine.inOut", immediateRender: false }, at + i * 0.02)),
      twinkle: (sel, at) => document.querySelectorAll(sel + " svg").forEach((s, i) =>
        tl.fromTo(s, { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: 0.25, ease: "back.out(3)" }, at + i * 0.06)),
      // Result card: pops in, radar grows, score counts up, the tip and the replay chip follow.
      result: (sel, at, score) => {
        const card = document.querySelector(sel), num = card.querySelector(".r-score"), sc = { v: 0 };
        tl.fromTo(card, { y: 60, scale: 0.9, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.25, ease: "back.out(1.8)" }, at);
        tl.fromTo(card.querySelector(".r-shape"), { scale: 0 }, { scale: 1, duration: 0.45, ease: "back.out(1.6)" }, at + 0.15);
        tl.fromTo(sc, { v: 0 }, { v: score, duration: 0.6, ease: "power2.out", onUpdate: () => { num.textContent = Math.round(sc.v); } }, at + 0.15);
        tl.fromTo(card.querySelector(".r-tip"), { x: 40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, at + 0.75);
        const again = card.querySelector(".r-again");
        if (again) tl.fromTo(again, { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2)" }, at + 1.0);
      },
      // End card builds in 0.4 s.
      end: (at) => {
        tl.fromTo("#end-mimi", { y: -80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.22, ease: "back.out(1.8)" }, at);
        tl.fromTo("#end-lockup", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, at + 0.04);
        tl.fromTo("#end-line", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, at + 0.08);
        tl.fromTo("#end-cta", { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }, at + 0.12);
        tl.fromTo("#end-store", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.25, ease: "power2.out" }, at + 0.12);
      },
    };
  }

  // Standard end card markup (ids used by kit.end).
  function endCard(el, line, cta) {
    el.innerHTML = `<img id="end-mimi" class="mimi" src="assets/kit/brand/mimi-end.png" alt="" />
      <div id="end-lockup" class="lockup"><img src="assets/kit/brand/mark.png" alt="" /><span>Lanclo</span></div>
      <div id="end-line" class="line">${line}</div><div id="end-cta" class="cta">${cta}</div>
      <img id="end-store" class="store" src="assets/kit/brand/appstore.png" alt="App Store" />`;
  }

  window.MimiKit = { radar, sparkles, bars, kit, endCard };
})();
