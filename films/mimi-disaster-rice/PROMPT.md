# PROMPT (consolidated; not the original request)

Make Lanclo SNS short #039 “Pronunciation Disasters 3 - Rice / Lice”, episode 3 of “Pronunciation Disasters” (Japanese learners' classic mix-ups that sound rude), in the pilot's format (films/mimi-disaster-sit).

- Hook on screen from frame 1 (Japanese): “毎日シラミ 食べてます” って言ってた
- Scene: a homestay dinner: a shiba-inu learner proudly says “I eat rice every day” and it comes out as “lice”; the sheep host dad recoils, scratching his head. Mimi bursts out of a rice bowl with crossed chopsticks.
- The learner line and the model line are the owner's own registered Lanclo voice (ownvoice.py): `learner` with a custom style that clearly produces the wrong word, `us` for the right one (see source/own-voice.json). Other characters: Kokoro English.
- The rude word is audible but censored on screen with ★.
- Comparison card: “R と L で、ごはんが虫に”; right column the slip (舌先が歯ぐきに つくと lice), left column the model (舌はどこにも つけない), front-view mouth icons that look like lips.
- A tiny real Lanclo moment: today's lesson in the simulator (QA fixture data, a capture-only tweak puts the episode's sentence and flagged word in; QA labels never visible), お手本 = your own voice.
- Then the fixed line, the end card 「自分の声で、ネイティブの発音を。」 and the 「7日間無料ではじめる」 tap.
- Mimi's first person in Japanese is 「僕」. 15–20 s, comedic tempo, BGM about 21 dB under the voice, SFX quiet. Two cuts: Japanese only and English subtitles.
