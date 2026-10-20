"""English journal feature short (9:16). Beat timings in output seconds; picture and sound read from here."""

FPS = 60
DURATION = 22.5

HOOK_LAND = 0.17
QUESTION_IN = 0.55
TITLE_IN = 0.95
LINE_A = (0.95, 1.45)          # underline under the question
MIMI_HOP = (1.65, 2.1)

MOVE1 = (2.0, 2.75)            # to the microphone
MIC_ON = 2.75
H1 = (2.85, 3.3)
REC = (3.0, 5.6)               # waveform and transcript words

MOVE2 = (6.0, 6.75)            # to the corrected journal
CARD2_IN = (6.55, 7.0)
H2 = (6.85, 7.3)
STRIKE = 7.55
WENT = 7.85
SCORES = 8.35                  # + i * SCORE_GAP
SCORE_GAP = 0.13
TIP = 9.1

MOVE3 = (10.0, 10.75)          # to the illustration
H3 = (10.85, 11.3)
DRAW = (10.75, 12.55)
TINT = (12.35, 12.95)
MIMI_ART = 11.0
CAPTION = 12.95

MOVE4 = (14.0, 14.8)           # to the calendar; the picture flies into today
PAST = 14.25                   # + i * PAST_GAP for earlier days
PAST_GAP = 0.11
CELL_LAND = 15.1
H4 = (15.0, 15.45)
PULL = (16.3, 17.6)

MOVE5 = (18.0, 18.7)           # to the lock-up
LOGO_LINE = (18.55, 19.05)
MIMI_LAND = 19.0
FANFARE = 19.45
TAGLINE = 19.35
END_CARD = 19.95

# Camera keyframes: (time, y, zoom). Stations stack downwards; the line runs between them.
S0, S1, S2, S3, S4, S5 = 0, 1800, 3900, 5900, 7950, 9950
CAMERA = [
    (0.0, S0, 1.0), (MOVE1[0], S0, 1.0), (MOVE1[1], S1, 1.0),
    (MOVE2[0], S1, 1.03), (MOVE2[1], S2, 1.0),
    (MOVE3[0], S2, 1.02), (MOVE3[1], S3, 1.0),
    (MOVE4[0], S3, 1.03), (MOVE4[1], S4, 1.0), (PULL[0], S4, 1.0), (PULL[1], S4 + 20, 0.94),
    (MOVE5[0], S4 + 20, 0.94), (MOVE5[1], S5, 1.0), (DURATION, S5, 1.0),
]
WHOOSHES = [MOVE1[0], MOVE2[0], MOVE3[0], MOVE4[0], MOVE5[0]]

# English subtitle under each Japanese type beat.
SUBS = [
    ((0.5, 2.0), "How was your day?"),
    ((2.85, 5.9), "Talk about your day, and it becomes an English journal."),
    ((6.85, 9.9), "Corrected into natural English, with pronunciation tips."),
    ((10.85, 13.9), "Your day, turned into a picture."),
    ((15.0, 17.9), "Days in your voice, lined up on your calendar."),
    ((TAGLINE, DURATION), "Keep today, in English."),
]
