"""Render the English journal feature short (9:16) frame by frame (cairo) and pipe to ffmpeg.

usage: journal.py OUT.mp4 [--scale 0.5] [--fps 30] [--from 0 --to 22.5] [--still T,T,...] [--audio mix.wav]
"""
import argparse
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cairo
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from render import (A, PAPER, SOFT, INK, PRIMARY, BRAND_C, MUTED, LINE_SOFT, PINK, rgb, clamp, prog,  # noqa: E402
                    ease_io, ease_out, ease_in, ease_back, spring, lerp, to_surface, image, text_width, draw_text,
                    draw_image, round_rect, card, pill, bezier, draw_line, glow_dot, stroke_path, lockup, draw_parts)
from journal_timeline import *  # noqa: E402,F403

W0, H0 = 1080, 1920


# ---------- the illustration (app demo style sheet, 3x2 tiles) ----------
TILES = ['coffee', 'trees', 'laptop', 'book', 'shoes', 'ramen']


@lru_cache(None)
def tile_rgba(name):
    """Tile on transparent paper: alpha from darkness, colour un-multiplied against white."""
    i = TILES.index(name)
    img = Image.open(A / 'journal-art.png').convert('RGB')
    tw, th = img.width // 3, img.height // 2
    x = np.asarray(img.crop(((i % 3) * tw, (i // 3) * th, (i % 3 + 1) * tw, (i // 3 + 1) * th))).astype(np.float32)
    a = np.clip((255 - x.min(axis=2)) / 255 * 1.5, 0, 1)
    col = 255 - (255 - x) / np.maximum(a[..., None], 1e-3)
    return np.clip(col, 0, 255), a


@lru_cache(None)
def tile(name):
    col, a = tile_rgba(name)
    return to_surface(Image.fromarray(np.dstack([col, a * 255]).astype(np.uint8), 'RGBA'))


def _draw_plan():
    """Ink strokes appear by a time map (top-down with a wobble); pale fills wash in afterwards."""
    col, a = tile_rgba('coffee')
    lum = col.mean(axis=2)
    ink = (a > 0.35) & (lum < 140)
    h, w = a.shape
    ys, xs = np.nonzero(a > 0.05)
    y0, y1 = ys.min(), ys.max()
    noise = np.asarray(Image.fromarray((np.random.default_rng(5).random((6, 6)) * 255).astype(np.uint8))
                       .resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    yy = np.clip((np.arange(h)[:, None] - y0) / (y1 - y0), 0, 1)
    tmap = 0.6 * yy + 0.4 * noise
    tmap = (tmap - tmap[ink].min()) / (tmap[ink].max() - tmap[ink].min())
    # pen position: centroid of the strokes being drawn at each moment
    pen = []
    for r in np.linspace(0, 1, 61):
        m = ink & (np.abs(tmap - r) < 0.035)
        pen.append((xs.mean(), ys.mean()) if not m.any() else (np.nonzero(m)[1].mean(), np.nonzero(m)[0].mean()))
    return col, a, ink, tmap, pen


PLAN = None


def drawing_surface(u_ink, u_tint):
    col, a, ink, tmap, _ = PLAN
    k_ink = np.clip((u_ink * 1.08 - tmap) / 0.08, 0, 1)
    wash = np.clip((u_tint * 1.4 - (1 - tmap) * 0.4), 0, 1)
    alpha = a * np.where(ink, k_ink, wash)
    return to_surface(Image.fromarray(np.dstack([col, alpha * 255]).astype(np.uint8), 'RGBA'))


def pen_point(u):
    pen = PLAN[4]
    f = clamp(u) * (len(pen) - 1)
    i = min(int(f), len(pen) - 2)
    k = f - i
    return lerp(pen[i][0], pen[i + 1][0], k), lerp(pen[i][1], pen[i + 1][1], k)


# ---------- camera / background ----------
def camera(t):
    for (t0, y0, z0), (t1, y1, z1) in zip(CAMERA, CAMERA[1:]):
        if t0 <= t <= t1:
            u = ease_io(prog(t, t0, t1))
            return lerp(y0, y1, u), math.exp(lerp(math.log(z0), math.log(z1), u))
    return CAMERA[-1][1:]


rng = np.random.default_rng(11)
BLOBS = [(float(x), float(y), float(r)) for x, y, r in zip(rng.uniform(-700, 700, 30), rng.uniform(-900, 11000, 30),
                                                           rng.uniform(180, 420, 30))]
SHARDS = [(math.radians(a), s, sz, c) for a, s, sz, c in zip(rng.uniform(190, 350, 18), rng.uniform(800, 1500, 18),
                                                              rng.uniform(10, 24, 18),
                                                              rng.choice([BRAND_C, '#a9c3d9', PINK, PRIMARY], 18))]


def background(ctx, cam, W, H, S):
    ctx.set_source_rgba(*rgb(PAPER))
    ctx.paint()
    cy, z = cam
    for bx, by, r in BLOBS:  # far layer, slower parallax
        sx = W / 2 + bx * z * S * 0.8
        sy = H / 2 + (by - cy) * 0.55 * z * S * 0.8
        rr = r * S * z
        if sy < -rr or sy > H + rr:
            continue
        g = cairo.RadialGradient(sx, sy, 0, sx, sy, rr)
        g.add_color_stop_rgba(0, *rgb(SOFT, 0.85))
        g.add_color_stop_rgba(1, *rgb(SOFT, 0))
        ctx.set_source(g)
        ctx.arc(sx, sy, rr, 0, 2 * math.pi)
        ctx.fill()


def headline(ctx, y, parts1, parts2, t, beats, out=None, size=76):
    """Two-line type beat above a station; each line rises in on its own beat."""
    gone = 1 - prog(t, out, out + 0.3) if out else 1
    k1 = ease_out(prog(t, beats[0], beats[0] + 0.5)) * gone
    k2 = ease_out(prog(t, beats[1], beats[1] + 0.5)) * gone
    draw_parts(ctx, parts1, 0, y + (1 - k1) * 26, size, k1)
    draw_parts(ctx, parts2, 0, y + 104 + (1 - k2) * 26, size, k2)


# ---------- S0 hook ----------
LINE_A_Y = S0 + 380
SEG_A = [(-380, LINE_A_Y), (380, LINE_A_Y)]


def scene_hook(ctx, t):
    mimi = image('artist.png')
    if t < HOOK_LAND:
        u = t / HOOK_LAND
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(16):  # speed lines
            ang = i / 16 * 2 * math.pi + 0.2
            r0, r1 = lerp(100, 600, u), lerp(260, 1100, u)
            ctx.move_to(math.cos(ang) * r0, -80 + math.sin(ang) * r0)
            ctx.line_to(math.cos(ang) * r1, -80 + math.sin(ang) * r1)
            ctx.set_line_width(6)
            ctx.set_source_rgba(*rgb('#bcd3e6', 0.7 * (1 - u)))
            ctx.stroke()
        draw_image(ctx, mimi, 0, lerp(-200, 420, u ** 2), lerp(40, 980, u ** 2.2), 'b', 0.9, 1.14, 0, clamp(u * 3))
    elif t < MIMI_HOP[1] + 0.1:
        sq = spring(t, HOOK_LAND, 0.26, 2.4, 6.5)
        shrink = ease_io(prog(t, 0.38, 0.95))
        hgt, yb = lerp(980, 520, shrink), lerp(420, 190, shrink)
        x, rot = 0.0, 0.0
        if t > MIMI_HOP[0]:  # anticipation, then a hop out to the right
            a = prog(t, MIMI_HOP[0], MIMI_HOP[0] + 0.12)
            j = prog(t, MIMI_HOP[0] + 0.12, MIMI_HOP[1])
            sq += 0.10 * math.sin(math.pi * a) if j == 0 else 0
            yb -= 900 * ease_in(j) - 160 * math.sin(math.pi * min(j * 1.6, 1))
            x += 620 * j
            rot = 0.25 * j
        if t < 0.95:
            d = t - HOOK_LAND
            for ang, spd, size, col in SHARDS:
                ctx.save()
                ctx.translate(math.cos(ang) * spd * d, 380 + math.sin(ang) * spd * d + 1600 * d * d)
                ctx.rotate(ang * 3 + d * 8)
                round_rect(ctx, -size / 2, -size / 2, size, size, size * 0.35)
                ctx.set_source_rgba(*rgb(col, clamp(1 - d / 0.75)))
                ctx.fill()
                ctx.restore()
        draw_image(ctx, mimi, x, yb, hgt, 'b', 1 + sq * 0.75, 1 - sq, rot)
    gone = 1 - prog(t, MOVE1[1], MOVE1[1] + 0.1)
    k = ease_out(prog(t, QUESTION_IN, QUESTION_IN + 0.45)) * gone
    draw_parts(ctx, [('今日', BRAND_C), ('、どんな一日だった？', INK)], 0, S0 + 290 + (1 - k) * 26, 76, k)
    p = ease_back(prog(t, TITLE_IN, TITLE_IN + 0.35)) * gone
    if p > 0:
        ctx.save()
        ctx.translate(0, S0 - 520)
        ctx.scale(p, p)
        pill(ctx, 0, 0, '英語日記', 52, PRIMARY, '#ffffff', clamp(p), pad=(44, 18))
        ctx.restore()
    draw_line(ctx, SEG_A, ease_io(prog(t, *LINE_A)), head=t < LINE_A[1])


# ---------- S1 record ----------
MIC = (0, S1 - 150)
MIC_R = 100
WAVE_Y = S1 + 40
WAVE_X = 430
TRANS_C = (0, S1 + 270, 940, 250)
SEG_B = bezier((380, LINE_A_Y), (540, S0 + 1000), (520, MIC[1]), (MIC_R + 6, MIC[1]), 120)
WORDS = 'Today I go to a small café after work.'.split()
WORD_T = [REC[0] + 0.2 + i * 0.27 for i in range(len(WORDS))]
BARS = 44


def speech_env(n, seed):
    r = np.random.default_rng(seed)
    v = np.abs(np.sin(np.linspace(0, 9.5 * math.pi, n))) * r.uniform(0.5, 1.0, n) + r.uniform(0, 0.15, n)
    return np.clip(v / v.max(), 0.08, 1) ** 0.8


ENV = speech_env(BARS, 4)


def mic_glyph(ctx, x, y, s, color):
    ctx.set_source_rgba(*rgb(color))
    round_rect(ctx, x - 17 * s, y - 44 * s, 34 * s, 62 * s, 17 * s)
    ctx.fill()
    ctx.set_line_width(7 * s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.arc(x, y - 6 * s, 32 * s, 0.15 * math.pi, 0.85 * math.pi)
    ctx.stroke()
    ctx.move_to(x, y + 26 * s)
    ctx.line_to(x, y + 44 * s)
    ctx.stroke()


def wrap_words(words, size, max_w, weight='m'):
    """Greedy line break; returns [(word, x, line)] with lines centred on 0."""
    gap = size * 0.3
    lines, cur, cur_w = [], [], 0
    for w in words:
        ww = text_width(w, size, weight)
        if cur and cur_w + gap + ww > max_w:
            lines.append((cur, cur_w))
            cur, cur_w = [], 0
        cur_w += (gap if cur else 0) + ww
        cur.append((w, ww))
    lines.append((cur, cur_w))
    out = []
    for li, (ws, lw) in enumerate(lines):
        x = -lw / 2
        for w, ww in ws:
            out.append((w, x, li))
            x += ww + gap
    return out


def scene_record(ctx, t):
    if t < MOVE1[0] - 0.1 or t > MOVE2[1] + 0.2:
        if t > MOVE2[1]:
            draw_line(ctx, SEG_B, 1, head=False)
        return
    draw_line(ctx, SEG_B, ease_io(prog(t, MOVE1[0], MOVE1[1])))
    headline(ctx, S1 - 600, [('今日のこと', INK), ('を話すだけ。', INK)], [('それが', INK), ('英語日記', BRAND_C), ('に。', INK)],
             t, H1)
    # microphone lights up when the line arrives, then breathes while recording
    on = ease_back(prog(t, MIC_ON - 0.05, MIC_ON + 0.3))
    rec = REC[0] <= t <= REC[1]
    if rec:
        for k in range(3):
            ph = ((t - REC[0]) / 1.2 + k / 3) % 1
            ctx.arc(*MIC, MIC_R + 10 + 90 * ph, 0, 2 * math.pi)
            ctx.set_source_rgba(*rgb(BRAND_C, 0.35 * (1 - ph)))
            ctx.set_line_width(4)
            ctx.stroke()
    r = MIC_R * lerp(0.92, 1.0, on) * (1 + (0.04 * math.sin((t - REC[0]) * 9) if rec else 0))
    ctx.arc(*MIC, r + 8, 0, 2 * math.pi)
    ctx.set_source_rgba(*rgb('#ffffff'))
    ctx.fill_preserve()
    ctx.set_source_rgba(*rgb(LINE_SOFT))
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.arc(*MIC, r * clamp(on), 0, 2 * math.pi)
    ctx.set_source_rgba(*rgb(PRIMARY))
    ctx.fill()
    mic_glyph(ctx, MIC[0], MIC[1] + 4, 1.15, '#ffffff' if on > 0.5 else LINE_SOFT)
    # elapsed time beside the mic
    secs = int(12 * prog(t, *REC))
    a = clamp(prog(t, REC[0] - 0.2, REC[0]))
    if a > 0:
        ctx.arc(MIC_R + 70, MIC[1], 9, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb(PINK, a * (0.5 + 0.5 * (math.sin(t * 8) > 0) if rec else a)))
        ctx.fill()
        draw_text(ctx, f'0:{secs:02d}', MIC_R + 95, MIC[1], 40, 'm', MUTED, a, 'l')
    # the line becomes the voice: bars spread outward from under the mic
    u = ease_out(prog(t, REC[0], REC[1]))
    if u > 0:
        stem = ease_out(prog(t, REC[0] - 0.2, REC[0] + 0.1))
        draw_line(ctx, [(0, MIC[1] + MIC_R + 8), (0, WAVE_Y)], stem, width=5, head=False)
        draw_line(ctx, [(0, WAVE_Y), (WAVE_X, WAVE_Y)], u, width=5, head=False)
        draw_line(ctx, [(0, WAVE_Y), (-WAVE_X, WAVE_Y)], u, width=5, head=False)
        half = BARS // 2
        gap = WAVE_X / half
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(half):
            d = gap * (i + 0.5)
            if d > WAVE_X * u:
                break
            live = rec and d > WAVE_X * u - 140
            wob = 0.75 + 0.25 * math.sin(t * 17 + i * 1.7) if live else 1
            pop = ease_back(clamp((WAVE_X * u - d) / 60))
            for side, env in ((1, ENV[half + i]), (-1, ENV[half - 1 - i])):
                hh = max(4, env * 70 * pop * wob)
                ctx.set_line_width(gap * 0.5)
                ctx.set_source_rgba(*rgb(PRIMARY))
                ctx.move_to(side * d, WAVE_Y - hh)
                ctx.line_to(side * d, WAVE_Y + hh)
                ctx.stroke()
    # transcript card fills in word by word
    cx, cy, cw, ch = TRANS_C
    rise = ease_back(prog(t, REC[0] - 0.1, REC[0] + 0.35), 1.2)
    if rise > 0:
        card(ctx, cx, cy + (1 - rise) * 60, cw, ch, clamp(rise * 2), 36)
        draw_text(ctx, '話した内容', cx - cw / 2 + 44, cy - 72 + (1 - rise) * 60, 30, 'b', BRAND_C, clamp(rise * 2), 'l')
        for (w, x, li), wt in zip(wrap_words(WORDS, 54, cw - 220), WORD_T):
            k = ease_out(prog(t, wt, wt + 0.22))
            draw_text(ctx, w, x, cy + li * 72 + (1 - k) * 14, 54, 'm', INK, k, 'l')


# ---------- S2 corrected journal ----------
CARD2 = (0, S2 + 60, 960, 760)
SEG_C = bezier((WAVE_X, WAVE_Y), (560, WAVE_Y + 500), (560, S2 - 500), (CARD2[2] / 2 - 30, CARD2[1] - CARD2[3] / 2 + 60), 120)
SCORE_ITEMS = [('内容', 78), ('文法', 72), ('語彙', 80), ('発音', 76), ('流暢さ', 79)]


def corrected_line(ctx, t, x0, y, alpha):
    """'Today I go to a small café' where 'go' is struck out and 'went' takes its place."""
    size, gap = 54, 16
    s = ease_io(prog(t, WENT, WENT + 0.35))
    parts = ['Today', 'I', None, 'to', 'a', 'small', 'café']
    go_w, went_w = text_width('go', size, 'm'), text_width('went', size, 'b')
    widths = [text_width(p, size, 'm') if p else lerp(go_w, went_w, s) for p in parts]
    x = x0 - (sum(widths) + gap * (len(parts) - 1)) / 2
    for p, w in zip(parts, widths):
        if p:
            draw_text(ctx, p, x, y, size, 'm', INK, alpha, 'l')
        else:
            k = ease_out(prog(t, STRIKE, STRIKE + 0.25))
            draw_text(ctx, 'go', x, y - 52 * s, size * lerp(1, 0.62, s), 'm', PINK if k > 0 else INK, alpha, 'l')
            if k > 0:
                gw = go_w * lerp(1, 0.62, s)
                ctx.move_to(x - 4, y - 52 * s)
                ctx.line_to(x - 4 + (gw + 8) * k, y - 52 * s)
                ctx.set_source_rgba(*rgb(PINK, alpha))
                ctx.set_line_width(5)
                ctx.stroke()
            if s > 0:
                round_rect(ctx, x - 8, y - 36, went_w + 16, 72, 14)
                ctx.set_source_rgba(*rgb(SOFT, alpha * s))
                ctx.fill()
                draw_text(ctx, 'went', x + went_w / 2, y, size, 'b', BRAND_C, alpha * clamp(s * 2), 'c',
                          ease_back(s, 2.2))
        x += w + gap


def scene_feedback(ctx, t):
    if t < MOVE2[0] - 0.1:
        return
    if t > MOVE3[1] + 0.2:
        draw_line(ctx, SEG_C, 1, head=False)
        return
    draw_line(ctx, SEG_C, ease_io(prog(t, MOVE2[0], MOVE2[1] - 0.05)))
    headline(ctx, S2 - 610, [('自然な英語', BRAND_C), ('に直して、', INK)], [('発音', BRAND_C), ('のアドバイスも。', INK)], t, H2)
    cx, cy, cw, ch = CARD2
    r = ease_back(prog(t, *CARD2_IN), 1.2)
    if r <= 0:
        return
    a = clamp(r * 2)
    ctx.save()
    ctx.translate(cx, cy + (1 - r) * 80)
    ctx.scale(lerp(0.94, 1, r), lerp(0.94, 1, r))
    ctx.translate(-cx, -cy)
    left, top = cx - cw / 2 + 48, cy - ch / 2
    card(ctx, cx, cy, cw, ch, a, 40)
    pill(ctx, cx + cw / 2 - 100, top + 62, 'デモ表示', 24, '#eef2f5', MUTED, a * 0.9, pad=(18, 8), weight='m')
    draw_text(ctx, '自然な表現に直した日記', left, top + 62, 32, 'b', BRAND_C, a, 'l')
    corrected_line(ctx, t, cx, top + 175, a)
    draw_text(ctx, 'after work.', cx, top + 255, 54, 'm', INK, a)
    k = ease_out(prog(t, WENT + 0.25, WENT + 0.6))
    draw_text(ctx, '今日すでに起きた出来事なので went を使います。', cx, top + 335 + (1 - k) * 12, 30, 'm', MUTED, k)
    ctx.move_to(left, top + 395)
    ctx.line_to(cx + cw / 2 - 48, top + 395)
    ctx.set_source_rgba(*rgb('#e2eaf0', a))
    ctx.set_line_width(2)
    ctx.stroke()
    # five score chips pop in one after another and count up
    chip_w, chip_g = 162, 12
    x = cx - (5 * chip_w + 4 * chip_g) / 2
    for i, (label, score) in enumerate(SCORE_ITEMS):
        t0 = SCORES + i * SCORE_GAP
        p = ease_back(prog(t, t0, t0 + 0.3), 2.0)
        if p > 0:
            ccx, ccy = x + chip_w / 2, top + 510
            ctx.save()
            ctx.translate(ccx, ccy)
            ctx.scale(p, p)
            hi = label == '発音' and t > TIP
            round_rect(ctx, -chip_w / 2, -70, chip_w, 140, 26)
            ctx.set_source_rgba(*rgb(PRIMARY if hi else SOFT, clamp(p)))
            ctx.fill()
            draw_text(ctx, label, 0, -34, 28, 'b', '#ffffff' if hi else MUTED, clamp(p))
            n = round(score * ease_out(prog(t, t0, t0 + 0.6)))
            draw_text(ctx, str(n), 0, 22, 60, 'b', '#ffffff' if hi else PRIMARY, clamp(p))
            ctx.restore()
        x += chip_w + chip_g
    k = ease_out(prog(t, TIP, TIP + 0.4))
    draw_text(ctx, '“by the window”', left, top + 648 + (1 - k) * 14, 40, 'm', PRIMARY, k, 'l')
    draw_text(ctx, 'まとまりを意識して発音できています。', left, top + 705 + (1 - k) * 14, 30, 'm', MUTED, k, 'l')
    ctx.restore()
    m = ease_back(prog(t, TIP - 0.1, TIP + 0.25)) * (1 - prog(t, MOVE3[0], MOVE3[0] + 0.3))
    draw_image(ctx, image('success.png'), cx + cw / 2 - 30, top + 30, 190 * m, 'b', 1, 1, 0.08)


# ---------- S3 illustration ----------
FRAME = (0, S3 - 50, 740)
ART_H = 660
SEG_D = bezier((CARD2[2] / 2 - 30, CARD2[1] + CARD2[3] / 2 - 60), (580, S2 + 900), (560, S3 - 600),
               (FRAME[2] / 2 - 20, FRAME[1] - 200), 120)


def art_origin():
    """Top-left of the 700 px art inside the frame, and px-per-tile-pixel."""
    k = ART_H / PLAN[1].shape[0]
    return FRAME[0] - ART_H / 2, FRAME[1] - ART_H / 2, k


def scene_draw(ctx, t):
    if t < MOVE3[0] - 0.1:
        return
    if t > MOVE4[1] + 0.2:
        draw_line(ctx, SEG_D, 1, head=False)
        return
    draw_line(ctx, SEG_D, ease_io(prog(t, MOVE3[0], MOVE3[1])), head=t < DRAW[0] + 0.1)
    headline(ctx, S3 - 650, [('その日が、', INK)], [('Mimi', BRAND_C), ('の絵になる。', INK)], t, H3, out=MOVE4[0])
    fx, fy, fs = FRAME
    fly = ease_io(prog(t, *MOVE4))
    fa = 1 - prog(t, MOVE4[0], MOVE4[0] + 0.35)
    r = ease_back(prog(t, MOVE3[1] - 0.25, MOVE3[1] + 0.15), 1.1)
    card(ctx, fx, fy, fs * lerp(0.9, 1, r), fs * lerp(0.9, 1, r), clamp(r * 2) * fa, 48)
    if fly == 0:
        u_ink = ease_io(prog(t, *DRAW))
        u_tint = ease_out(prog(t, *TINT))
        if u_ink > 0:
            draw_image(ctx, drawing_surface(u_ink, u_tint), fx, fy, ART_H)
        if 0 < u_ink < 1:
            x0, y0, k = art_origin()
            px, py = pen_point(u_ink)
            glow_dot(ctx, (x0 + px * k, y0 + py * k), 9)
    # Mimi the artist and the caption from the app
    m = ease_back(prog(t, MIMI_ART, MIMI_ART + 0.35)) * fa
    bob = 10 * math.sin((t - MIMI_ART) * 6) if t < DRAW[1] else 0
    draw_image(ctx, image('artist.png'), -300, fy + fs / 2 + 150 - bob, 330 * m, 'b', 1, 1, -0.06)
    c = ease_back(prog(t, CAPTION, CAPTION + 0.35), 1.4) * fa
    if c > 0:
        label = '仕事帰りにカフェでほっと一息。'
        w = text_width(label, 36, 'm') + 64
        bx, by = 120, fy + fs / 2 + 75
        ctx.save()
        ctx.translate(bx - w / 2, by)
        ctx.scale(c, c)
        round_rect(ctx, 0, -42, w, 84, 42)
        ctx.move_to(4, -10)
        ctx.line_to(-26, 6)
        ctx.line_to(20, 22)
        ctx.close_path()
        ctx.set_source_rgba(*rgb(PRIMARY, clamp(c)))
        ctx.fill()
        draw_text(ctx, label, w / 2, 0, 36, 'm', '#ffffff', clamp(c))
        ctx.restore()


# ---------- S4 calendar ----------
CAL = (0, S4 + 30, 1000, 900)
COLS, ROW_H = 7, 138
FIRST_WD = 4      # 2026-10-01 is a Thursday; weeks start on Sunday
TODAY = 20
ENTRIES = {9: 'trees', 11: 'ramen', 13: 'book', 15: 'trees', 16: 'laptop', 17: 'ramen', 18: 'book', 19: 'shoes'}
PAST_ORDER = sorted(ENTRIES)
SEG_E = bezier((FRAME[2] / 2 - 20, FRAME[1] + 200), (580, S3 + 900), (580, S4 - 600), (CAL[2] / 2 - 10, CAL[1] - 300), 120)
SEG_F = bezier((-CAL[2] / 2 + 10, CAL[1] + 380), (-580, S4 + 1000), (-560, S5 - 200), (-380, S5 + 10), 120)


def cell(day):
    i = FIRST_WD + day - 1
    cw = (CAL[2] - 40) / COLS
    x = CAL[0] - CAL[2] / 2 + 20 + cw * (i % 7 + 0.5)
    y = CAL[1] - CAL[3] / 2 + 230 + ROW_H * (i // 7)
    return x, y, cw


def scene_calendar(ctx, t):
    if t < MOVE4[0] - 0.1:
        return
    if t > MOVE5[1] + 0.2:
        draw_line(ctx, SEG_F, 1, head=False)
        return
    draw_line(ctx, SEG_E, ease_io(prog(t, MOVE4[0], MOVE4[1])), head=False)
    headline(ctx, S4 - 660, [('声で残した日々', INK), ('が、', INK)], [('カレンダー', BRAND_C), ('に並ぶ。', INK)], t, H4)
    cx, cy, cw, ch = CAL
    r = ease_back(prog(t, MOVE4[0] + 0.2, MOVE4[0] + 0.6), 1.1)
    a = clamp(r * 2)
    card(ctx, cx, cy + (1 - r) * 80, cw, ch, a, 44)
    top = cy - ch / 2 + (1 - r) * 80
    draw_text(ctx, '2026年10月', cx - cw / 2 + 48, top + 70, 42, 'b', INK, a, 'l')
    draw_text(ctx, '‹   ›', cx + cw / 2 - 48, top + 70, 42, 'm', MUTED, a, 'r')
    for i, wd in enumerate('日月火水木金土'):
        x, _, _ = cell(1 + i - FIRST_WD)
        draw_text(ctx, wd, x, top + 150, 28, 'm', MUTED, a)
    for day in range(1, 32):
        x, y, w = cell(day)
        y += (1 - r) * 80
        today = day == TODAY
        land = ease_back(prog(t, CELL_LAND, CELL_LAND + 0.3), 2.0)
        if today and land > 0:  # selected-day ring
            round_rect(ctx, x - w / 2 + 4, y - 20, w - 8, ROW_H - 6, 22)
            ctx.set_source_rgba(*rgb(BRAND_C, clamp(land)))
            ctx.set_line_width(4)
            ctx.stroke()
        col = BRAND_C if today else ('#b8c3cc' if day > TODAY else INK)
        draw_text(ctx, str(day), x - w / 2 + 16, y, 30, 'b', col, a, 'l')
        if day in ENTRIES:
            j = PAST_ORDER.index(day)
            p = ease_back(prog(t, PAST + j * PAST_GAP, PAST + j * PAST_GAP + 0.3), 2.0)
            draw_image(ctx, tile(ENTRIES[day]), x, y + 62, 104 * p)
    # today's picture flies in from the frame above and lands with a bump
    fly = ease_io(prog(t, *MOVE4))
    if t >= MOVE4[0]:
        x1, y1, _ = cell(TODAY)
        y1 += 62
        x0, y0 = FRAME[0], FRAME[1]
        arc = -120 * math.sin(math.pi * fly)
        h = math.exp(lerp(math.log(ART_H), math.log(104), fly))
        bump = 1 + spring(t, CELL_LAND, 0.25, 2.6, 7)
        draw_image(ctx, tile('coffee'), lerp(x0, x1, fly) + arc, lerp(y0, y1, fly), h * bump)
        burst = prog(t, CELL_LAND, CELL_LAND + 0.5)
        if 0 < burst < 1:
            ctx.arc(x1, y1, 60 + 70 * ease_out(burst), 0, 2 * math.pi)
            ctx.set_source_rgba(*rgb(BRAND_C, 0.6 * (1 - burst)))
            ctx.set_line_width(5)
            ctx.stroke()
    draw_line(ctx, SEG_F, ease_io(prog(t, MOVE5[0], MOVE5[1] - 0.05)), head=False)


# ---------- S5 lock-up ----------
LOCK_Y = S5 - 90
UNDER = [(-380, S5 + 10), (380, S5 + 10)]


def scene_final(ctx, t):
    if t < MOVE5[0]:
        return
    u = ease_io(prog(t, *LOGO_LINE))
    tip = draw_line(ctx, UNDER, u)
    if u > 0:
        lockup(ctx, 0, LOCK_Y, reveal_x=tip[0] + 30 if u < 1 else None)
    if t > MIMI_LAND - 0.35:  # Mimi drops in above the lock-up, then a happy hop on the fanfare
        f = prog(t, MIMI_LAND - 0.35, MIMI_LAND)
        yb = lerp(S5 - 1200, S5 - 230, ease_in(f))
        sq = spring(t, MIMI_LAND, 0.24, 2.6, 7)
        sx, sy = (0.9, 1.12) if f < 1 else (1 + sq * 0.75, 1 - sq)
        yb -= 70 * math.sin(math.pi * prog(t, FANFARE, FANFARE + 0.45))
        draw_image(ctx, image('artist.png'), 0, yb, 380, 'b', sx, sy)
    k = ease_out(prog(t, TAGLINE, TAGLINE + 0.5))
    draw_parts(ctx, [('今日', BRAND_C), ('を、英語で残そう。', INK)], 0, S5 + 140 + (1 - k) * 26, 72, k)
    e = ease_out(prog(t, END_CARD, END_CARD + 0.6))
    if e > 0:
        by = S5 + 290 + (1 - e) * 30
        w = text_width('7日間無料ではじめる', 42) + 90
        round_rect(ctx, -w / 2 - 150, by - 48, w, 96, 48)
        ctx.set_source_rgba(*rgb(PRIMARY, e))
        ctx.fill()
        draw_text(ctx, '7日間無料ではじめる', -150, by, 42, 'b', '#ffffff', e)
        draw_image(ctx, image('appstore.png'), w / 2 - 150 + 150, by, 96, alpha=e)
        draw_text(ctx, 'lanclo.app', 0, by + 110, 34, 'm', MUTED, e)


SCENES = [scene_hook, scene_record, scene_feedback, scene_draw, scene_calendar, scene_final]


def shake(t):
    out = [0.0, 0.0]
    for t0, amp in ((HOOK_LAND, 24), (CELL_LAND, 6), (MIMI_LAND, 12)):
        d = t - t0
        if 0 <= d < 0.5:
            k = amp * math.exp(-9 * d)
            out[0] += k * math.sin(d * 71)
            out[1] += k * math.cos(d * 59)
    return out


def wrap(s, size, max_w):
    lines, cur = [], ''
    for w in s.split():
        nxt = f'{cur} {w}'.strip()
        if cur and text_width(nxt, size, 'm') > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = nxt
    return lines + [cur]


def subtitles(ctx, t, W, H, S):
    """English translation of the on-screen type, in screen space above the SNS UI zone."""
    for (t0, t1), s in SUBS:
        a = min(prog(t, t0 + 0.15, t0 + 0.35), 1 - prog(t, t1 - 0.2, t1)) if t1 < DURATION else prog(t, t0 + 0.15,
                                                                                                    t0 + 0.35)
        if a <= 0:
            continue
        ctx.save()
        ctx.scale(S, S)
        size, lh = 38, 54
        lines = wrap(s, size, 860)
        w = max(text_width(l, size, 'm') for l in lines) + 60
        h = lh * len(lines) + 24
        y = H / S - 400
        round_rect(ctx, W / S / 2 - w / 2, y - h / 2, w, h, min(34, h / 2))
        ctx.set_source_rgba(*rgb('#ffffff', 0.85 * a))
        ctx.fill()
        for i, l in enumerate(lines):
            draw_text(ctx, l, W / S / 2, y + (i - (len(lines) - 1) / 2) * lh, size, 'm', INK, a)
        ctx.restore()


GRAIN = None


def frame(t, W, H, S):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    cam = camera(t)
    background(ctx, cam, W, H, S)
    cy, z = cam
    dx, dy = shake(t)
    ctx.translate(W / 2 + dx * S, H / 2 + dy * S)
    ctx.scale(z * S, z * S)
    ctx.translate(0, -cy)
    for s in SCENES:
        s(ctx, t)
    ctx.identity_matrix()
    subtitles(ctx, t, W, H, S)
    surf.flush()
    stride = surf.get_stride()
    arr = np.ndarray((H, stride // 4, 4), np.uint8, surf.get_data())[:, :W]
    g = GRAIN[int(t * 24) % len(GRAIN)]
    out = np.clip(arr[..., :3].astype(np.int16) + g[..., None], 0, 255).astype(np.uint8)
    return np.dstack([out, arr[..., 3:]])


def main():
    global GRAIN, PLAN
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--fps', type=int, default=FPS)
    ap.add_argument('--from', dest='t0', type=float, default=0.0)
    ap.add_argument('--to', dest='t1', type=float, default=DURATION)
    ap.add_argument('--still', default='')
    ap.add_argument('--audio', default='')
    a = ap.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    W, H = int(W0 * a.scale) // 2 * 2, int(H0 * a.scale) // 2 * 2
    GRAIN = [np.random.default_rng(i).integers(-3, 4, (H, W)).astype(np.int16) for i in range(6)]
    PLAN = _draw_plan()
    if a.still:
        for ts in a.still.split(','):
            img = frame(float(ts), W, H, a.scale)
            Image.fromarray(img[..., [2, 1, 0]]).save(f'{a.out}-{float(ts):05.2f}.png')
        return
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(a.fps), '-i', '-']
    if a.audio:
        cmd += ['-ss', str(a.t0), '-i', a.audio, '-c:a', 'aac', '-b:a', '256k', '-shortest']
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', '-movflags', '+faststart', a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(round(a.t0 * a.fps), round(a.t1 * a.fps)):
        p.stdin.write(frame(n / a.fps, W, H, a.scale).tobytes())
        if n % (a.fps * 2) == 0:
            print(f'{n / a.fps:5.1f}s', file=sys.stderr, flush=True)
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    main()
