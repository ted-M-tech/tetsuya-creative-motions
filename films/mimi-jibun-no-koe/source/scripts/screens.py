"""Draw the phone screens used in previs/animation.  usage: uv run --no-project --with pillow python scripts/screens.py"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = str(ROOT / 'assets/fonts/ZenMaruGothic-Bold.ttf')


def f(size):
    return ImageFont.truetype(FONT, size)


def draw(kind):
    W, H = 600, 1200
    img = Image.new('RGB', (W, H), '#fbfcfd')
    d = ImageDraw.Draw(img)
    d.text((W / 2, 110), 'Lanclo', font=f(56), fill='#273b4b', anchor='mm')
    d.rounded_rectangle((50, 200, W - 50, 520), 36, fill='#eaf1f6')
    d.text((W / 2, 300), 'Could you let me know', font=f(34), fill='#344f69', anchor='mm')
    d.text((W / 2, 360), "if you're available?", font=f(34), fill='#344f69', anchor='mm')
    if kind == 'rec':
        d.ellipse((W / 2 - 130, 760, W / 2 + 130, 1020), fill='#e5484d')
        d.text((W / 2, 1080), '録音', font=f(44), fill='#273b4b', anchor='mm')
    elif kind == 'play':
        d.rounded_rectangle((60, 700, W - 60, 900), 44, fill='#eef2f5')
        d.text((W / 2, 800), '▶ 録音した声', font=f(52), fill='#273b4b', anchor='mm')
        for i in range(24):  # playback waveform
            h = 30 + 50 * abs(__import__('math').sin(i * 1.3))
            x = 90 + i * 18
            d.rounded_rectangle((x, 1000 - h / 2, x + 9, 1000 + h / 2), 4, fill='#9fb0bd')
    else:
        d.rounded_rectangle((60, 640, W - 60, 800), 40, fill='#eef2f5')
        d.text((W / 2, 720), '▶ 自分の声', font=f(48), fill='#596875', anchor='mm')
        d.rounded_rectangle((60, 850, W - 60, 1010), 40, fill='#344f69')
        d.text((W / 2, 930), '▶ 自分の声のお手本', font=f(44), fill='#ffffff', anchor='mm')
        d.text((W / 2, 1080), '自分の声 → ネイティブの発音', font=f(30), fill='#5b7f9f', anchor='mm')
    out = ROOT / f'renders/previs/screen-{kind}.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


for k in ('rec', 'play', 'model'):
    draw(k)
