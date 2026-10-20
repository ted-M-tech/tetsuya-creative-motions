"""2D Mimi in Rive: one drawn pose as a continuous skinned mesh with a few bones, plus a short performance.

Follows the approved Lanclo rig (design/mimi-welcome/build_scene.py): grid + Delaunay mesh over the cut-out,
weights from position, Tendons to bones, LinearAnimation on the bones, a state machine that plays it.

usage: uv run --no-project --with scipy python scripts/rig2d.py hook
       rive rive/hook --verify && rive rive/hook --screenshot=renders/hook/f000.png --advance=0
"""
import base64
import math
import sys
import xml.etree.ElementTree as E
from pathlib import Path

from PIL import Image
from scipy.spatial import Delaunay

ROOT = Path(__file__).resolve().parent.parent
AW, AH, FPS = 1080, 1920, 60


def el(tag, p=None, **attrs):
    n = E.Element(tag, {k: str(v) for k, v in attrs.items()})
    if p is not None:
        p.append(n)
    return n


def vi(values):
    b = []
    for v in values:
        while v > 127:
            b.append((v & 127) | 128)
            v >>= 7
        b.append(v)
    return base64.b64encode(bytes(b)).decode()


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def keys(anim, target, props):
    obj = el('KeyedObject', anim, objectId=target)
    for prop, pairs in props.items():
        kp = el('KeyedProperty', obj, propertyKey=prop)
        for f, v in pairs:
            k = el('KeyFrameDouble', kp, frame=f, value=round(v, 4), interpolationType='cubic')
            el('CubicEaseInterpolator', k, x1=.35, y1=0, x2=.25, y2=1)


# ---------- poses: image + bone landmarks in image pixels ----------
POSES = {
    'hide': dict(image='art/hide-cut.png', head=(470, 600), ears=(560, 160), paw_l=(430, 600), paw_r=(720, 580),
                 contact=(480, 890), neck_y=(600, 700)),
}


def build(pose_name, perf):
    P = POSES[pose_name]
    im = Image.open(ROOT / P['image'])
    W, H = im.size
    S = 0.95                                   # image px -> artboard px
    ox, oy = AW / 2 - 60 - P['contact'][0] * S, 1330 - P['contact'][1] * S   # feet on the desk top, left of the phone

    def A(x, y):
        return ox + x * S, oy + y * S

    r = el('Rive', version='1', kind='fragment')
    a = el('Artboard', r, name='Mimi 2D', id='0:2', width=AW, height=AH, styleId='0:3', defaultStateMachineId='0:7')
    el('LayoutComponentStyle', a, id='0:3')
    hp, cp = A(*P['head']), A(*P['contact'])
    head = el('RootBone', a, id='0:40', name='Head', x=hp[0], y=hp[1], length=80)
    marks = [('0:41', 'Ear tips', A(*P['ears'])), ('0:43', 'Left paw', A(*P['paw_l'])), ('0:45', 'Right paw', A(*P['paw_r']))]
    for ident, name, pt in marks:
        el('RootBone', head, id=ident, name=name, x=pt[0] - hp[0], y=pt[1] - hp[1], length=50)
    el('RootBone', a, id='0:44', name='Contact', x=cp[0], y=cp[1], length=30)
    binds = [('0:40', hp)] + [(i, pt) for i, _, pt in marks] + [('0:44', cp)]
    n0, n1 = P['neck_y']

    def weight(x, y):
        h = 1 - smooth((y - n0) / (n1 - n0))                       # head above the neck, contact below
        ear = smooth((P['ears'][1] + 260 - y) / 260)               # top of the ears
        paws = [1 - smooth((math.hypot(x - px, y - py) - 40) / 70) for px, py in (P['paw_l'], P['paw_r'])]
        w = [h * (1 - ear), h * ear, 0, 0, 1 - h]
        for j, paw in enumerate(paws):
            f = paw * .5
            w = [v * (1 - f) for v in w]
            w[2 + j] += f
        pairs = [(i + 1, v) for i, v in enumerate(w) if v > 1e-5][:4]
        tot = sum(v for _, v in pairs)
        vals = [round(v / tot * 255) for _, v in pairs]
        vals[vals.index(max(vals))] += 255 - sum(vals)
        return sum(i << (8 * j) for j, (i, _) in enumerate(pairs)), sum(v << (8 * j) for j, v in enumerate(vals))

    step = 32
    xs = list(range(0, W, step)) + [W]
    ys = list(range(0, H, step)) + [H]
    border = [(x, 0) for x in xs] + [(W, y) for y in ys[1:]] + [(x, H) for x in reversed(xs[:-1])] + [(0, y) for y in reversed(ys[1:-1])]
    bs = set(border)
    pts = border + [(x, y) for y in ys for x in xs if (x, y) not in bs]
    tri = [int(i) for t in Delaunay(pts).simplices for i in t]
    image = el('Image', a, name=f'{pose_name} • skin', assetId='0:60')
    mesh = el('Mesh', image, triangleIndexBytes=vi(tri))
    for i, (x, y) in enumerate(pts):
        px, py = A(x, y)
        v = el('ContourMeshVertex' if i < len(border) else 'MeshVertex', mesh, x=px, y=py, u=x / W, v=y / H)
        idx, val = weight(x, y)
        el('Weight', v, indices=idx, values=val)
    sk = el('Skin', mesh)
    for ident, pt in binds:
        el('Tendon', sk, boneId=ident, tx=pt[0], ty=pt[1])
    el('Image', a, name='Background • desk', assetId='0:61', x=AW / 2, y=AH / 2)  # first sibling draws on top, so the background goes last

    anim = el('LinearAnimation', a, name=perf, id='0:6', fps=FPS, duration=PERFS[perf]['frames'], loopValue='oneShot')
    PERFS[perf]['keys'](anim, hp, cp)
    sm = el('StateMachine', a, id='0:7', name='Play')
    layer = el('StateMachineLayer', sm)
    el('AnyState', layer, x=0, y=-180)
    el('ExitState', layer, x=200, y=-180)
    entry = el('EntryState', layer, x=-180, y=0)
    el('StateTransition', entry, stateToId='0:9')
    el('AnimationState', layer, id='0:9', animationId='0:6', reset='true', x=100, y=0)
    rel = Path('../..') / P['image']
    el('ImageAsset', r, id='0:60', name=pose_name, file=str(rel))
    el('ImageAsset', r, id='0:61', name='desk', file='../../art/bg-desk.png')
    E.indent(r)
    out = ROOT / 'rive' / perf
    out.mkdir(parents=True, exist_ok=True)
    E.ElementTree(r).write(out / 'scene.rml', encoding='unicode')
    (out / 'rive.yaml').write_text(f'name: {perf}\n')
    print(f'{perf}: {len(pts)} vertices, {len(tri) // 3} triangles, 5 bones, {PERFS[perf]["frames"]} frames')


# ---------- performances ----------
def hook_keys(anim, hp, cp):
    """Embarrassed shiver: fast small head jitter with a slight hunch, ear tips lagging, paws pressing in."""
    n = 60
    fr = list(range(0, n + 1, 2))
    shiver = [math.sin(2 * math.pi * f / 5.0) * (0.6 + 0.4 * math.sin(math.pi * f / n)) for f in fr]
    keys(anim, "0:40", {15: [(f, 0.045 * s) for f, s in zip(fr, shiver)],
                        90: [(f, hp[0] + 5 * s) for f, s in zip(fr, shiver)],
                        91: [(f, hp[1] + 6 * smooth(f / 12) - 3 * smooth((f - 40) / 20)) for f in fr]})
    lag = [math.sin(2 * math.pi * (f - 1.5) / 5.0) for f in fr]
    keys(anim, '0:41', {15: [(f, -0.07 * s) for f, s in zip(fr, lag)]})
    keys(anim, '0:43', {15: [(f, 0.03 * math.sin(2 * math.pi * f / 5.0 + 1)) for f in fr]})
    keys(anim, '0:45', {15: [(f, -0.03 * math.sin(2 * math.pi * f / 5.0 + 2)) for f in fr]})


PERFS = {'hook': dict(pose='hide', frames=60, keys=hook_keys)}

if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'hook'
    build(PERFS[name]['pose'], name)
