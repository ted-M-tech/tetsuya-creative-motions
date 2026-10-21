# 声の調整（アクセントもリクエスト）

[English](README.md) · **日本語**

[mimi-voice](../mimi-voice/README.ja.md) の続編。Mimiが自分のAIボイスを聞いて首をかしげる「なんか、ちょっと僕っぽくない…？」→ コピー「AIボイスは アクセントも リクエストできる！」→ 実アプリ（シミュレーター、テスト用データ）の「声の調整」：話し方（落ち着いて／ゆっくり／穏やか）→「発音・話し方のリクエスト」に「イギリス英語っぽく」→「試聴音声を作る」→「すべてのボイス」で聴きくらべ → 同じ文のイギリス英語の試聴音声（イメージ。「試聴音声を作る」は押していない）「Can't I have a bottle of water after the party?」、イギリス英語らしい語（can't / bottle / water / after / party）を発音に合わせて色付け→ 山高帽とティーカップのMimi「……イギリス帰りの僕」、友だち「行ったことないでしょ！」→ エンドカード。19.6秒、1080×1920、60fps。日本語のみ版と英語字幕版の2本。

**声**：オーナー本人がLancloに登録した声のAIボイス（Gemini gemini-3.8-flash-tts）。同じ文を、調整前はアメリカ英語（`us`）、調整後はイギリス英語（`uk`、「イギリス英語っぽく」）で（`source/own-voice.json`）。声のファイルは生体情報なのでGitに入れず Drive `Tuning_assets/own-voice/` に保管。Mimiは女の子だが声はオーナー（男性）の声。

経緯は [PROCESS.md](PROCESS.md)、作り直しは [source/README.md](source/README.md)。
