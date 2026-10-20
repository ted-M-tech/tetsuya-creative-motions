"""Animatic: previs stills on the shot timeline with real voice clips, placeholder SFX, captions and the end card.

usage: uv run --no-project --with numpy --with pillow python scripts/animatic.py
Writes renders/animatic.mp4 (540x960, 30 fps).
"""
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from shots import TIMELINE, DURATION, OWN_TAIL, OWN_FULL, MODEL_AT  # noqa: E402

W, H, FPS, SR = 540, 960, 30, 48000
PREVIS = ROOT / 'renders/previs'
FONT_B = str(ROOT / 'assets/fonts/ZenMaruGothic-Bold.ttf')


def font(size):
    return ImageFont.truetype(FONT_B, size)


def still(key, cache={}):
    if key not in cache:
        cache[key] = Image.open(PREVIS / f'{key}.png').convert('RGB').resize((W, H), Image.LANCZOS)
    return cache[key]


def zoom(img, k, dx=0, dy=0):
    if k == 1 and not dx and not dy:
        return img
    w, h = int(W / k), int(H / k)
    x, y = (W - w) // 2 + dx, (H - h) // 2 + dy
    return img.crop((x, y, x + w, y + h)).resize((W, H), Image.LANCZOS)


def caption(img, text):
    d = ImageDraw.Draw(img)
    lines = text.split('\n')
    f = font(34)
    widths = [d.textlength(l, font=f) for l in lines]
    bw, bh = max(widths) + 48, 52 * len(lines) + 24
    x0, y0 = (W - bw) / 2, 120
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 26, fill=(255, 255, 255))
    for i, l in enumerate(lines):
        d.text((W / 2, y0 + 12 + 26 + 52 * i), l, font=f, fill='#273b4b', anchor='mm')


def sweat(img, t):
    d = ImageDraw.Draw(img)
    y = 250 + 30 * (t % 1)
    d.ellipse((300, y, 322, y + 30), fill='#7cc3ff')
    d.polygon([(303, y + 8), (311, y - 14), (319, y + 8)], fill='#7cc3ff')


def sparkles(img, t, n=6, cx=W / 2, cy=420, r=250):
    d = ImageDraw.Draw(img)
    for i in range(n):
        a = i / n * 2 * math.pi + t * 1.5
        s = 10 + 8 * math.sin(t * 9 + i)
        x, y = cx + r * math.cos(a), cy + r * 0.8 * math.sin(a)
        d.polygon([(x, y - s * 2), (x + s * 0.5, y), (x, y + s * 2), (x - s * 0.5, y)], fill='#ffd84a')
        d.polygon([(x - s * 2, y), (x, y + s * 0.5), (x + s * 2, y), (x, y - s * 0.5)], fill='#ffd84a')


def rewind(img, u):
    shifted = img.filter(ImageFilter.BoxBlur(6))
    arr = np.asarray(shifted).copy()
    for row in range(0, H, 6):
        arr[row:row + 3] = np.roll(arr[row:row + 3], int(40 * math.sin(row * 0.05 + u * 20)), axis=1)
    out = Image.fromarray((arr * 0.85 + 30).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    d.text((W / 2, H / 2), '3秒前', font=font(56), fill='#ffffff', anchor='mm', stroke_width=4, stroke_fill='#273b4b')
    return out


def end_card(u):
    img = Image.new('RGB', (W, H), '#fbfcfd')
    mimi = Image.open(ROOT / 'assets/brand/success.png').convert('RGBA')
    mh = int(300 * min(1, u * 3))
    if mh > 0:
        mimi = mimi.resize((int(mimi.width * mh / mimi.height), mh), Image.LANCZOS)
        img.paste(mimi, ((W - mimi.width) // 2, 230), mimi)
    mark = Image.open(ROOT / 'assets/brand/mark.png').convert('RGBA').resize((64, 64), Image.LANCZOS)
    img.paste(mark, (150, 575), mark)
    d = ImageDraw.Draw(img)
    d.text((230, 607), 'Lanclo', font=font(60), fill='#273b4b', anchor='lm')
    d.text((W / 2, 660), '自分の声で、ネイティブの発音を。', font=font(26), fill='#5b7f9f', anchor='mm')
    d.rounded_rectangle((95, 700, 445, 770), 35, fill='#344f69')
    d.text((W / 2, 735), '7日間無料ではじめる', font=font(30), fill='#ffffff', anchor='mm')
    badge = Image.open(ROOT / 'assets/brand/appstore.png').convert('RGBA')
    badge = badge.resize((int(badge.width * 56 / badge.height), 56), Image.LANCZOS)
    img.paste(badge, ((W - badge.width) // 2, 795), badge)
    return img


def frame(t):
    for t0, t1, keys, cap, note in TIMELINE:
        if t0 <= t < t1:
            break
    u = (t - t0) / (t1 - t0)
    if not keys:
        return end_card(u)
    i = min(int(u * len(keys)), len(keys) - 1)
    img = still(keys[i])
    if i > 0:  # short crossfade into the next key
        k = min(1, (u * len(keys) - i) / 0.25)
        img = Image.blend(still(keys[i - 1]), img, k)
    jitter = (int(3 * math.sin(t * 60)), 0) if keys[0] in ('S1a', 'S5a') and cap != '3秒前' else (0, 0)
    img = zoom(img.copy(), 1 + 0.04 * u, *jitter)
    if cap == '3秒前':
        return rewind(img, u)
    if 'S4b' in keys and i == 1:
        sweat(img, u)
    if keys[i] in ('S7b', 'S8a', 'S9a', 'S9b'):
        sparkles(img, t)
    if cap:
        caption(img, cap)
    return img


# ---------- sound ----------
def load(name, start=0.0, length=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(ROOT / 'assets/voice' / name)]
    cmd += (['-t', str(length)] if length else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)


def tone(freqs, d, decay=6.0, vel=0.3):
    t = np.arange(int(d * SR)) / SR
    return vel * np.exp(-decay * t) * sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)


def noise(d, vel=0.2, k=0.1):
    n = np.random.default_rng(1).standard_normal(int(d * SR))
    y, acc = np.empty_like(n), 0.0
    for i, v in enumerate(n):
        acc += k * (v - acc)
        y[i] = acc
    return vel * y * np.sin(np.pi * np.arange(len(n)) / len(n))


def mix():
    bus = np.zeros(int(DURATION * SR))

    def at(x, t, g=1.0):
        i = int(t * SR)
        x = x[:len(bus) - i]
        bus[i:i + len(x)] += g * x

    own = load('own.mp3', 0, 2.76)
    at(own[-int((OWN_TAIL[1] - OWN_TAIL[0]) * SR):], OWN_TAIL[0], 0.9)      # opening: the end of her own take
    at(noise(0.3, 0.5, 0.3), 1.0)                                           # rewind whoosh
    at(tone([1200, 1800], 0.12, 30), 1.6)                                   # tap record
    at(own, OWN_FULL, 0.9)
    at(tone([180, 120], 0.35, 9, 0.5), 4.8)                                # pofu
    at(tone([1200, 1800], 0.12, 30), 5.45)                                  # tap model
    at(load('model.mp3', 0, 1.78), MODEL_AT, 0.9)
    for i, f in enumerate([1568, 1976, 2349]):                               # sparkle
        at(tone([f], 0.6, 5, 0.18), 7.5 + i * 0.07)
    at(noise(0.5, 0.35, 0.15), 7.5)                                          # spin
    for i, f in enumerate([1175, 1480, 1760, 2349]):                         # end chime
        at(tone([f], 1.4, 3, 0.2), 12.6 + i * 0.09)
    return bus / (np.abs(bus).max() / 0.9)


def main():
    out = ROOT / 'renders/animatic.mp4'
    wav = ROOT / 'renders/animatic.wav'
    pcm = (mix() * 32767).astype(np.int16)
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', str(wav), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-shortest', str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(int(DURATION * FPS)):
        p.stdin.write(frame(n / FPS).tobytes())
    p.stdin.close()
    p.wait()
    print(out)


if __name__ == '__main__':
    main()
