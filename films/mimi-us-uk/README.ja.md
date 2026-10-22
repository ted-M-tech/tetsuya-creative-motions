# アメリカ英語とイギリス英語、同じ僕の声で（聞き分けクイズ）

[English](README.md) · **日本語**

[mimi-tuning](../mimi-tuning/README.ja.md)（#23 声の調整）のクイズ形式のスピンオフ。1コマ目から同じMimiが2人「A VS B」、フック「アメリカ英語とイギリス英語 / 同じ僕の声で言ってみた」。「イギリス英語はどっち？」で A・B が同じ文「I can't park the car by the water.」を話す（どちらもオーナー本人がLancloに登録した声のAIボイス。A＝イギリス英語、B＝アメリカ英語）。友だち「ぜったい Bでしょ！」と3・2・1 →「正解は A！」、友だち「えっ」→ A をもう一度、can't／park／car／water を発音に合わせて色付け、「can't =「カーント」」「r を言わない」「t がくっきり」。実アプリ（シミュレーター、テスト用データ、mimi-tuning の録画を再利用）：「声の調整」→「落ち着いて」→「発音・話し方のリクエスト」に「イギリス英語っぽく」。Mimi「AもBも、僕の声だよ」、友だち「耳がだまされた…！」→ エンドカード。18.9秒、1080×1920、60fps。日本語のみ版と英語字幕版の2本。

**声**：オーナー本人がLancloに登録した声（Gemini gemini-3.8-flash-tts、`kits/mimi-short/scripts/ownvoice.py` の `uk` と `us`）。声のファイルは生体情報なのでGitに入れず Drive `US_UK_assets/own-voice/` に保管。

経緯は [PROCESS.md](PROCESS.md)、作り直しは [source/README.md](source/README.md)。
