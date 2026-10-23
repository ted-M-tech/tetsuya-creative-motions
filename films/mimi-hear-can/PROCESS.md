# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- Standing cast rule (kits/mimi-short/cast/README.md): 「なんでちょこちょこ新しいキャラ出てるの？メインキャラは二人。ミミと友達。そこメインで回して。…」

## Steps and decisions

1. Brief from the batch commander ([prompts/00-commander-brief.txt](prompts/00-commander-brief.txt)) and the Notion row (061, team review: “best comment bait of the round”). Episode 1 of a new series, so the layout was rebuilt from films/mimi-disaster-hat/source as a quiz with generic beat ids (hook, play, reveal, rule, ask, end) and the times moved to `source/cues.json`.
2. Cast: Mimi + Friend only, all library poses (Friend `dreamy` listening → `tease` pointing “Aでしょ！” → `shock` → `yay`; Mimi `confident` → `tease` grin → `point` on the rule card → `jump`). The first pick (`friend-puzzled`, `friend-proud`) held a camera and a rice bowl, which read oddly in a quiz; swapped. No codex-p run, no new art.
3. Quiz order: A = “I can't swim.”, B = “I can swim.”, question 「can はどっち？」. The Friend picks A because he heard no t — exactly the trap the rule card explains. The answers appear under the cards only at the reveal.
4. Voice: `own-voice.json` → ownvoice.py, 2 paid generations, 0 regenerations (direction verbatim in own-voice.json: can reduced to a weak k'n with the stress on “swim”; can't with a full, long /æ/ and a soft, barely heard t).

   Acoustic check with Praat (`source/scripts/check_voice.py`; 20 ms frames, F1/F2 over the voiced part, the share of energy above 4 kHz for the k aspiration and the s):

| | k release / aspiration | voiced “can(’t)” (vowel + n) | vowel F1 / F2 | t | F0 on can(’t) vs swim |
|---|---|---|---|---|---|
| `us-can` “I can swim.” | ~40 ms | ~100 ms (0.48–0.57 s) | ~300 / ~1750 Hz (reduced, nasal) | — | ~128 Hz vs 71–90 Hz |
| `us-cant` “I can't swim.” | ~140 ms | ~200 ms (0.64–0.84 s) | ~600 / ~1900 Hz (open /æ/) | ~20–40 ms closure, no audible release | ~80–85 Hz vs ~60–118 Hz (creaky) |

   So “can” is reduced and short (half the length, closed schwa-like vowel, little aspiration) and “can't” has a twice-as-long open /æ/ with a strongly aspirated k and an unreleased t: the contrast the film teaches. One nuance for the owner's ear: the can take has its pitch peak on “can” itself (the reduced syllable is higher than “swim”), while length and vowel quality say “unstressed”. Not regenerated, since the requested check passed; flagged as an open question. Whisper not used.
5. Mix: takes trimmed to speech with heads and tails kept (us-cant 0.28–1.48 s, us-can 0.18–1.06 s of the take); kit bed and levels unchanged; soft taps for the countdown, pofu for the reveal. Measured: voice segments RMS about -13 to -17 dB vs bed-only segments about -25 dB; true peak -1.5 dBFS; integrated -16.6 LUFS after Mix.write's loudnorm (sparse voice, peak-limited).
6. Layout fixes after the first contact sheet: the rule-card subtitle covered Mimi's face, so the rows were tightened, Mimi moved up and right, the rule subtitle cut to two lines; the 「キャン」 punch line ran off the right edge (moved left); the end-card subtitle covered the CTA, so it sits at the top on the end card only. HyperFrames contrast fixes (A orange #d57333, grey #7e90a0). `hyperframes check`: 0 errors.

## Open questions

- Owner's ear on the two takes (is “can” heard as weak enough with its higher pitch?).
- Length 16.1 s (brief ~17 s): kept tight for tempo.
