"""Render the Lanclo "One line" promo frame by frame (cairo) and pipe to ffmpeg.

usage: render.py OUT.mp4 [--scale 0.5] [--fps 30] [--from 0 --to 26.6] [--still T,T,...]
"""
import argparse
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cairo
import numpy as np
from PIL import Image, ImageFont, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from timeline import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'assets'
W0, H0 = 1920, 1080

# Lanclo palette (DESIGN.md)
PAPER = '#fbfcfd'
SOFT = '#eaf1f6'
INK = '#273b4b'
PRIMARY = '#344f69'
BRAND_C = '#5b7f9f'
MUTED = '#596875'
LINE_SOFT = '#ccd8df'
OWN = '#9fb0bd'
PINK = '#f4a9b8'


def rgb(h, a=1.0):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def ease_io(u):
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def ease_out(u):
    return 1 - (1 - u) ** 3


def ease_in(u):
    return u ** 3


def ease_back(u, s=1.6):
    u -= 1
    return 1 + (s + 1) * u ** 3 + s * u ** 2


def spring(t, t0, amp, freq=2.6, decay=7.0):
    if t < t0:
        return 0.0
    d = t - t0
    return amp * math.exp(-decay * d) * math.cos(2 * math.pi * freq * d)


def lerp(a, b, u):
    return a + (b - a) * u


# ---------- assets ----------
_KEEP = []


def to_surface(img):
    img = img.convert('RGBA')
    arr = np.asarray(img).astype(np.float32)
    a = arr[..., 3:4] / 255.0
    bgra = np.empty_like(arr)
    bgra[..., 0] = arr[..., 2] * a[..., 0]
    bgra[..., 1] = arr[..., 1] * a[..., 0]
    bgra[..., 2] = arr[..., 0] * a[..., 0]
    bgra[..., 3] = arr[..., 3]
    h, w = arr.shape[:2]
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
    buf = np.zeros((h, stride // 4, 4), np.uint8)
    buf[:, :w] = bgra.astype(np.uint8)
    surf = cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, stride)
    _KEEP.append(buf)  # cairo does not own the pixel buffer
    return surf


@lru_cache(None)
def image(name, max_px=1400):
    img = Image.open(A / name).convert('RGBA')
    if max(img.size) > max_px:
        img.thumbnail((max_px, max_px), Image.LANCZOS)
    return to_surface(img)


@lru_cache(None)
def circle_photo(name, px=480):
    img = Image.open(A / name).convert('RGB').resize((px, px), Image.LANCZOS)
    mask = Image.new('L', (px * 4, px * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, px * 4 - 1, px * 4 - 1), fill=255)
    out = img.convert('RGBA')
    out.putalpha(mask.resize((px, px), Image.LANCZOS))
    return to_surface(out)


FONTS = {'r': 'fonts/ZenMaruGothic-Regular.ttf', 'm': 'fonts/ZenMaruGothic-Medium.ttf', 'b': 'fonts/ZenMaruGothic-Bold.ttf'}
TEXT_OVERSAMPLE = 2.2


@lru_cache(None)
def text(s, size, weight='b', color=INK):
    font = ImageFont.truetype(str(A / FONTS[weight]), int(size * TEXT_OVERSAMPLE))
    asc, desc = font.getmetrics()
    x0, _, x1, _ = font.getbbox(s)
    w, h = x1 - x0 + 8, asc + desc + 8
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((4 - x0, 4), s, font=font, fill=color)
    surf = to_surface(img)
    return surf, w / TEXT_OVERSAMPLE, h / TEXT_OVERSAMPLE


def text_width(s, size, weight='b'):
    return text(s, size, weight)[1]


def draw_text(ctx, s, x, y, size, weight='b', color=INK, alpha=1.0, anchor='c', scale=1.0):
    if alpha <= 0:
        return
    surf, w, h = text(s, size, weight, color)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(scale, scale)
    ox = {'c': -w / 2, 'l': 0, 'r': -w}[anchor]
    ctx.translate(ox, -h / 2)
    ctx.scale(1 / TEXT_OVERSAMPLE, 1 / TEXT_OVERSAMPLE)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(alpha)
    ctx.restore()


def draw_image(ctx, surf, x, y, height, anchor='c', sx=1.0, sy=1.0, rot=0.0, alpha=1.0):
    """anchor 'c' = centre at (x,y); 'b' = bottom-centre at (x,y) (squash pivots on feet)."""
    if alpha <= 0 or height < 1:  # sub-pixel scales make cairo's matrix singular
        return
    w, h = surf.get_width(), surf.get_height()
    k = height / h
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(sx * k, sy * k)
    ctx.translate(-w / 2, -h if anchor == 'b' else -h / 2)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(alpha)
    ctx.restore()


def round_rect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def card(ctx, cx, cy, w, h, alpha=1.0, r=44):
    if alpha <= 0:
        return
    x, y = cx - w / 2, cy - h / 2
    for i in range(6):  # soft shadow from stacked translucent shapes
        g = 6 + i * 7
        round_rect(ctx, x - g / 2, y - g / 2 + 18, w + g, h + g, r + g / 2)
        ctx.set_source_rgba(*rgb(PRIMARY, 0.018 * alpha))
        ctx.fill()
    round_rect(ctx, x, y, w, h, r)
    ctx.set_source_rgba(*rgb('#ffffff', alpha))
    ctx.fill_preserve()
    ctx.set_source_rgba(*rgb('#e2eaf0', alpha))
    ctx.set_line_width(2)
    ctx.stroke()


def pill(ctx, cx, cy, label, size, bg, fg, alpha=1.0, pad=(30, 14), weight='b'):
    if alpha <= 0:
        return
    w = text_width(label, size, weight) + pad[0] * 2
    h = size * 1.2 + pad[1] * 2
    round_rect(ctx, cx - w / 2, cy - h / 2, w, h, h / 2)
    ctx.set_source_rgba(*rgb(bg, alpha))
    ctx.fill()
    draw_text(ctx, label, cx, cy, size, weight, fg, alpha)
    return w, h


# ---------- the line ----------
def bezier(p0, p1, p2, p3, n=80):
    out = []
    for i in range(n + 1):
        u = i / n
        a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def partial(pts, u):
    """Prefix of a polyline covering fraction u of its length; returns (points, head)."""
    if u <= 0:
        return [], None
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total, target, acc = sum(seg), sum(seg) * min(u, 1), 0.0
    out = [pts[0]]
    for i, s in enumerate(seg):
        if acc + s >= target:
            k = (target - acc) / s if s else 0
            p = (lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k))
            out.append(p)
            return out, p
        out.append(pts[i + 1])
        acc += s
    return out, pts[-1]


def stroke_path(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)


def draw_line(ctx, pts, u, width=10, color=PRIMARY, alpha=1.0, head=True):
    """The one line. Every station draws through this so it reads as the same light."""
    part, tip = partial(pts, u)
    if len(part) < 2 or alpha <= 0:
        return tip
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for wmul, a in ((4.2, 0.06), (2.4, 0.10)):
        stroke_path(ctx, part)
        ctx.set_line_width(width * wmul)
        ctx.set_source_rgba(*rgb(BRAND_C, a * alpha))
        ctx.stroke()
    stroke_path(ctx, part)
    ctx.set_line_width(width)
    ctx.set_source_rgba(*rgb(color, alpha))
    ctx.stroke()
    if head and u < 1:
        glow_dot(ctx, tip, width, alpha)
    return tip


def glow_dot(ctx, p, width, alpha=1.0):
    g = cairo.RadialGradient(p[0], p[1], 0, p[0], p[1], width * 4)
    g.add_color_stop_rgba(0, *rgb('#ffffff', alpha))
    g.add_color_stop_rgba(0.25, *rgb('#bcd3e6', 0.9 * alpha))
    g.add_color_stop_rgba(1, *rgb(BRAND_C, 0))
    ctx.set_source(g)
    ctx.arc(p[0], p[1], width * 4, 0, 2 * math.pi)
    ctx.fill()


# ---------- audio-derived waveform bars ----------
def envelope(name, length, bars):
    if not (A / name).exists():  # voice clips are not in Git; fall back to a speech-like shape
        v = np.abs(np.sin(np.linspace(0, 8.5 * math.pi, bars))) * np.random.default_rng(len(name)).uniform(0.5, 1, bars)
        return np.clip(v / v.max(), 0.06, 1.0) ** 0.8
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(A / name), '-t', str(length), '-ac', '1', '-ar', '16000',
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    chunks = np.array_split(x, bars)
    v = np.array([np.sqrt(np.mean(c ** 2)) for c in chunks])
    return np.clip(v / (v.max() + 1e-9), 0.06, 1.0) ** 0.8


BARS = 60
ENV_OWN = envelope('voice/own.mp3', OWN_LEN, BARS)
ENV_MODEL = envelope('voice/model.mp3', MODEL_LEN, BARS)
SAMPLE = json.loads((A / 'voice-comparison-sample.json').read_text())
SHOWN_WORDS = 8  # "Could you let me know if you're available"


def draw_wave(ctx, x0, x1, y, env, u, color, alpha=1.0, amp=96, glow=False):
    """Bars appear as the playhead passes; the baseline is the line itself."""
    n = len(env)
    gap = (x1 - x0) / n
    head_x = lerp(x0, x1, clamp(u))
    draw_line(ctx, [(x0, y), (x1, y)], clamp(u), width=5, color=color, alpha=alpha * 0.9, head=False)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, v in enumerate(env):
        bx = x0 + gap * (i + 0.5)
        if bx > head_x:
            break
        pop = ease_back(clamp((head_x - bx) / 70))
        hh = max(4, v * amp * pop)
        if glow:
            ctx.set_line_width(gap * 1.3)
            ctx.set_source_rgba(*rgb(BRAND_C, 0.10 * alpha))
            ctx.move_to(bx, y - hh)
            ctx.line_to(bx, y + hh)
            ctx.stroke()
        ctx.set_line_width(gap * 0.52)
        ctx.set_source_rgba(*rgb(color, alpha))
        ctx.move_to(bx, y - hh)
        ctx.line_to(bx, y + hh)
        ctx.stroke()
    if 0 < u < 1:
        glow_dot(ctx, (head_x, y), 8, alpha)


# ---------- camera ----------
def camera(t):
    for (t0, x0, y0, z0), (t1, x1, y1, z1) in zip(CAMERA, CAMERA[1:]):
        if t0 <= t <= t1:
            u = ease_io(prog(t, t0, t1))
            return lerp(x0, x1, u), lerp(y0, y1, u), math.exp(lerp(math.log(z0), math.log(z1), u))
    return CAMERA[-1][1:]


rng = np.random.default_rng(7)
BLOBS = [(float(x), float(y), float(r)) for x, y, r in zip(rng.uniform(-1500, 8500, 26), rng.uniform(-900, 900, 26),
                                                           rng.uniform(160, 420, 26))]
SHARDS = [(math.radians(a), s, sz, c) for a, s, sz, c in zip(rng.uniform(190, 350, 18), rng.uniform(900, 1700, 18),
                                                              rng.uniform(10, 24, 18),
                                                              rng.choice([BRAND_C, '#a9c3d9', PINK, PRIMARY], 18))]


def background(ctx, t, cam, W, H, S):
    ctx.set_source_rgba(*rgb(PAPER))
    ctx.paint()
    cx, cy, z = cam
    for bx, by, r in BLOBS:  # far layer, slower parallax
        sx = W / 2 + (bx - cx * 0.55) * z * S * 0.8
        sy = H / 2 + (by - cy * 0.55) * z * S * 0.8
        rr = r * S * z
        if sx < -rr or sx > W + rr:
            continue
        g = cairo.RadialGradient(sx, sy, 0, sx, sy, rr)
        g.add_color_stop_rgba(0, *rgb(SOFT, 0.85))
        g.add_color_stop_rgba(1, *rgb(SOFT, 0))
        ctx.set_source(g)
        ctx.arc(sx, sy, rr, 0, 2 * math.pi)
        ctx.fill()


# ---------- stations ----------
MARK_H = 150
LOCK_TEXT = 150


def lockup(ctx, cx, cy, reveal_x=None):
    """Approved LC mark + wordmark; revealed left to right by the line head."""
    tw = text_width('Lanclo', LOCK_TEXT, 'r')
    total = MARK_H + 40 + tw
    x0 = cx - total / 2
    ctx.save()
    if reveal_x is not None:
        ctx.rectangle(x0 - 50, cy - 200, reveal_x - x0 + 50, 400)
        ctx.clip()
    draw_image(ctx, image('mark.png'), x0 + MARK_H / 2, cy, MARK_H * 1.05)
    draw_text(ctx, 'Lanclo', x0 + MARK_H + 40, cy - 6, LOCK_TEXT, 'r', INK, anchor='l')
    ctx.restore()
    return x0, x0 + total


def scene_hook(ctx, t):
    mimi = image('master.png')
    # Mimi rushes in from depth, lands big, eases back above the lock-up, hops out.
    if t < HOOK_LAND:
        u = t / HOOK_LAND
        hgt, yb, sx, sy, alpha = lerp(40, 1000, u ** 2.2), lerp(-60, 430, u ** 2), 0.9, 1.14, clamp(u * 3)
        # speed lines
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(16):
            ang = i / 16 * 2 * math.pi + 0.2
            r0, r1 = lerp(100, 700, u), lerp(260, 1200, u)
            ctx.move_to(math.cos(ang) * r0, -40 + math.sin(ang) * r0)
            ctx.line_to(math.cos(ang) * r1, -40 + math.sin(ang) * r1)
            ctx.set_line_width(6)
            ctx.set_source_rgba(*rgb('#bcd3e6', 0.7 * (1 - u)))
            ctx.stroke()
        draw_image(ctx, mimi, 0, yb, hgt, 'b', sx, sy, 0, alpha)
        return
    sq = spring(t, HOOK_LAND, 0.26, 2.4, 6.5)
    shrink = ease_io(prog(t, 0.38, 0.95))
    hgt, yb = lerp(1000, 360, shrink), lerp(430, 10, shrink)
    x, rot, alpha = 0.0, 0.0, 1.0
    if t > MIMI_HOP[0]:  # anticipation, then a hop up and out
        a = prog(t, MIMI_HOP[0], MIMI_HOP[0] + 0.12)
        j = prog(t, MIMI_HOP[0] + 0.12, MIMI_HOP[1])
        sq += 0.10 * math.sin(math.pi * a) if j == 0 else 0
        yb -= 1000 * ease_in(j) - 160 * math.sin(math.pi * min(j * 1.6, 1))
        x += 760 * j
        rot = 0.25 * j
    sx, sy = 1 + sq * 0.75, 1 - sq
    if t < 0.95:  # shards from the landing
        d = t - HOOK_LAND
        for ang, spd, size, col in SHARDS:
            px = math.cos(ang) * spd * d
            py = 380 + math.sin(ang) * spd * d + 1600 * d * d
            a = clamp(1 - d / 0.75)
            ctx.save()
            ctx.translate(px, py)
            ctx.rotate(ang * 3 + d * 8)
            round_rect(ctx, -size / 2, -size / 2, size, size, size * 0.35)
            ctx.set_source_rgba(*rgb(col, a))
            ctx.fill()
            ctx.restore()
    draw_image(ctx, mimi, x, yb, hgt, 'b', sx, sy, rot, alpha)


SEG0 = [(-380, 255), (380, 255)]
T_OUT = 0.0  # output clock, for type that animates during warp holds


def draw_parts(ctx, parts, x, y, size, alpha=1.0, weight='b'):
    """One centred line built from (text, colour) runs."""
    total = sum(text_width(p, size, weight) for p, _ in parts)
    cx = x - total / 2
    for p, col in parts:
        draw_text(ctx, p, cx, y, size, weight, col, alpha, 'l')
        cx += text_width(p, size, weight)


def scene_question(ctx, t):
    k = ease_out(prog(T_OUT, QUESTION[0], QUESTION[0] + 0.5))
    k2 = ease_out(prog(T_OUT, QUESTION[0] + 0.45, QUESTION[0] + 0.95))
    if k <= 0:
        return
    draw_parts(ctx, [('自分の声', BRAND_C), ('で、', INK)], 0, 430 + (1 - k) * 26, 70, k)
    draw_parts(ctx, [('ネイティブの発音', BRAND_C), ('を聴けたら？', INK)], 0, 530 + (1 - k2) * 26, 70, k2)


def scene_logo(ctx, t):
    u = ease_io(prog(t, *LOGO_LINE))
    if u <= 0:
        return
    tip = draw_line(ctx, SEG0, u)
    lockup(ctx, 0, 150, reveal_x=tip[0] + 30 if u < 1 else None)


CARD = (2600, 0, 1400, 660)
ROW_X = (2290, 3240)
ROW1_Y, ROW2_Y = -10, 175
SENT_Y = -205
SEG1 = bezier((380, 255), (1100, 255), (1600, ROW1_Y), (ROW_X[0], ROW1_Y), 120)


def word_spans():
    words = [w['text'] for w in SAMPLE['recorded']['words'][:SHOWN_WORDS]]
    size, gap = 46, 15
    widths = [text_width(w, size, 'm') for w in words]
    total = sum(widths) + gap * (len(words) - 1) + text_width('…', size, 'm') + gap
    x = CARD[0] - total / 2
    spans = []
    for w, wd in zip(words, widths):
        spans.append((w, x, wd))
        x += wd + gap
    return spans, x, size


SPANS, ELLIPSIS_X, SENT_SIZE = word_spans()


def scene_card(ctx, t):
    if t < CARD_IN[0] - 0.2 or t > 11.3:
        draw_line(ctx, SEG1, 1, head=False) if t > 11.3 else None
        return
    cx, cy, cw, ch = CARD
    rise = ease_back(prog(t, *CARD_IN), 1.2)
    fade_out = ease_io(prog(t, MERGE[0], MERGE[1] - 0.2))
    a = clamp(prog(t, *CARD_IN) * 2) * (1 - fade_out)
    ctx.save()
    ctx.translate(cx, cy + (1 - rise) * 90)
    s = lerp(0.94, 1, rise)
    ctx.scale(s, s)
    ctx.translate(-cx, -cy)
    card(ctx, cx, cy, cw, ch, a)
    # sentence with word-by-word highlight
    own_t, model_t = t - OWN_START, t - MODEL_START
    rec, mod = SAMPLE['recorded']['words'], SAMPLE['model']['words']
    for i, (w, x, wd) in enumerate(SPANS):
        col, weight = '#b8c3cc', 'm'
        if own_t >= rec[i]['start']:
            col = MUTED
        if model_t >= mod[i]['start']:
            col = PRIMARY
        draw_text(ctx, w, x, SENT_Y, SENT_SIZE, weight, col, a, 'l')
    draw_text(ctx, '…', ELLIPSIS_X, SENT_Y, SENT_SIZE, 'm', '#b8c3cc', a, 'l')
    ctx.restore()

    draw_line(ctx, SEG1, ease_io(prog(t, 2.45, 3.45)))
    m = ease_io(prog(t, *MERGE))
    y1 = lerp(ROW1_Y, 80, m)
    y2 = lerp(ROW2_Y, 80, m)
    draw_wave(ctx, *ROW_X, y1, ENV_OWN, prog(t, OWN_START, OWN_START + OWN_LEN), OWN, lerp(1, 0.75, m))
    draw_wave(ctx, *ROW_X, y2, ENV_MODEL, prog(t, MODEL_START, MODEL_START + MODEL_LEN), PRIMARY, 1, glow=True)
    # labels sit on the line like stations
    pill(ctx, 2045, ROW1_Y, '自分の声', 34, '#eef2f5', MUTED, a)
    pill(ctx, 2045, ROW2_Y, 'お手本', 34, PRIMARY, '#ffffff', a * clamp(prog(t, MODEL_START - 0.5, MODEL_START - 0.1)))

    # Mimi listens from the card's corner while the model plays
    pop = ease_back(prog(t, MODEL_START - 0.3, MODEL_START + 0.15)) * (1 - ease_io(prog(t, MERGE[0], MERGE[0] + 0.4)))
    if pop > 0:
        draw_image(ctx, image('listening.png'), 3330, -230, 300 * pop, 'b', 1, 1, -0.08)

    # headline
    k1 = ease_out(prog(t, VO['n2'] + 0.05, VO['n2'] + 0.55))
    k2 = ease_out(prog(t, VO['n2'] + N2_SECOND, VO['n2'] + N2_SECOND + 0.5))
    draw_text(ctx, '声はあなたのまま、', cx, -330 + (1 - k1) * 30, 92, 'b', INK, k1)
    draw_text(ctx, '発音だけネイティブに。', cx, -190 + (1 - k2) * 30, 92, 'b', BRAND_C, k2)


RADAR_C, RADAR_R = (5300, 40), 250
AXES = ['流暢さ', '発音', 'アクセント', 'リズム', '抑揚']
DEMO = [0.80, 0.52, 0.74, 0.68, 0.62]


def vertex(i, r=RADAR_R):
    ang = math.radians(-90 + 72 * i)
    return RADAR_C[0] + r * math.cos(ang), RADAR_C[1] + r * math.sin(ang)


SEG4 = bezier((ROW_X[1], 80), (3900, 80), (4500, vertex(0)[1]), vertex(0), 120)
PENTAGON = [vertex(i % 5) for i in range(6)]


def scene_radar(ctx, t):
    if t < 11.0:
        return
    draw_line(ctx, SEG4, ease_io(prog(t, 11.15, 11.9)), head=True)
    gp = ease_out(prog(t, PENT[0], PENT[1] + 0.3))
    for k in (0.33, 0.66):
        pts = [vertex(i % 5, RADAR_R * k) for i in range(6)]
        stroke_path(ctx, pts)
        ctx.set_line_width(2.5)
        ctx.set_source_rgba(*rgb(LINE_SOFT, gp))
        ctx.stroke()
    for i in range(5):
        ctx.move_to(*RADAR_C)
        ctx.line_to(*vertex(i))
        ctx.set_line_width(2)
        ctx.set_source_rgba(*rgb(LINE_SOFT, gp))
        ctx.stroke()
    f = ease_back(prog(t, *FILL), 1.3)
    if f > 0:
        pts = [vertex(i % 5, RADAR_R * DEMO[i % 5] * f) for i in range(6)]
        stroke_path(ctx, pts)
        ctx.close_path()
        ctx.set_source_rgba(*rgb(BRAND_C, 0.28))
        ctx.fill_preserve()
        ctx.set_source_rgba(*rgb(BRAND_C, 0.9))
        ctx.set_line_width(5)
        ctx.stroke()
        for i in range(5):
            p = vertex(i, RADAR_R * DEMO[i] * f)
            ctx.arc(*p, 9, 0, 2 * math.pi)
            ctx.set_source_rgba(*rgb(PRIMARY))
            ctx.fill()
    draw_line(ctx, PENTAGON, ease_io(prog(t, *PENT)), width=8)
    for i, label in enumerate(AXES):
        x, y = vertex(i, RADAR_R + 78)
        a = ease_out(prog(t, PENT[0] + i * 0.12, PENT[0] + i * 0.12 + 0.3))
        hi = i == 1 and t > 14.0
        draw_text(ctx, label, x, y, 40, 'b', PRIMARY if hi else INK, a)
    # weakest axis pulses before the line leaves it
    if t > 13.6:
        p = vertex(1, RADAR_R * DEMO[1])
        pulse = (t - 13.6) % 0.8 / 0.8
        ctx.arc(*p, 12 + 34 * pulse, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb(PINK, 0.8 * (1 - pulse)))
        ctx.set_line_width(5)
        ctx.stroke()
    if f > 0:  # overall demo score counts up in the centre
        ctx.arc(*RADAR_C, 78, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb('#ffffff', 0.95 * min(1, f)))
        ctx.fill()
        score = round(sum(DEMO) / len(DEMO) * 100 * ease_out(prog(t, *FILL)))
        draw_text(ctx, str(score), RADAR_C[0], RADAR_C[1] - 2, 84, 'b', PRIMARY, min(1, f))
    a = ease_out(prog(t, VO['n3'], VO['n3'] + 0.5))
    draw_text(ctx, 'あなたの発音を、5つの視点で。', 5150, -390 + (1 - a) * 24, 68, 'b', INK, a * (1 - prog(t, 14.2, 14.6)))
    pill(ctx, 5150, -472, 'デモ表示', 24, '#eef2f5', MUTED, gp * 0.9 * (1 - prog(t, 14.2, 14.6)), pad=(20, 8), weight='m')
    m = ease_back(prog(t, 12.2, 12.65)) * (1 - prog(t, 14.3, 14.7))
    draw_image(ctx, image('thinking.png'), 4740, 330, 320 * m, 'b')


NEXT_C = (6170, 10, 700, 420)
SEG6 = bezier(vertex(1, RADAR_R * DEMO[1]), (5650, -60), (5720, -40), (NEXT_C[0] - NEXT_C[2] / 2, -40), 80)


def scene_next(ctx, t):
    if t < 14.2:
        return
    draw_line(ctx, SEG6, ease_io(prog(t, 14.3, 14.9)))
    k1 = ease_out(prog(t, 14.55, 15.05)) * (1 - prog(t, 17.0, 17.3))
    k2 = ease_out(prog(t, 15.0, 15.5)) * (1 - prog(t, 17.0, 17.3))
    draw_parts(ctx, [('苦手', BRAND_C), ('がわかると、', INK)], 5650, -470 + (1 - k1) * 26, 66, k1)
    draw_parts(ctx, [('次の一文', BRAND_C), ('が変わる。', INK)], 5650, -380 + (1 - k2) * 26, 66, k2)
    cx, cy, cw, ch = NEXT_C
    r = ease_back(prog(t, *NEXT_CARD), 1.3)
    if r <= 0:
        return
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(lerp(0.9, 1, r), lerp(0.9, 1, r))
    ctx.translate(-cx, -cy)
    a = clamp(r * 1.5)
    card(ctx, cx, cy, cw, ch, a, 40)
    draw_text(ctx, '次の練習ポイント', cx - cw / 2 + 56, cy - 130, 34, 'b', BRAND_C, a, 'l')
    draw_text(ctx, '舌先を、軽く歯の間に。', cx - cw / 2 + 56, cy - 50, 54, 'b', INK, a, 'l')
    s = ease_out(prog(t, NEXT_SENTENCE, NEXT_SENTENCE + 0.45))
    ctx.move_to(cx - cw / 2 + 56, cy + 30)
    ctx.line_to(cx - cw / 2 + 56 + (cw - 112) * s, cy + 30)
    ctx.set_source_rgba(*rgb('#e2eaf0', a))
    ctx.set_line_width(2)
    ctx.stroke()
    draw_text(ctx, '次の一文', cx - cw / 2 + 56, cy + 85 + (1 - s) * 20, 28, 'm', MUTED, s, 'l')
    draw_text(ctx, 'Thank you for thinking of me.', cx - cw / 2 + 56, cy + 140 + (1 - s) * 20, 40, 'm', PRIMARY, s, 'l')
    ctx.restore()
    pop = ease_back(prog(t, MIMI_SUCCESS - 0.1, MIMI_SUCCESS + 0.25)) * (1 - prog(t, 17.1, 17.5))
    hop = 40 * math.sin(math.pi * prog(t, MIMI_SUCCESS + 0.25, MIMI_SUCCESS + 0.6))
    draw_image(ctx, image('success.png'), cx + cw / 2 - 40, cy - ch / 2 + 30 - hop, 260 * pop, 'b')


FORK_O = (7000, 0)
NODE_X = 8350
NODE_Y = [-480, -160, 160, 480]
NODE_R = 112
NODES_INFO = [('発音', 'node-pronunciation.jpg'), ('ロールプレイ', 'node-roleplay.jpg'),
              ('写真描写', 'node-describe.jpg'), ('英語日記', 'node-journal.jpg')]
SEG7 = [(NEXT_C[0] + NEXT_C[2] / 2, NEXT_C[1]), FORK_O]
BRANCHES = [bezier(FORK_O, (7450, 0), (7750, y), (NODE_X - NODE_R, y), 60) for y in NODE_Y]
LABEL_X = NODE_X + NODE_R + 50
TAG_C = (10100, 0)
BASE_Y = 160
BASE = (9620, 10580)


def converge_path(i):
    y = NODE_Y[i]
    x = LABEL_X + text_width(NODES_INFO[i][0], 66) + 40
    return bezier((x, y), (x + 320, y), (BASE[0] - 420, BASE_Y), (BASE[0], BASE_Y), 80)


CONVERGE = [converge_path(i) for i in range(4)]


def scene_fork(ctx, t):
    if t < 16.9:
        return
    draw_line(ctx, SEG7, ease_io(prog(t, 17.0, 17.4)), head=False)
    for i, br in enumerate(BRANCHES):
        draw_line(ctx, br, ease_io(prog(t, 17.3 + i * 0.05, 17.85 + i * 0.05)))
    for i, (label, photo) in enumerate(NODES_INFO):
        y = NODE_Y[i]
        on = prog(t, NODES[i] - 0.05, NODES[i] + 0.25)
        k = ease_back(on)
        ring = ease_out(prog(t, 17.6, 18.0))
        ctx.arc(NODE_X, y, NODE_R + 10, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb('#ffffff', ring))
        ctx.fill_preserve()
        ctx.set_line_width(6)
        ctx.set_source_rgba(*rgb(PRIMARY if on > 0 else LINE_SOFT, ring))
        ctx.stroke()
        if k > 0:
            draw_image(ctx, circle_photo(photo), NODE_X, y, NODE_R * 2 * k)
            burst = prog(t, NODES[i], NODES[i] + 0.5)
            if 0 < burst < 1:
                ctx.arc(NODE_X, y, NODE_R + 14 + 60 * ease_out(burst), 0, 2 * math.pi)
                ctx.set_source_rgba(*rgb(BRAND_C, 0.6 * (1 - burst)))
                ctx.set_line_width(5)
                ctx.stroke()
        draw_text(ctx, label, LABEL_X, y, 66, 'b', INK, ease_out(on), 'l')
    for i, path in enumerate(CONVERGE):
        draw_line(ctx, path, ease_io(prog(t, 20.55 + i * 0.04, 21.15 + i * 0.04)), head=i == 0)


SEG9 = bezier((BASE[1], BASE_Y), (11000, BASE_Y), (11200, 165), (11500, 165), 60)
LOCK2 = (11890, 60)
UNDER2 = [(11500, 165), (12560, 165)]
MIMI_X2 = 12380


def scene_tag(ctx, t):
    if t < 20.4:
        return
    draw_line(ctx, [(BASE[0], BASE_Y), (BASE[1], BASE_Y)], ease_io(prog(t, 21.0, 21.7)), width=10)
    k1 = ease_out(prog(t, TAG[0], TAG[0] + 0.5))
    k2 = ease_out(prog(t, TAG[1], TAG[1] + 0.5))
    draw_text(ctx, 'その声で、', TAG_C[0], -110 + (1 - k1) * 30, 116, 'b', INK, k1)
    draw_text(ctx, 'なりたい自分へ。', TAG_C[0], 50 + (1 - k2) * 30, 116, 'b', BRAND_C, k2)


def scene_final(ctx, t):
    if t < 22.4:
        return
    draw_line(ctx, SEG9, ease_io(prog(t, 22.55, 23.0)), head=False)
    u = ease_io(prog(t, *LOGO2_LINE))
    tip = draw_line(ctx, UNDER2, u)
    if u > 0:
        lockup(ctx, *LOCK2, reveal_x=tip[0] + 30 if u < 1 else None)
    # Mimi drops onto the line on the hit, then a happy hop on the fanfare
    if t > MIMI_LAND - 0.35:
        f = prog(t, MIMI_LAND - 0.35, MIMI_LAND)
        yb = lerp(-900, 165, ease_in(f))
        sq = spring(t, MIMI_LAND, 0.24, 2.6, 7)
        sx, sy = (0.9, 1.12) if f < 1 else (1 + sq * 0.75, 1 - sq)
        hop = prog(t, FANFARE, FANFARE + 0.45)
        yb -= 70 * math.sin(math.pi * hop)
        pose = 'success.png' if FANFARE - 0.05 < t else 'master.png'
        draw_image(ctx, image(pose), MIMI_X2, yb, 330, 'b', sx, sy)
    e = ease_out(prog(t, END_CARD, END_CARD + 0.6))
    if e > 0:
        bx, by = 11740, 400
        w = text_width('7日間無料ではじめる', 46) + 100
        round_rect(ctx, bx - w / 2, by - 52 + (1 - e) * 30, w, 104, 52)
        ctx.set_source_rgba(*rgb(PRIMARY, e))
        ctx.fill()
        draw_text(ctx, '7日間無料ではじめる', bx, by + (1 - e) * 30, 46, 'b', '#ffffff', e)
        draw_image(ctx, image('appstore.png'), 12330, by + (1 - e) * 30, 104, alpha=e)
        draw_text(ctx, 'lanclo.app', 12000, 530 + (1 - e) * 30, 36, 'm', MUTED, e)


SCENES = [scene_hook, scene_logo, scene_question, scene_card, scene_radar, scene_next, scene_fork, scene_tag, scene_final]


def shake(t):
    out = [0.0, 0.0]
    for t0, amp in ((HOOK_LAND, 26), (MIMI_LAND, 12)):
        d = t - t0
        if 0 <= d < 0.5:
            k = amp * math.exp(-9 * d)
            out[0] += k * math.sin(d * 71)
            out[1] += k * math.cos(d * 59)
    return out


def subtitles(ctx, t, W, H, S):
    for k, (t0, t1) in SUB_OUT.items():
        a = min(prog(t, t0 + 0.15, t0 + 0.35), 1 - prog(t, t1 - 0.2, t1))
        if a <= 0:
            continue
        ctx.save()
        ctx.scale(S, S)
        y, size = H / S - 78, 38
        w = text_width(SUBS[k], size, 'm') + 56
        round_rect(ctx, W / S / 2 - w / 2, y - 34, w, 68, 34)
        ctx.set_source_rgba(*rgb('#ffffff', 0.82 * a))
        ctx.fill()
        draw_text(ctx, SUBS[k], W / S / 2, y, size, 'm', INK, a)
        ctx.restore()


GRAIN = None


def frame(t_out, W, H, S):
    global T_OUT
    T_OUT = t_out
    t = to_story(t_out)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    cam = camera(t)
    background(ctx, t, cam, W, H, S)
    cx, cy, z = cam
    dx, dy = shake(t)
    ctx.translate(W / 2 + dx * S, H / 2 + dy * S)
    ctx.scale(z * S, z * S)
    ctx.translate(-cx, -cy)
    for s in SCENES:
        s(ctx, t)
    ctx.identity_matrix()
    subtitles(ctx, t_out, W, H, S)
    surf.flush()
    stride = surf.get_stride()
    arr = np.ndarray((H, stride // 4, 4), np.uint8, surf.get_data())[:, :W]
    g = GRAIN[int(t_out * 24) % len(GRAIN)]
    out = np.clip(arr[..., :3].astype(np.int16) + g[..., None], 0, 255).astype(np.uint8)
    return np.dstack([out, arr[..., 3:]])


def main():
    global GRAIN
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--fps', type=int, default=FPS)
    ap.add_argument('--from', dest='t0', type=float, default=0.0)
    ap.add_argument('--to', dest='t1', type=float, default=OUT_DURATION)
    ap.add_argument('--still', default='')
    ap.add_argument('--audio', default='')
    a = ap.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    W, H = int(W0 * a.scale) // 2 * 2, int(H0 * a.scale) // 2 * 2
    GRAIN = [np.random.default_rng(i).integers(-3, 4, (H, W)).astype(np.int16) for i in range(6)]
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
    n0, n1 = round(a.t0 * a.fps), round(a.t1 * a.fps)
    for n in range(n0, n1):
        p.stdin.write(frame(n / a.fps, W, H, a.scale).tobytes())
        if n % (a.fps * 2) == 0:
            print(f'{n / a.fps:5.1f}s', file=sys.stderr, flush=True)
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    main()
