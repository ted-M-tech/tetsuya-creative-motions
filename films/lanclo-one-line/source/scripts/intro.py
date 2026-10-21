"""Render the app intro (9:16, 30 s) frame by frame (cairo) and pipe to ffmpeg.

Same drawing language as the "One line" promo (render.py): one line runs through every station.
usage: intro.py OUT.mp4 [--scale 0.5] [--fps 30] [--from 0 --to 30] [--still T,T,...] [--audio mix.wav] [--en]
--en draws English subtitles in the bottom safe zone (the English-subtitle cut); without it the picture is unchanged.
"""
import argparse
import math
import subprocess
import sys
from pathlib import Path

import cairo
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from render import (A, PAPER, SOFT, INK, PRIMARY, BRAND_C, MUTED, LINE_SOFT, OWN, PINK, rgb, clamp, prog,  # noqa: E402
                    ease_io, ease_out, ease_in, ease_back, spring, lerp, image, circle_photo, text_width, draw_text,
                    draw_image, round_rect, card, pill, bezier, draw_line, glow_dot, stroke_path, lockup, draw_parts,
                    envelope, SAMPLE)
from journal import background, headline, mic_glyph, wrap_words  # noqa: E402
import journal  # noqa: E402
from intro_timeline import *  # noqa: E402,F403

W0, H0 = 1080, 1920
journal.BLOBS = [(float(x), float(y), float(r)) for x, y, r in
                 zip(*(np.random.default_rng(23).uniform(lo, hi, 34) for lo, hi in ((-700, 700), (-900, 13300), (180, 420))))]


def camera(t):
    for (t0, y0, z0), (t1, y1, z1) in zip(CAMERA, CAMERA[1:]):
        if t0 <= t <= t1:
            u = ease_io(prog(t, t0, t1))
            return lerp(y0, y1, u), math.exp(lerp(math.log(z0), math.log(z1), u))
    return CAMERA[-1][1:]


def speaker_glyph(ctx, x, y, s, color, waves=2):
    ctx.set_source_rgba(*rgb(color))
    ctx.move_to(x - 22 * s, y - 10 * s)
    ctx.line_to(x - 10 * s, y - 10 * s)
    ctx.line_to(x + 6 * s, y - 24 * s)
    ctx.line_to(x + 6 * s, y + 24 * s)
    ctx.line_to(x - 10 * s, y + 10 * s)
    ctx.line_to(x - 22 * s, y + 10 * s)
    ctx.close_path()
    ctx.fill()
    ctx.set_line_width(5 * s)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(waves):
        ctx.arc(x + 8 * s, y, (16 + 12 * k) * s, -0.3 * math.pi, 0.3 * math.pi)
        ctx.stroke()


def icon_pill(ctx, cx, cy, label, size, bg, fg, alpha, glyph):
    """Pill with a drawn icon on the left (the font has no emoji)."""
    if alpha <= 0:
        return
    tw = text_width(label, size)
    w, h = tw + size * 1.3 + 70, size * 1.2 + 30
    round_rect(ctx, cx - w / 2, cy - h / 2, w, h, h / 2)
    ctx.set_source_rgba(*rgb(bg, alpha))
    ctx.fill()
    gx = cx - w / 2 + 34 + size * 0.45
    ctx.push_group()
    glyph(ctx, gx, cy + (4 if glyph is mic_glyph else 0), size / 62, fg)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    draw_text(ctx, label, gx + size * 0.75, cy, size, 'b', fg, alpha, 'l')


# ---------- S0 hook: typed type ----------
LINE1, LINE2A, LINE2B = 'その英語、', 'まだ日本語に', '聞こえとるわ。'
HOOK_SIZE = 104


def typed(s, t, start, per):
    return s[:max(0, min(len(s), int((t - start) / per) + 1))] if t >= start else ''


def hook_chars(t):
    n2 = len(LINE2A + LINE2B)
    a = typed(LINE1, t, *TYPE_1)
    b = typed(LINE2A + LINE2B, t, *TYPE_2)
    return a, b[:len(LINE2A)], b[len(LINE2A):], len(b) == n2


def phone(ctx, cx, cy, h, alpha, t):
    """A pale phone on its recording screen, behind the second card."""
    w = h * 0.49
    round_rect(ctx, cx - w / 2, cy - h / 2, w, h, w * 0.16)
    ctx.set_source_rgba(*rgb('#ffffff', alpha))
    ctx.fill_preserve()
    ctx.set_source_rgba(*rgb(PRIMARY, alpha * 0.8))
    ctx.set_line_width(10)
    ctx.stroke()
    round_rect(ctx, cx - w * 0.16, cy - h / 2 + 26, w * 0.32, 34, 17)
    ctx.set_source_rgba(*rgb(PRIMARY, alpha * 0.8))
    ctx.fill()
    for i, lw in enumerate((0.7, 0.5)):
        round_rect(ctx, cx - w * 0.36, cy - h * 0.3 + i * 52, w * lw, 26, 13)
        ctx.set_source_rgba(*rgb(LINE_SOFT, alpha))
        ctx.fill()
    n = 26
    for i in range(n):
        v = 0.25 + 0.75 * abs(math.sin(i * 0.9 + t * 7)) * abs(math.sin(i * 0.37))
        x = cx - w * 0.38 + i * (w * 0.76 / (n - 1))
        ctx.move_to(x, cy - v * 70)
        ctx.line_to(x, cy + v * 70)
    ctx.set_line_width(9)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgba(*rgb(OWN, alpha))
    ctx.stroke()
    ctx.arc(cx, cy + h * 0.33, 62, 0, 2 * math.pi)
    ctx.set_source_rgba(*rgb(PINK, alpha))
    ctx.fill()


MIMI_HOOK = (-150, S0 + 930, 1000)  # bottom-centre x, y and height of the big pointing Mimi
POINT_TIP = (0.962, 0.661)  # fingertip as a fraction of point.png


def mimi_hook(ctx, t):
    """Big Mimi springs up and points out at the viewer while the first line plays; leaves for the second card."""
    if t > CARD_2 + 0.35:
        return
    x, yb, h = MIMI_HOOK
    up = ease_back(prog(t, 0.05, 0.45), 1.6)
    away = ease_in(prog(t, CARD_2, CARD_2 + 0.3))
    yb += (1 - up) * 900 + away * 1100
    poke = spring(t, VO['v1'], 0.18, 2.4, 7) + spring(t, JOLT, 0.14, 3.0, 8)  # a jab on the line and on the stop
    sx, sy = 1 + 0.5 * poke, 1 - 0.4 * poke
    rot = 0.03 * math.sin(t * 5.5) * clamp(prog(t, VO['v1'], VO['v1'] + 0.2))
    draw_image(ctx, image('point.png'), x, yb, h, 'b', sx, sy, rot)
    tx = x + (POINT_TIP[0] - 0.5) * h * 1050 / 1347
    ty = yb - h + POINT_TIP[1] * h
    for j, ang in enumerate((-0.5, 0.0, 0.5)):  # emphasis strokes off the fingertip
        e = prog(t, JOLT + j * 0.03, JOLT + 0.35 + j * 0.03)
        if 0 < e < 1:
            r0, r1 = 50 + 40 * ease_out(e), 90 + 70 * ease_out(e)
            ctx.move_to(tx + r0 * math.cos(ang), ty + r0 * math.sin(ang))
            ctx.line_to(tx + r1 * math.cos(ang), ty + r1 * math.sin(ang))
            ctx.set_line_width(10)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_source_rgba(*rgb(PINK, 1 - e))
            ctx.stroke()


def scene_hook(ctx, t):
    if t > MOVE1[1] + 0.1:
        return
    out1 = ease_io(prog(t, CARD_2, CARD_2 + 0.45))
    if out1 < 1:
        a, b1, b2, done = hook_chars(t)
        y0 = S0 - 640 - out1 * 120
        al = 1 - out1
        x1 = x2 = x3 = -text_width(LINE2B, HOOK_SIZE) / 2  # one left edge, like a text field
        draw_text(ctx, a, x1, y0, HOOK_SIZE, 'b', INK, al, 'l')
        draw_parts_left(ctx, [(b1[:2], INK), (b1[2:5], BRAND_C), (b1[5:], INK)], x2, y0 + 160, HOOK_SIZE, al)
        draw_text(ctx, b2, x3, y0 + 320, HOOK_SIZE, 'b', INK, al, 'l')
        # caret
        if not done or t < JOLT + 0.5:
            if b2:
                cx, cy = x3 + text_width(b2, HOOK_SIZE), y0 + 320
            elif b1:
                cx, cy = x2 + text_width(b1, HOOK_SIZE), y0 + 160
            else:
                cx, cy = x1 + text_width(a, HOOK_SIZE), y0
            if (t * 2.2) % 1 < 0.6 or (0 < t - TYPE_1[0] < 2.4):
                round_rect(ctx, cx + 8, cy - 52, 8, 104, 4)
                ctx.set_source_rgba(*rgb(BRAND_C, al))
                ctx.fill()
        # a short underline sweeps under 日本語 when the stop lands
        u = ease_out(prog(t, JOLT, JOLT + 0.35))
        if u > 0:
            ux = x2 + text_width('まだ', HOOK_SIZE)
            draw_line(ctx, [(ux, y0 + 228), (ux + text_width('日本語', HOOK_SIZE), y0 + 228)], u, width=8, color=PINK,
                      alpha=al, head=False)
    mimi_hook(ctx, t)
    k = ease_out(prog(t, CARD_2 + 0.15, CARD_2 + 0.6))
    if k > 0:
        gone = 1 - prog(t, MOVE1[0], MOVE1[0] + 0.3)
        phone(ctx, 0, S0 + 260 + (1 - k) * 60, 900, 0.22 * k * gone, t)
        k2 = ease_out(prog(t, CARD_2 + 0.55, CARD_2 + 1.0))
        draw_parts(ctx, [('どこが変なんか', BRAND_C), ('、', INK)], 0, S0 - 520 + (1 - k) * 26, 92, k * gone)
        draw_parts(ctx, [('自分では', INK), ('聞こえへん', BRAND_C), ('。', INK)], 0, S0 - 390 + (1 - k2) * 26, 92, k2 * gone)


def draw_parts_left(ctx, parts, x, y, size, alpha=1.0, weight='b'):
    for p, col in parts:
        if p:
            draw_text(ctx, p, x, y, size, weight, col, alpha, 'l')
            x += text_width(p, size, weight)


# ---------- S1 logo + question ----------
SEG_A = [(-380, S1 + 10), (380, S1 + 10)]
LOCK_Y = S1 - 90
SEG_B = bezier((380, S1 + 10), (560, S1 + 500), (560, S2 - 700), (420, S2 - 330), 120)


def scene_logo(ctx, t):
    if t < MOVE1[0] or t > MOVE2[1] + 0.2:
        return
    u = ease_io(prog(t, *LOGO_LINE))
    tip = draw_line(ctx, SEG_A, u)
    if u > 0:
        lockup(ctx, 0, LOCK_Y, reveal_x=tip[0] + 30 if u < 1 else None)
    m = ease_back(prog(t, MIMI_POP, MIMI_POP + 0.35))
    draw_image(ctx, image('listening.png'), 300, LOCK_Y - 110, 300 * m, 'b', 1, 1, 0.08)
    k1 = ease_out(prog(t, Q_IN[0], Q_IN[0] + 0.5))
    k2 = ease_out(prog(t, Q_IN[1], Q_IN[1] + 0.5))
    draw_parts(ctx, [('自分の声', BRAND_C), ('で、', INK)], 0, S1 + 200 + (1 - k1) * 26, 80, k1)
    draw_parts(ctx, [('ネイティブの発音', BRAND_C), ('が', INK)], 0, S1 + 310 + (1 - k2) * 26, 80, k2)
    draw_parts(ctx, [('聴けたらどうやろ？', INK)], 0, S1 + 420 + (1 - k2) * 26, 80, k2)
    draw_line(ctx, SEG_B, ease_io(prog(t, MOVE2[0], MOVE2[1])), head=t < MOVE2[1])


# ---------- S2 recording card ----------
CARD = (0, S2 + 40, 960, 700)
WAVE_X = (-400, 400)
ROW1, ROW2 = S2 + 50, S2 + 280
ENV_OWN = envelope('voice/own.mp3', OWN_CLIP, 48)
ENV_MODEL = envelope('voice/model.mp3', MODEL_CLIP, 48)
REC_W, MOD_W = SAMPLE['recorded']['words'][:8], SAMPLE['model']['words'][:8]
SENT = wrap_words([w['text'] for w in REC_W[:-1]] + ['available?'], 54, 820)


def draw_wave(ctx, y, env, u, color, alpha=1.0, amp=74, glow=False):
    x0, x1 = WAVE_X
    n = len(env)
    gap = (x1 - x0) / n
    head_x = lerp(x0, x1, clamp(u))
    draw_line(ctx, [(x0, y), (x1, y)], clamp(u), width=5, color=color, alpha=alpha * 0.9, head=False)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, v in enumerate(env):
        bx = x0 + gap * (i + 0.5)
        if bx > head_x:
            break
        hh = max(4, v * amp * ease_back(clamp((head_x - bx) / 60)))
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


SEG_C = bezier((WAVE_X[1], S2 + 210), (560, S2 + 700), (560, S3 - 900), (0, S3 - 120 - 300), 120)


def scene_card(ctx, t):
    if t < MOVE2[0] or t > MOVE3[1] + 0.2:
        return
    cx, cy, cw, ch = CARD
    rise = ease_back(prog(t, *CARD_IN), 1.2)
    m = ease_io(prog(t, *MERGE))
    a = clamp(prog(t, *CARD_IN) * 2) * (1 - m)
    if a > 0:
        ctx.save()
        ctx.translate(cx, cy + (1 - rise) * 80)
        s = lerp(0.94, 1, rise)
        ctx.scale(s, s)
        ctx.translate(-cx, -cy)
        card(ctx, cx, cy, cw, ch, a, 44)
        top = cy - ch / 2
        # the sentence: grey with the own take, cleared in the silence, navy with the model
        own_t, mod_t = t - OWN_START, t - MODEL_START
        clear = prog(t, FREEZE, FREEZE + 0.3)
        for (w, x, li), rw, mw in zip(SENT, REC_W, MOD_W):
            col, al = '#b8c3cc', 0.0
            if own_t >= rw['start']:
                col, al = MUTED, 1 - clear
            if mod_t >= mw['start']:
                col, al = PRIMARY, 1.0
            k = ease_out(clamp((own_t - rw['start']) / 0.2)) if mod_t < mw['start'] else 1
            draw_text(ctx, w, x, top + 110 + li * 72 + (1 - k) * 10 * (clear < 1), 54, 'b' if col == PRIMARY else 'm',
                      col, a * max(al, 0.25), 'l')
        ctx.restore()
    # rows: the own take (pale), then the model (dark) under it
    y1 = lerp(ROW1, S2 + 210, m)
    y2 = lerp(ROW2, S2 + 210, m)
    icon_pill(ctx, -270, ROW1 - 105, '自分の声', 34, '#eef2f5', MUTED, a * clamp(prog(t, REC_CLICK, REC_CLICK + 0.2)),
              mic_glyph)
    draw_wave(ctx, y1, ENV_OWN, prog(t, OWN_START, OWN_START + OWN_CLIP), OWN, lerp(1, 0.0, m))
    lab = ease_back(prog(t, MODEL_LABEL, MODEL_LABEL + 0.3))
    if lab > 0:
        icon_pill(ctx, -284, ROW2 - 105, 'お手本', 34, PRIMARY, '#ffffff', a * clamp(lab), speaker_glyph)
    draw_wave(ctx, y2, ENV_MODEL, prog(t, MODEL_START, MODEL_START + MODEL_CLIP), PRIMARY, 1, glow=True)
    # the freeze: a thin playhead holds still, then 音声ON in the top third
    if FREEZE <= t < MODEL_START:
        f = 1 - prog(t, MODEL_START - 0.1, MODEL_START)
        ctx.move_to(WAVE_X[1] + 22, ROW1 - 60)
        ctx.line_to(WAVE_X[1] + 22, ROW2 + 60)
        ctx.set_source_rgba(*rgb(BRAND_C, 0.5 * f))
        ctx.set_line_width(3)
        ctx.stroke()
    on = ease_back(prog(t, MODEL_LABEL, MODEL_LABEL + 0.35), 2.0) * (1 - prog(t, MERGE[0] - 0.3, MERGE[0]))
    if on > 0:
        ctx.save()
        ctx.translate(0, S2 - 560)
        ctx.scale(on, on)
        icon_pill(ctx, 0, 0, '音声ON', 52, BRAND_C, '#ffffff', clamp(on), speaker_glyph)
        ctx.restore()
        if MODEL_START <= t <= MODEL_START + MODEL_CLIP:  # rings from the badge while the model plays
            ph = ((t - MODEL_START) / 0.6) % 1
            round_rect(ctx, -170 - 40 * ph, S2 - 560 - 52 - 20 * ph, 340 + 80 * ph, 104 + 40 * ph, 52 + 20 * ph)
            ctx.set_source_rgba(*rgb(BRAND_C, 0.4 * (1 - ph)))
            ctx.set_line_width(4)
            ctx.stroke()
    pop = ease_back(prog(t, MODEL_START - 0.2, MODEL_START + 0.15)) * (1 - ease_io(prog(t, MERGE[0], MERGE[0] + 0.4)))
    draw_image(ctx, image('listening.png'), 360, cy - ch / 2 + 20, 260 * pop, 'b', 1, 1, 0.08)
    # 声はあなたのまま、発音だけネイティブに。
    k1 = ease_out(prog(t, H_VOICE[0], H_VOICE[0] + 0.5))
    k2 = ease_out(prog(t, H_VOICE[1], H_VOICE[1] + 0.5))
    draw_text(ctx, '声はあんたのまま、', 0, S2 - 230 + (1 - k1) * 30, 88, 'b', INK, k1)
    draw_text(ctx, '発音だけネイティブや。', 0, S2 - 100 + (1 - k2) * 30, 88, 'b', BRAND_C, k2)
    draw_line(ctx, SEG_C, ease_io(prog(t, MOVE3[0], MOVE3[1])), head=t < MOVE3[1])


# ---------- S3 radar and the tip ----------
RADAR_C, RADAR_R = (0, S3 - 120), 260
AXES = ['流暢さ', '発音', 'アクセント', 'リズム', '抑揚']
BEFORE = [0.70, 0.46, 0.66, 0.62, 0.61]   # 61
AFTER = [0.76, 0.56, 0.72, 0.68, 0.63]    # 67


def vertex(i, r=RADAR_R):
    ang = math.radians(-90 + 72 * i)
    return RADAR_C[0] + r * math.cos(ang), RADAR_C[1] + r * math.sin(ang)


PENTAGON = [vertex(i % 5) for i in range(6)]
TIP_C = (0, S3 + 470, 900, 250)
SEG_D = bezier((TIP_C[2] / 2, TIP_C[1]), (560, S3 + 900), (0, S4 - 900), (0, S4 - 290), 120)  # into the top of the language ring


def scene_radar(ctx, t):
    if t < MOVE3[0] or t > MOVE4[1] + 0.2:
        return
    gp = ease_out(prog(t, PENT[0], PENT[1] + 0.3))
    for k in (0.33, 0.66):
        stroke_path(ctx, [vertex(i % 5, RADAR_R * k) for i in range(6)])
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
    g = ease_io(prog(t, *GAIN))
    vals = [lerp(b, a, g) for b, a in zip(BEFORE, AFTER)]
    if f > 0:
        if g > 0:  # the earlier shape stays as a faint ghost
            stroke_path(ctx, [vertex(i % 5, RADAR_R * BEFORE[i % 5]) for i in range(6)])
            ctx.set_source_rgba(*rgb(OWN, 0.8 * g))
            ctx.set_line_width(3)
            ctx.set_dash([10, 8])
            ctx.stroke()
            ctx.set_dash([])
        pts = [vertex(i % 5, RADAR_R * vals[i % 5] * f) for i in range(6)]
        stroke_path(ctx, pts)
        ctx.close_path()
        ctx.set_source_rgba(*rgb(BRAND_C, 0.28))
        ctx.fill_preserve()
        ctx.set_source_rgba(*rgb(BRAND_C, 0.9))
        ctx.set_line_width(5)
        ctx.stroke()
        for i in range(5):
            ctx.arc(*vertex(i, RADAR_R * vals[i] * f), 9, 0, 2 * math.pi)
            ctx.set_source_rgba(*rgb(PRIMARY))
            ctx.fill()
    draw_line(ctx, PENTAGON, ease_io(prog(t, *PENT)), width=8)
    for i, label in enumerate(AXES):
        x, y = vertex(i, RADAR_R + 80)
        a = ease_out(prog(t, PENT[0] + i * 0.12, PENT[0] + i * 0.12 + 0.3))
        draw_text(ctx, label, x, y, 42, 'b', PRIMARY if i == 1 and t > TIP_IN else INK, a)
    if f > 0:
        ctx.arc(*RADAR_C, 84, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb('#ffffff', 0.95 * min(1, f)))
        ctx.fill()
        score = round(sum(vals) / 5 * 100 * ease_out(prog(t, *FILL)))
        bump = 1 + spring(t, GAIN[1], 0.18, 2.6, 7)
        draw_text(ctx, str(score), RADAR_C[0], RADAR_C[1] - 2, 90, 'b', PRIMARY, min(1, f), scale=bump)
        p = ease_back(prog(t, GAIN[1] - 0.1, GAIN[1] + 0.25), 2.0)
        if p > 0:
            ctx.save()
            ctx.translate(RADAR_C[0] + 150, RADAR_C[1] - 90)
            ctx.scale(p, p)
            pill(ctx, 0, 0, '+6', 40, PINK, '#ffffff', clamp(p), pad=(22, 8))
            ctx.restore()
    # weak axis pulses once the tip arrives
    if t > TIP_IN:
        p = vertex(1, RADAR_R * vals[1])
        pulse = (t - TIP_IN) % 0.8 / 0.8
        ctx.arc(*p, 12 + 34 * pulse, 0, 2 * math.pi)
        ctx.set_source_rgba(*rgb(PINK, 0.8 * (1 - pulse)))
        ctx.set_line_width(5)
        ctx.stroke()
    headline(ctx, S3 - 700, [('ゴール', BRAND_C), ('との差を、', INK)], [('5つの視点', BRAND_C), ('で見るで。', INK)], t, H_RADAR,
             out=TIP_IN - 0.3, size=84)
    headline(ctx, S3 - 700, [('直す音', BRAND_C), ('がわかるから、', INK)], [('もう', INK), ('迷わへん', BRAND_C), ('。', INK)], t, H_TIP,
             size=84)
    m = ease_back(prog(t, FILL[0], FILL[0] + 0.4)) * (1 - prog(t, TIP_IN, TIP_IN + 0.3))
    draw_image(ctx, image('thinking.png'), -400, RADAR_C[1] + 470, 260 * m, 'b')
    # the tip card, tail pointing at 発音
    cx, cy, cw, ch = TIP_C
    r = ease_back(prog(t, TIP_IN, TIP_IN + 0.4), 1.3)
    if r > 0:
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(lerp(0.9, 1, r), lerp(0.9, 1, r))
        ctx.translate(-cx, -cy)
        a = clamp(r * 1.5)
        card(ctx, cx, cy, cw, ch, a, 40)
        draw_text(ctx, '次の練習ポイント', cx - cw / 2 + 56, cy - 50, 34, 'b', BRAND_C, a, 'l')
        draw_text(ctx, '舌先、軽く歯の間にな。', cx - cw / 2 + 56, cy + 30, 60, 'b', INK, a, 'l')
        ctx.restore()
    s = ease_back(prog(t, TIP_IN + 0.35, TIP_IN + 0.7)) * (1 - prog(t, MOVE4[0], MOVE4[0] + 0.3))
    hop = 40 * math.sin(math.pi * prog(t, TIP_IN + 0.7, TIP_IN + 1.05))
    draw_image(ctx, image('success.png'), cw / 2 - 40, cy - ch / 2 + 10 - hop, 200 * s, 'b')
    draw_line(ctx, SEG_D, ease_io(prog(t, MOVE4[0], MOVE4[1])), head=t < MOVE4[1])


# ---------- S4 17 languages ----------
RC, RR = (0, S4 - 40), 250  # the ring around the count
GREET_H = 1.6  # greeting PNG line box / font size (scripts/greetings.swift)
# (code, x, y, size): English and Korean are named in the line, so they come first and larger
GREETS = [('en', -235, S4 - 620, 86), ('ko', 250, S4 - 440, 86),
          ('ja', 0, S4 + 400, 64), ('zh', -340, S4 + 420, 64), ('fr', -320, S4 - 400, 64), ('es', 300, S4 - 760, 64),
          ('th', 380, S4 - 230, 64), ('yue', 340, S4 + 430, 64), ('de', -320, S4 - 820, 64), ('it', -400, S4 - 170, 64),
          ('pt-BR', 420, S4 + 30, 64), ('id', -410, S4 + 70, 64), ('vi', -250, S4 + 610, 64), ('hi', 240, S4 + 620, 64),
          ('bn', -330, S4 + 800, 64), ('ru', 50, S4 + 810, 64), ('tr', 370, S4 + 790, 64)]
GREET_T = [LANG_EN, LANG_KO] + [LANG_ALL + i * LANG_STEP for i in range(15)]
RING_P = [(RC[0] + RR * math.sin(a), RC[1] - RR * math.cos(a)) for a in np.linspace(0, 2 * math.pi, 121)]
SEG_G = [(0, RC[1] + RR), (0, S5 - 480)]


def bubble(ctx, code, x, y, size, k, alpha):
    """A speech bubble with one greeting, scaled by k from its tail."""
    if k < 0.02 or alpha <= 0:
        return
    surf = image(f'greet/{code}.png')
    h = size * GREET_H
    w = surf.get_width() * h / surf.get_height()
    bw, bh = w + 34, size * 1.5
    ctx.save()
    ctx.translate(x - bw / 2 + 40, y + bh / 2)
    ctx.scale(k, k)
    ctx.translate(-(x - bw / 2 + 40), -(y + bh / 2))
    card(ctx, x, y, bw, bh, alpha, r=bh / 2)
    ctx.move_to(x - bw / 2 + 30, y + bh / 2 - 6)
    ctx.line_to(x - bw / 2 + 22, y + bh / 2 + 26)
    ctx.line_to(x - bw / 2 + 62, y + bh / 2 - 6)
    ctx.close_path()
    ctx.set_source_rgba(*rgb('#ffffff', alpha))
    ctx.fill()
    draw_image(ctx, surf, x, y + size * 0.05, h, alpha=alpha)
    ctx.restore()


def scene_langs(ctx, t):
    if t < MOVE4[0] or t > MOVE5[1] + 0.2:
        return
    tip = draw_line(ctx, RING_P, ease_io(prog(t, *RING)), head=t < RING[1])
    gather = ease_in(prog(t, CONVERGE, CONVERGE + 0.45))
    n = sum(t >= g for g in GREET_T)
    if n:  # the count: one per greeting, 17 once they are all in
        land = spring(t, GREET_T[-1], 0.22, 2.6, 7)
        draw_text(ctx, str(n), 0, RC[1] - 40, 230 * (1 + 0.25 * land), 'b', PRIMARY)
        draw_text(ctx, '言語', 0, RC[1] + 110, 72, 'b', INK, ease_out(prog(t, LANG_EN, LANG_EN + 0.3)))
        r = prog(t, GREET_T[-1], GREET_T[-1] + 0.6)
        if 0 < r < 1:
            ctx.arc(*RC, RR + 10 + 80 * ease_out(r), 0, 2 * math.pi)
            ctx.set_source_rgba(*rgb(BRAND_C, 0.5 * (1 - r)))
            ctx.set_line_width(6)
            ctx.stroke()
    for i, ((code, x, y, size), t0) in enumerate(zip(GREETS, GREET_T)):
        if t < t0:
            continue
        k = ease_back(prog(t, t0, t0 + 0.3), 2.0)
        y += 7 * math.sin((t - t0) * 2.4 + i)
        x, y = lerp(x, RC[0], gather), lerp(y, RC[1], gather)
        bubble(ctx, code, x, y, size, k * (1 - 0.7 * gather), 1 - gather)
        if i < 2:
            burst = prog(t, t0, t0 + 0.5)
            if 0 < burst < 1:
                ctx.arc(x, y, 110 + 70 * ease_out(burst), 0, 2 * math.pi)
                ctx.set_source_rgba(*rgb(BRAND_C, 0.5 * (1 - burst)))
                ctx.set_line_width(5)
                ctx.stroke()
    draw_line(ctx, SEG_G, ease_io(prog(t, CONVERGE + 0.4, MOVE5[0] + 0.3)), head=t < MOVE5[0] + 0.3)


# ---------- S5 tagline ----------
SEG_E = [(0, S5 - 480), (0, S5 - 300)]
SEG_F = bezier((0, S5 + 300), (0, S5 + 800), (-560, S6 - 500), (-380, S6 + 10), 120)


def scene_tag(ctx, t):
    if t < MOVE5[0] or t > MOVE6[1] + 0.2:
        return
    draw_line(ctx, SEG_E, ease_io(prog(t, MOVE5[0] + 0.2, MOVE5[1])), head=False)
    k1 = ease_out(prog(t, TAG[0], TAG[0] + 0.5))
    k2 = ease_out(prog(t, TAG[1], TAG[1] + 0.5))
    draw_text(ctx, 'その声で、', 0, S5 - 110 + (1 - k1) * 30, 120, 'b', INK, k1)
    draw_text(ctx, 'なりたい自分へ行こ。', 0, S5 + 60 + (1 - k2) * 30, 100, 'b', BRAND_C, k2)
    draw_line(ctx, [(0, S5 + 200), (0, S5 + 300)], ease_io(prog(t, MOVE6[0] - 0.2, MOVE6[0])), head=False)
    draw_line(ctx, SEG_F, ease_io(prog(t, MOVE6[0], MOVE6[1])), head=False)


# ---------- S6 lock-up ----------
UNDER = [(-380, S6 + 10), (380, S6 + 10)]
LOCK2_Y = S6 - 90


def sparkle(ctx, x, y, r, alpha, color=BRAND_C):
    ctx.move_to(x, y - r)
    for k in range(4):
        a0 = math.pi / 2 * k - math.pi / 2
        ctx.curve_to(x + 0.12 * r * math.cos(a0 + 0.8), y + 0.12 * r * math.sin(a0 + 0.8),
                     x + 0.12 * r * math.cos(a0 + 0.8), y + 0.12 * r * math.sin(a0 + 0.8),
                     x + r * math.cos(a0 + math.pi / 2), y + r * math.sin(a0 + math.pi / 2))
    ctx.close_path()
    ctx.set_source_rgba(*rgb(color, alpha))
    ctx.fill()


def scene_final(ctx, t):
    if t < MOVE6[0]:
        return
    u = ease_io(prog(t, *LOGO2_LINE))
    tip = draw_line(ctx, UNDER, u)
    if u > 0:
        lockup(ctx, 0, LOCK2_Y, reveal_x=tip[0] + 30 if u < 1 else None)
    if t > MIMI_LAND - 0.35:  # Mimi drops in above the lock-up, hops on the fanfare, then winks
        f = prog(t, MIMI_LAND - 0.35, MIMI_LAND)
        yb = lerp(S6 - 1300, S6 - 240, ease_in(f))
        sq = spring(t, MIMI_LAND, 0.24, 2.6, 7) + spring(t, WINK, 0.12, 3.0, 8)
        sx, sy = (0.9, 1.12) if f < 1 else (1 + sq * 0.75, 1 - sq)
        yb -= 70 * math.sin(math.pi * prog(t, FANFARE, FANFARE + 0.45))
        tilt = -0.08 * ease_back(prog(t, WINK, WINK + 0.3))
        pose = 'master.png' if t >= WINK else 'success.png'
        draw_image(ctx, image(pose), 0, yb, 420, 'b', sx, sy, tilt)
        for j, (dx, dy, r) in enumerate([(120, -330, 34), (175, -270, 20), (90, -250, 14)]):
            s = ease_back(prog(t, WINK + 0.05 + j * 0.06, WINK + 0.3 + j * 0.06), 2.2) * (1 - prog(t, WINK + 1.1, WINK + 1.4))
            if s > 0:
                sparkle(ctx, dx, yb + dy, r * s, 1, PINK if j == 1 else BRAND_C)
    e = ease_out(prog(t, END_CARD, END_CARD + 0.6))
    if e > 0:
        by = S6 + 160 + (1 - e) * 30
        w = text_width('7日間無料で始めよ', 42) + 90
        round_rect(ctx, -w / 2 - 150, by - 48, w, 96, 48)
        ctx.set_source_rgba(*rgb(PRIMARY, e))
        ctx.fill()
        draw_text(ctx, '7日間無料で始めよ', -150, by, 42, 'b', '#ffffff', e)
        draw_image(ctx, image('appstore.png'), w / 2, by, 96, alpha=e)
        draw_text(ctx, '17言語対応 ・ lanclo.app', 0, by + 105, 34, 'm', MUTED, e)
    k = ease_out(prog(t, GOAL_LINE, GOAL_LINE + 0.5))
    draw_parts(ctx, [('1分で', BRAND_C), ('、あんたの声すぐ確認しよや。', INK)], 0, S6 + 400 + (1 - k) * 26, 56, k)


SCENES = [scene_hook, scene_logo, scene_card, scene_radar, scene_langs, scene_tag, scene_final]


def shake(t):
    out = [0.0, 0.0]
    for t0, amp in ((JOLT, 22), (MIMI_LAND, 12)):
        d = t - t0
        if 0 <= d < 0.5:
            k = amp * math.exp(-9 * d)
            out[0] += k * math.sin(d * 71)
            out[1] += k * math.cos(d * 59)
    return out


# ---------- English subtitles (--en) ----------
# (start, end, lines): one per on-screen Japanese line (the Osaka-dialect type), timed to when it is readable.
SUBS = [
    (TYPE_1[0], CARD_2, ['Your English still sounds Japanese.']),
    (CARD_2 + 0.15, MOVE1[0] + 0.15, ['And you can’t hear what’s off yourself.']),
    (Q_IN[0], MOVE2[0], ['What if you could hear native pronunciation', 'in your own voice?']),
    (REC_CLICK, FREEZE, ['My voice']),
    (MODEL_LABEL, MERGE[0], ['The model · sound on']),
    (H_VOICE[0], MOVE3[0] + 0.25, ['Still your voice, just native pronunciation.']),
    (H_RADAR[0], TIP_IN - 0.3, ['Let’s see the gap to your goal from five angles.']),
    (H_TIP[0], MOVE4[0] + 0.25, ['You know which sound to fix, so no more guessing.',
                                 'Next: tongue tip lightly between your teeth.']),
    (LANG_EN, LANG_ALL, ['English, Korean…']),
    (CONVERGE + 0.45, MOVE5[0] + 0.25, ['17 languages.']),  # not while the 15 greetings fill the bottom
    (TAG[0], MOVE6[0] + 0.25, ['With that voice, go be who you want to be.']),
    (END_CARD, DURATION, ['Start free for 7 days.', 'Check your voice in just one minute.']),
]
SUB_SIZE, SUB_LEAD, SUB_BOTTOM = 38, 1.35, 150  # px at 1080 wide, like the Mimi shorts' .sub
EN = False


def subtitles(ctx, t, S):
    for t0, t1, lines in SUBS:
        if t0 <= t < t1:
            ctx.save()
            ctx.scale(S, S)
            lh = SUB_SIZE * SUB_LEAD
            w = max(text_width(s, SUB_SIZE) for s in lines) + 52
            h = lh * len(lines) + 24
            y = H0 - SUB_BOTTOM - h
            round_rect(ctx, (W0 - w) / 2, y, w, h, 22)
            ctx.set_source_rgba(*rgb('#273b4b', 0.88))
            ctx.fill()
            for i, s in enumerate(lines):
                draw_text(ctx, s, W0 / 2, y + 12 + lh * (i + 0.5), SUB_SIZE, 'b', '#ffffff')
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
    if EN:
        ctx.identity_matrix()
        subtitles(ctx, t, S)
    surf.flush()
    stride = surf.get_stride()
    arr = np.ndarray((H, stride // 4, 4), np.uint8, surf.get_data())[:, :W]
    g = GRAIN[int(t * 24) % len(GRAIN)]
    out = np.clip(arr[..., :3].astype(np.int16) + g[..., None], 0, 255).astype(np.uint8)
    return np.dstack([out, arr[..., 3:]])


def main():
    global GRAIN, EN
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--fps', type=int, default=FPS)
    ap.add_argument('--from', dest='t0', type=float, default=0.0)
    ap.add_argument('--to', dest='t1', type=float, default=DURATION)
    ap.add_argument('--still', default='')
    ap.add_argument('--audio', default='')
    ap.add_argument('--en', action='store_true', help='English subtitles')
    a = ap.parse_args()
    EN = a.en
    W, H = int(W0 * a.scale) // 2 * 2, int(H0 * a.scale) // 2 * 2
    GRAIN = [np.random.default_rng(i).integers(-3, 4, (H, W)).astype(np.int16) for i in range(6)]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
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
