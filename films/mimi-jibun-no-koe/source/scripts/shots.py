"""Shot list for 「自分の声、むり」 (15 s, 9:16). Times in seconds. Shared by previs.py and animatic.py.

Opening A: start on the emotional peak (Mimi hiding in her ears) with a relatable question, then rewind.
"""
HIDE = dict(earL=(20, -30, 70), earR=(115, 0, 25), nod=18, squash=-0.12, lean=8, eyes=1.0)
LISTEN = dict(armR=(-35, 0, 20))
DROOP = dict(earL=(-25, 0, 20), earR=(-35, 0, -25), nod=10, eyes=0.25, squash=-0.05)
PEEK = dict(earL=(5, -20, 50), earR=(100, 0, 20), nod=10, squash=-0.08, eyes=1.0)
PERK = dict(earL=(55, 0, 0), earR=(0, 0, 0), nod=-6, squash=0.08, eyes=1.25, tilt=-4)
SPIN = dict(earL=(40, 0, -10), earR=(-15, 0, 0), z=0.35, spin=110, squash=0.1, eyes=1.25, armL=(-60, 0, 0), armR=(-60, 0, 0))
PUMP = dict(earL=(35, 0, 0), armR=(-150, 0, -35), tilt=-12, eyes=1.2, squash=0.05)

HERO = dict(earL=(40, 0, 0), armR=(-60, 0, 30), tilt=-14, eyes=1.15, squash=0.04)

# key: cam, pose, screen
KEYS = {
    'S1a': dict(cam='cu', pose=HIDE),
    'S3a': dict(cam='insert', pose=dict(armR=(-75, 0, 45), tilt=-14), screen='rec'),
    'S4a': dict(cam='med', pose=LISTEN, screen='play'),
    'S4b': dict(cam='med', pose=DROOP, screen='play'),
    'S5a': dict(cam='cu', pose=HIDE, screen='play'),
    'S6a': dict(cam='insert', pose=dict(HIDE, armR=(-75, 0, 45)), screen='model'),
    'S7a': dict(cam='cu', pose=PEEK, screen='model'),
    'S7b': dict(cam='cu', pose=PERK, screen='model'),
    'S8a': dict(cam='wide', pose=SPIN, screen='model'),
    'S9a': dict(cam='med', pose=PUMP, screen='model'),
    'S9b': dict(cam='med', pose=HERO, screen='model'),
}

# (start, end, keys shown in order, caption, note). Revised after the Codex storyboard review:
# value earlier (model voice at 5.7 s), record vs playback shown on the phone, shorter second hide,
# separate listening from celebrating, no loop bridge back to the sad pose.
TIMELINE = [
    (0.0, 1.0, ['S1a'], '自分の英語、聴ける？', 'own voice tail; tremble'),
    (1.0, 1.3, ['S1a'], '3秒前', 'rewind whoosh'),
    (1.3, 2.0, ['S3a'], '', 'tap record'),
    (2.0, 4.2, ['S4a', 'S4b'], '', 'playback screen; own voice from the top; ears droop, = ='),
    (4.2, 4.6, ['S4b'], '自分の声、むり…', 'caption leads the hide'),
    (4.6, 5.1, ['S5a'], '自分の声、むり…', 'pofu'),
    (5.1, 5.7, ['S6a'], '', 'paw taps 自分の声のお手本'),
    (5.7, 6.4, ['S7a'], '自分の声のお手本', 'model voice starts; peek'),
    (6.4, 7.5, ['S7b'], '私の声なのに…！', 'ears shoot up'),
    (7.5, 8.2, ['S8a'], '', 'spin hop; sparkle sting'),
    (8.2, 12.6, ['S9a', 'S9b'], '声はあなたのまま、\n発音だけネイティブに。', 'fist pump, then hero pose with the phone'),
    (12.6, 15.0, [], 'END', 'Lanclo end card'),
]
DURATION = 15.0
OWN_TAIL = (0.0, 1.0)      # last second of the own-voice clip under the opening
OWN_FULL = 2.0             # own voice starts with the playback screen
MODEL_AT = 5.7
