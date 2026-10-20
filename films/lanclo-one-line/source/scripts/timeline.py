"""Shared beat timings (seconds). Picture and sound both read from here."""

FPS = 60
DURATION = 26.6

# Type beats on the story clock (first cut was timed to a narration take; the timings stayed when it was dropped).
VO = {
    'n1': 0.45,   # 自分の声で、ネイティブの発音を聴けたら？
    'n2': 8.60,   # 声はあなたのまま、発音だけネイティブに。
    'n3': 11.70,  # どこを直すか、5つの視点でわかる。
    'n4': 14.40,  # 苦手がわかると、次の一文が変わる。
    'n5': 17.40,  # 発音、ロールプレイ、写真描写、英語日記。
    'n6': 21.10,  # その声で、なりたい自分へ。
    'n7': 23.30,  # Lanclo。
}
N2_SECOND = 1.38                     # 発音だけネイティブに。
N5_WORDS = [0.0, 0.63, 1.45, 2.70]   # 発音 / ロールプレイ / 写真描写 / 英語日記
N6_SECOND = 1.14                     # なりたい自分へ。

# English comparison clips (cut at the end of "available").
OWN_START, OWN_LEN = 3.60, 2.76
MODEL_START, MODEL_LEN = 6.60, 1.78

HOOK_LAND = 0.17
LOGO_LINE = (0.75, 1.25)
MIMI_HOP = (1.35, 1.85)
CARD_IN = (2.55, 3.25)
MERGE = (8.45, 9.20)
PENT = (11.85, 12.55)
FILL = (12.45, 13.25)
NEXT_CARD = (14.75, 15.25)
NEXT_SENTENCE = 16.35
MIMI_SUCCESS = 15.85
NODES = [VO['n5'] + w for w in N5_WORDS]
TAG = (VO['n6'], VO['n6'] + N6_SECOND)
BREATH = 22.75
MIMI_LAND = 23.20
LOGO2_LINE = (22.95, 23.55)
FANFARE = 23.70
END_CARD = 24.40

# Camera keyframes: (time, x, y, zoom). Holds between moves; eased in between.
CAMERA = [
    (0.00, 0, 40, 1.00),
    (1.70, 0, 40, 1.00),
    (2.10, 0, 260, 1.00),
    (2.45, 0, 260, 1.00),
    (3.30, 2600, 0, 1.00),
    (6.40, 2600, 0, 1.00),
    (7.40, 2600, -10, 1.06),
    (8.40, 2600, -10, 1.06),
    (9.20, 2600, -60, 1.00),
    (11.15, 2600, -60, 1.00),
    (11.95, 5150, -30, 1.00),
    (14.20, 5150, -30, 1.00),
    (14.95, 5650, 0, 0.92),
    (17.05, 5650, 0, 0.92),
    (17.75, 7950, 0, 0.66),
    (20.55, 7950, 0, 0.66),
    (21.30, 10100, 0, 1.00),
    (22.55, 10100, 0, 1.00),
    (23.25, 12000, 60, 1.00),
    (24.40, 12000, 60, 1.00),
    (25.20, 12000, 150, 0.94),
    (DURATION, 12000, 150, 0.94),
]

# Camera moves with a whoosh.
WHOOSHES = [2.45, 11.15, 14.20, 17.05, 20.55, 22.55]

# English subtitles, one per type beat.
SUBS = {
    'n1': "What if you could hear native pronunciation in your own voice?",
    'n2': "Your voice stays yours. Only the pronunciation goes native.",
    'n3': "See what to fix, from five angles.",
    'n4': "Know your weak spots, and your next sentence changes.",
    'n5': "Pronunciation, role-play, picture description, English journal.",
    'n6': "In your voice, toward who you want to be.",
}

# No narration: on-screen Japanese type carries the story. Picture beats above stay on the
# "story clock"; output time maps onto it piecewise (holds give the type reading time).
_W = [(0, 0), (2.0, 2.0), (3.05, 3.6), (7.83, 8.38), (8.0, 8.6), (10.48, 11.08), (10.85, 11.7), (13.08, 13.93),
      (13.3, 14.4), (15.3, 16.4), (15.8, 17.4), (19.07, 20.67), (19.45, 21.1), (24.95, 26.6)]
QUESTION_HOLD = 1.45  # extra output time on the lock-up for the opening question
WARP = [(0, 0), (2.1, 2.1), (2.1 + QUESTION_HOLD, 2.45), (3.05 + QUESTION_HOLD, 3.6)] + \
       [(o + QUESTION_HOLD, st) for o, st in _W[3:]]
QUESTION = (2.25, 2.1 + QUESTION_HOLD + 0.45)  # output time

# English subtitle under each Japanese type beat (output time).
SUB_OUT = {
    'n1': QUESTION,
    'n2': (9.45, 12.0),
    'n3': (12.3, 14.5),
    'n4': (14.75, 16.9),
    'n5': (17.25, 20.4),
    'n6': (20.9, 22.9),
}
OUT_DURATION = WARP[-1][0]


def _map(t, pairs):
    for (a0, b0), (a1, b1) in zip(pairs, pairs[1:]):
        if t <= a1:
            return b0 + (b1 - b0) * (t - a0) / (a1 - a0)
    return pairs[-1][1]


def to_story(t):
    return _map(t, WARP)


def to_out(t):
    return _map(t, [(b, a) for a, b in WARP])
