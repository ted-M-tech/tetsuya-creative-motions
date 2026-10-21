"""App intro (9:16, 30 s). Beat timings in output seconds; picture and sound read from here.

The Notion script (Content Calendar「アプリ紹介」) fixes the beats; narration lines start at VO.
"""

FPS = 60
DURATION = 30.0

# The LP clips play to the end of "available" (the word list's end time clips its tail).
OWN_CLIP = 3.02
MODEL_CLIP = 1.98

# Narration line starts (Mimi's Kansai take at 1.2x, cut by scripts/intro_vo.sh).
VO = {
    'v1': 0.95,  # その英語、まだ日本語に聞こえとるわ。
    'v2': 3.2,  # でも、どこが変なんか、自分では聞こえへん。
    'v3': 5.95,  # もし、自分の声でネイティブの発音が聴けたらどうやろ？
    'v4': 14.25,  # これがあんたのゴールの声や。聴くだけでも、ちょっと楽しいやろ。
    'v5': 17.05,  # ゴールと今の差を、5つの視点で。
    'v6': 19.15,  # 直す音がわかるから、もう迷わへん。
    'v7': 21.0,  # 英語も、韓国語も、17言語。毎日、ゴールに近づけんで。
    'v8': 24.75,  # その声で、なりたい自分へ行こう。
    'v9': 26.5,  # Lanclo、7日間無料。
    'v10': 27.88,  # 1分で、あんたの声すぐ確認しようや。
}

# S0 hook: the line is typed character by character
TYPE_1 = (0.1, 0.16)  # (start, per char) その英語、
TYPE_2 = (1.4, 0.1)  # まだ日本語に聞こえてます。
JOLT = 2.75  # the full stop lands; the frame jolts
CARD_2 = 3.1  # どこが変か、自分では聞こえない。

# S1 logo and the question
MOVE1 = (5.6, 6.05)
LOGO_LINE = (5.95, 6.45)
MIMI_POP = 6.4
Q_IN = (6.3, 6.9)

# S2 the recording card: own voice, a beat of silence, the model
MOVE2 = (7.85, 8.35)
CARD_IN = (8.05, 8.45)
REC_CLICK = 8.15
OWN_START = 8.5  # own.mp3, OWN_CLIP long
FREEZE = 11.55
MODEL_LABEL = 11.75  # お手本 + 音声ON
MODEL_START = 12.1  # model.mp3, MODEL_CLIP long
MERGE = (14.15, 14.85)
H_VOICE = (14.25, 15.15)  # 声はあなたのまま、 / 発音だけネイティブに。

# S3 the five-angle radar, then the tip
MOVE3 = (16.6, 17.15)
PENT = (16.9, 17.5)
FILL = (17.45, 18.1)  # to 61
GAIN = (18.3, 18.95)  # 61 -> 67
H_RADAR = (17.1, 17.5)
TIP_IN = 19.1
H_TIP = (19.15, 19.55)

# S4 17 languages: a greeting per language around a count-up (v7: 英語も 21.0, 韓国語も 21.76, 17言語 22.4, 毎日 23.37)
MOVE4 = (20.85, 21.4)
RING = (21.2, 21.75)
LANG_EN = 21.1
LANG_KO = 21.8
LANG_ALL = 22.4  # the other 15 pop, LANG_STEP apart
LANG_STEP = 0.05
CONVERGE = 23.4  # greetings gather into the ring; the line leaves downwards

# S5 tagline
MOVE5 = (24.2, 24.75)
TAG = (24.75, 25.45)

# S6 lock-up, end card, wink
MOVE6 = (26.1, 26.55)
LOGO2_LINE = (26.4, 26.9)
MIMI_LAND = 26.7
FANFARE = 27.15
END_CARD = 27.4
WINK = 27.9
GOAL_LINE = 28.0
TAIL = None  # no "available?" tail: the closing line runs to the end

# Camera keyframes: (time, y, zoom). Stations stack downwards; the line runs between them.
S0, S1, S2, S3, S4, S5, S6 = 0, 1900, 3800, 6000, 8300, 10500, 12300
CAMERA = [
    (0.0, S0, 1.0), (CARD_2 - 0.05, S0, 1.02), (MOVE1[0], S0, 1.02), (MOVE1[1], S1, 1.0),
    (MOVE2[0], S1, 1.02), (MOVE2[1], S2, 1.0), (FREEZE, S2, 1.0), (MODEL_START + 1.9, S2, 1.04),
    (MERGE[0], S2, 1.04), (MERGE[1], S2, 1.0),
    (MOVE3[0], S2, 1.0), (MOVE3[1], S3, 1.0), (MOVE4[0], S3, 1.02), (MOVE4[1], S4, 1.0),
    (MOVE5[0], S4, 1.02), (MOVE5[1], S5, 1.0), (MOVE6[0], S5, 1.03), (MOVE6[1], S6, 1.0),
    (WINK, S6, 1.0), (DURATION, S6, 1.05),
]
WHOOSHES = [MOVE1[0], MOVE2[0], MOVE3[0], MOVE4[0], MOVE5[0], MOVE6[0]]
