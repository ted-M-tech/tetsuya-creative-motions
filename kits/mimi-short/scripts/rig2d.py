"""Mimi shorts rig: the Lanclo design/mimi-2d rig2d.py, reading poses from kits/mimi-short/library (sync-library.sh).

Keep the construction identical to the library; changes made here for an episode go back to the library in a PR.
Additions over the library: episode poses by absolute path (add_pose), lip-sync from any voice clip (lipsync),
and build_shots() so an episode's shots.py builds every shot in one call.

usage (one shot): uv run --no-project --with scipy --with pillow --with numpy python kits/mimi-short/scripts/rig2d.py <pose> <act> <frames> [--bg desk|none] [--out DIR]
usage (episode):  see films/<id>/source/scripts/shots.py
"""
import base64
import os
import math
import sys
import xml.etree.ElementTree as E
from pathlib import Path

from PIL import Image
from scipy.spatial import Delaunay

ROOT = Path(__file__).resolve().parent.parent / 'library'   # synced copy of design/mimi-2d
OFFICIAL = ROOT / 'official'
AW, AH, FPS = 1080, 1920, 60
FEET = (480, 1330)          # artboard point where Mimi's feet stand on the desk


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


# ---------- poses ----------
# image: cut-out with transparent background. height: on-screen height of the whole drawing in artboard px,
# tuned so the HEAD reads the same size in every pose (raised ears and arms make the drawing taller).
# Landmarks come from the alpha bounding box.
POSES = {
    'hide': dict(image='poses/hide.webp', height=800),
    'reach': dict(image='poses/reach.webp', height=1230),
    'listen': dict(image=OFFICIAL / 'listening.png', height=1130),
    'droop': dict(image='poses/droop.webp', height=810),
    'hide-reach': dict(image='poses/hide-reach.webp', height=790),
    'peek': dict(image='poses/peek.webp', height=760),
    'perk': dict(image='poses/perk.webp', height=1150),
    'jump': dict(image='poses/jump.webp', height=1150),
    'success': dict(image=OFFICIAL / 'success.png', height=970),
    'master': dict(image=OFFICIAL / 'master.png', height=970),
    'think': dict(image=OFFICIAL / 'thinking.png', height=970),
    'speak': dict(image='poses/speak-closed.webp', alt='poses/speak-open.webp', height=1000),
    'confident': dict(image='poses/confident.webp', height=1000),
    'stunned': dict(image='poses/stunned.webp', height=1180),
}


def add_pose(name, image, height, alt=None):
    """Episode pose not yet in the library (absolute path to its cut-out)."""
    POSES[name] = dict(image=Path(image).resolve(), height=height, **({'alt': Path(alt).resolve()} if alt else {}))


def landmarks(im):
    x0, y0, x1, y1 = im.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox()
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    return dict(bbox=(x0, y0, x1, y1), contact=(cx, y1 - 0.03 * h), head=(cx, y0 + 0.66 * h), ears=(cx, y0 + 0.12 * h),
                paw_l=(cx - 0.18 * w, y0 + 0.68 * h), paw_r=(cx + 0.2 * w, y0 + 0.66 * h), neck=(y0 + 0.64 * h, y0 + 0.76 * h))


def keys(anim, target, props):
    obj = el('KeyedObject', anim, objectId=target)
    for prop, pairs in props.items():
        kp = el('KeyedProperty', obj, propertyKey=prop)
        for f, v in pairs:
            k = el('KeyFrameDouble', kp, frame=f, value=round(v, 4), interpolationType='cubic')
            el('CubicEaseInterpolator', k, x1=.35, y1=0, x2=.25, y2=1)


def build(shot, spec, out, bg='desk'):
    P = POSES[spec['pose']]
    im = Image.open(ROOT / P['image']).convert('RGBA')
    W, H = im.size
    L = landmarks(im)
    x0, y0, x1, y1 = L['bbox']
    S = P['height'] / (y1 - y0)
    ox, oy = FEET[0] - L['contact'][0] * S, FEET[1] - L['contact'][1] * S

    def A(x, y):
        return ox + x * S, oy + y * S

    r = el('Rive', version='1', kind='fragment')
    a = el('Artboard', r, name='Mimi 2D', id='0:2', width=AW, height=AH, styleId='0:3', defaultStateMachineId='0:7')
    el('LayoutComponentStyle', a, id='0:3')
    hp, cp = A(*L['head']), A(*L['contact'])
    head = el('RootBone', a, id='0:40', name='Head', x=hp[0], y=hp[1], length=80)
    marks = [('0:41', 'Ears', A(*L['ears'])), ('0:43', 'Left paw', A(*L['paw_l'])), ('0:45', 'Right paw', A(*L['paw_r']))]
    for ident, name, pt in marks:
        el('RootBone', head, id=ident, name=name, x=pt[0] - hp[0], y=pt[1] - hp[1], length=50)
    el('RootBone', a, id='0:44', name='Contact', x=cp[0], y=cp[1], length=30)
    binds = [('0:40', hp)] + [(i, pt) for i, _, pt in marks] + [('0:44', cp)]
    n0, n1 = L['neck']
    ear_y = L['ears'][1]

    def weight(x, y):
        h = 1 - smooth((y - n0) / (n1 - n0))
        ear = smooth((ear_y + 0.25 * (y1 - y0) - y) / (0.25 * (y1 - y0)))
        paws = [1 - smooth((math.hypot(x - px, y - py) - 0.04 * W) / (0.08 * W)) for px, py in (L['paw_l'], L['paw_r'])]
        w = [h * (1 - ear), h * ear, 0, 0, 1 - h]
        for j, paw in enumerate(paws):
            f = paw * .5
            w = [v * (1 - f) for v in w]
            w[2 + j] += f
        pairs = [(i + 1, v) for i, v in enumerate(w) if v > 1e-5]
        pairs = sorted(pairs, key=lambda p: -p[1])[:4]
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
    def skin(ident, asset, name, opacity=1):
        image = el('Image', a, id=ident, name=name, assetId=asset, opacity=opacity)
        mesh = el('Mesh', image, triangleIndexBytes=vi(tri))
        for i, (x, y) in enumerate(pts):
            px, py = A(x, y)
            v = el('ContourMeshVertex' if i < len(border) else 'MeshVertex', mesh, x=px, y=py, u=x / W, v=y / H)
            idx, val = weight(x, y)
            el('Weight', v, indices=idx, values=val)
        sk = el('Skin', mesh)
        for bone, pt in binds:
            el('Tendon', sk, boneId=bone, tx=pt[0], ty=pt[1])

    if 'alt' in P:  # lip-sync: the open-mouth drawing sits on top and is shown by opacity keys
        skin('0:51', '0:62', f'{spec["pose"]} • alt', opacity=0)
    skin('0:50', '0:60', f'{spec["pose"]} • skin')
    if bg != 'none':
        el('Image', a, name='Background • desk', assetId='0:61', x=AW / 2, y=AH / 2)  # first sibling draws on top: background last

    n = spec['frames']
    anim = el('LinearAnimation', a, name=shot, id='0:6', fps=FPS, duration=n, loopValue='oneShot')
    spec['act'](anim, hp, cp, n)
    sm = el('StateMachine', a, id='0:7', name='Play')
    layer = el('StateMachineLayer', sm)
    el('AnyState', layer, x=0, y=-180)
    el('ExitState', layer, x=200, y=-180)
    entry = el('EntryState', layer, x=-180, y=0)
    el('StateTransition', entry, stateToId='0:9')
    el('AnimationState', layer, id='0:9', animationId='0:6', reset='true', x=100, y=0)
    rel = lambda f: os.path.relpath(ROOT / f, out)
    el('ImageAsset', r, id='0:60', name=spec['pose'], file=rel(P['image']))
    if bg == 'desk':
        el('ImageAsset', r, id='0:61', name='desk', file=rel('backgrounds/desk.webp'))
    elif bg != 'none':
        el('ImageAsset', r, id='0:61', name='plate', file=rel(Path(bg).resolve()))
    if 'alt' in P:
        el('ImageAsset', r, id='0:62', name=spec['pose'] + ' alt', file=rel(P['alt']))
    E.indent(r)
    out.mkdir(parents=True, exist_ok=True)
    E.ElementTree(r).write(out / 'scene.rml', encoding='unicode')
    (out / 'rive.yaml').write_text(f'name: {shot}\n')
    print(f'{shot}: pose {spec["pose"]}, {len(pts)} vertices, {n} frames')


# ---------- performance helpers (frames at 60 fps; bone props: 15 rotation, 90 x, 91 y) ----------
def track(n, fn, step=2):
    return [(f, fn(f)) for f in list(range(0, n, step)) + [n]]


def body(anim, hp, cp, n, dy=lambda f: 0, squash=lambda f: 0, rot=lambda f: 0, dx=lambda f: 0):
    """Whole-body move: dy lifts both roots (hop); squash pushes the head down (>0) or up (<0) against the feet."""
    keys(anim, '0:40', {90: track(n, lambda f: hp[0] + dx(f)), 91: track(n, lambda f: hp[1] + dy(f) + squash(f)),
                        15: track(n, rot)})
    keys(anim, '0:44', {90: track(n, lambda f: cp[0] + dx(f)), 91: track(n, lambda f: cp[1] + dy(f))})


def bone_rot(anim, ident, n, fn):
    keys(anim, ident, {15: track(n, fn)})


def wave(f, period, amp, phase=0.0):
    return amp * math.sin(2 * math.pi * f / period + phase)


def spring(f, f0, amp, period=14, decay=0.08):
    return 0.0 if f < f0 else amp * math.exp(-decay * (f - f0)) * math.cos(2 * math.pi * (f - f0) / period)


def breathe(f):
    return wave(f, 90, 3)


# ---------- performances ----------
def act_hide(anim, hp, cp, n):
    """Embarrassed shiver: fast small head jitter, slight hunch, ears lagging, paws pressing in."""
    env = lambda f: 0.6 + 0.4 * math.sin(math.pi * min(f, 60) / 60)
    body(anim, hp, cp, n, squash=lambda f: 6 * smooth(f / 12), rot=lambda f: wave(f, 5, 0.045) * env(f), dx=lambda f: wave(f, 5, 5) * env(f))
    bone_rot(anim, '0:41', n, lambda f: wave(f - 1.5, 5, -0.07))
    bone_rot(anim, '0:43', n, lambda f: wave(f, 5, 0.03, 1))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 5, -0.03, 2))


def act_reach(anim, hp, cp, n):
    """Lean back, then reach and tap the screen at frame 26."""
    lean = lambda f: -8 * smooth(f / 10) + 16 * smooth((f - 10) / 14) - 8 * smooth((f - 30) / 12)
    body(anim, hp, cp, n, dx=lambda f: lean(f) * 0.6, rot=lambda f: lean(f) * 0.004, squash=lambda f: spring(f, 26, 5, 10))
    bone_rot(anim, '0:45', n, lambda f: -0.25 * smooth(f / 10) + 0.45 * smooth((f - 10) / 14) - 0.2 * smooth((f - 26) / 6))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 26, 0.06, 12))


def act_listen(anim, hp, cp, n):
    """Calm listening: slow head tilt toward the phone, one ear twitch, breathing."""
    body(anim, hp, cp, n, squash=breathe, rot=lambda f: 0.05 * smooth(f / 40))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 30, 0.08, 10))


def act_droop(anim, hp, cp, n):
    """Deflate: the head sinks into the body, a long slow sag, a small sigh at the end."""
    body(anim, hp, cp, n, squash=lambda f: 22 * smooth(f / 40) + wave(f, 70, 2), rot=lambda f: -0.03 * smooth(f / 40))
    bone_rot(anim, '0:41', n, lambda f: 0.06 * smooth(f / 50))


def act_hide_reach(anim, hp, cp, n):
    """Still hiding, a paw blindly pokes the screen at frame 22."""
    body(anim, hp, cp, n, squash=lambda f: 6, rot=lambda f: wave(f, 6, 0.02), dx=lambda f: 10 * smooth((f - 8) / 12) + wave(f, 6, 2))
    bone_rot(anim, '0:45', n, lambda f: 0.25 * smooth((f - 6) / 14) - 0.12 * smooth((f - 22) / 6))


def act_peek(anim, hp, cp, n):
    """Peek: a small rise, the head leans toward the voice, the ear lifts."""
    body(anim, hp, cp, n, squash=lambda f: -8 * smooth(f / 20), rot=lambda f: 0.04 * smooth(f / 24))
    bone_rot(anim, '0:41', n, lambda f: -0.06 * smooth(f / 16))


def act_perk(anim, hp, cp, n):
    """Pop: squash, overshoot stretch, settle; ears spring."""
    body(anim, hp, cp, n, squash=lambda f: 14 - 14 * smooth(f / 4) + spring(f, 4, -26, 16, 0.09))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 4, 0.12, 14, 0.07))


def act_jump(anim, hp, cp, n):
    """Hop: crouch, launch, airborne arc, land with squash."""
    arc = lambda f: math.sin(math.pi * max(0, min(1, (f - 6) / 26)))
    body(anim, hp, cp, n, dy=lambda f: -150 * arc(f),
         squash=lambda f: 16 * smooth(f / 6) - 16 * smooth((f - 6) / 4) - 10 * math.sin(math.pi * max(0, min(1, (f - 8) / 22))) + spring(f, 32, 16, 10))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 6, -0.1, 12) + spring(f, 32, 0.1, 12))


def act_success(anim, hp, cp, n):
    """Fist pump twice with a small bounce."""
    body(anim, hp, cp, n, squash=lambda f: -6 * abs(math.sin(math.pi * f / 26)), rot=lambda f: wave(f, 52, 0.02))
    bone_rot(anim, '0:45', n, lambda f: -0.12 * abs(math.sin(math.pi * f / 26)))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 26, 0.05, 1))


def act_master(anim, hp, cp, n):
    """Pleased idle: gentle sway, breathing, ear sway."""
    body(anim, hp, cp, n, squash=breathe, rot=lambda f: wave(f, 120, 0.03))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 120, 0.05, 0.8))


def mouth_open_frames(start_f, clip='model.mp3', length=1.78, threshold=0.28):
    """Frames (60 fps, from start_f) that show the open mouth: syllable peaks of the her-voice model.
    The pattern is saved to scripts/lipsync-model.json so the rig rebuilds without the voice file (not in Git)."""
    import json
    import subprocess
    import numpy as np
    cache = ROOT / 'lipsync-model.json'
    if not (ROOT / 'assets/voice' / clip).exists():  # voice clips are not in Git: use the cached pattern
        opens = json.loads(cache.read_text())['opens']
        return [(start_f + i * 4, o) for i, o in enumerate(opens)]
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ROOT / 'assets/voice' / clip), '-t', str(length), '-ac', '1', '-ar', '6000',
                          '-f', 's16le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(float)
    hop = 6000 // 15                                  # 15 mouth decisions per second
    rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
    rms /= rms.max()
    local = np.convolve(rms, np.ones(5) / 5, mode='same')          # open on syllable peaks, not on loudness alone
    opens = [bool(v > threshold and v >= local[i]) for i, v in enumerate(rms)]
    for i in range(1, len(opens)):                                  # never hold the mouth open for more than two steps
        if opens[i] and opens[i - 1] and i > 1 and opens[i - 2]:
            opens[i] = False
    cache.write_text(json.dumps({'clip': clip, 'step_frames': 4, 'opens': opens}) + '\n')
    return [(start_f + i * 4, o) for i, o in enumerate(opens)]


def act_practice(anim, hp, cp, n):
    """Shadowing: she speaks along with the her-voice model (mouth follows its loudness), then a proud little nod."""
    body(anim, hp, cp, n, squash=breathe, rot=lambda f: wave(f, 40, 0.025))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 20, 0.04))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 24, 0.05))
    flaps = mouth_open_frames(12)
    seq = [(0, 0)] + [(f, 1 if o else 0) for f, o in flaps if f < n] + [(min(n, flaps[-1][0] + 4), 0), (n, 0)]
    obj = el('KeyedObject', anim, objectId='0:51')
    kp = el('KeyedProperty', obj, propertyKey=18)
    for f, v in seq:
        el('KeyFrameDouble', kp, frame=f, value=v, interpolationType='hold')


def act_think(anim, hp, cp, n):
    """Reads the result: a slow tilt, then two convinced nods (head dips) from frame 40."""
    nod = lambda f: 14 * max(0.0, math.sin(math.pi * (f - 40) / 14)) if 40 <= f < 68 else 0.0
    body(anim, hp, cp, n, squash=lambda f: breathe(f) + nod(f), rot=lambda f: 0.05 * smooth(f / 30) - 0.05 * smooth((f - 40) / 20))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 40, 0.06, 14) + spring(f, 54, 0.06, 14))


def lipsync(anim, start_f, voice, cache, length=None, threshold=0.28):
    """Key the open-mouth skin (0:51) on syllable peaks of a voice clip from start_f. The pattern is cached next to
    the episode (cache) so the shot rebuilds when the voice file is missing."""
    import json
    import subprocess
    import numpy as np
    voice, cache = Path(voice), Path(cache)
    if voice.exists():
        cmd = ['ffmpeg', '-v', 'error', '-i', str(voice)] + (['-t', str(length)] if length else []) + ['-ac', '1', '-ar', '6000', '-f', 's16le', '-']
        x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.int16).astype(float)
        hop = 6000 // 15
        rms = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) for i in range(0, len(x) - hop, hop)])
        rms /= rms.max()
        local = np.convolve(rms, np.ones(5) / 5, mode='same')
        opens = [bool(v > threshold and v >= local[i]) for i, v in enumerate(rms)]
        for i in range(2, len(opens)):
            if opens[i] and opens[i - 1] and opens[i - 2]:
                opens[i] = False
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({'clip': voice.name, 'step_frames': 4, 'opens': opens}) + '\n')
    opens = json.loads(cache.read_text())['opens']
    obj = el('KeyedObject', anim, objectId='0:51')
    kp = el('KeyedProperty', obj, propertyKey=18)
    seq = [(0, 0)] + [(start_f + i * 4, 1 if o else 0) for i, o in enumerate(opens)] + [(start_f + len(opens) * 4, 0)]
    for f, v in seq:
        el('KeyFrameDouble', kp, frame=f, value=v, interpolationType='hold')


def build_shots(shots, out_root, bg='desk'):
    """shots: {name: dict(pose=, act=callable, frames=)} -> out_root/<name>/ Rive projects."""
    for name, spec in shots.items():
        build(name, spec, Path(out_root).resolve() / name, spec.get('bg', bg))


ACTS = {'hide': act_hide, 'reach': act_reach, 'listen': act_listen, 'droop': act_droop, 'hide-reach': act_hide_reach,
        'peek': act_peek, 'perk': act_perk, 'jump': act_jump, 'success': act_success, 'practice': act_practice,
        'think': act_think, 'master': act_master}

if __name__ == '__main__':
    args = sys.argv[1:]
    pose, act, frames = args[0], args[1], int(args[2])
    bg = args[args.index('--bg') + 1] if '--bg' in args else 'desk'
    out = Path(args[args.index('--out') + 1]).resolve() if '--out' in args else ROOT / 'rive' / f'{pose}-{act}'
    build(f'{pose}-{act}', dict(pose=pose, frames=frames, act=ACTS[act]), out, bg)
