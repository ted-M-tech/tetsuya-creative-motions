# 統合プロンプト（最初の入力の原文ではなく、完成形を作り直すためにまとめたもの）

Lancloの縦型ショート（1080×1920、60fps、20秒、日本語のみ版と英語字幕版の2本）を `kits/mimi-short` と `films/mimi-action-review` の型で作る。

- 0–2.7秒（フック、1フレーム目から）：上部キャプション「180秒しゃべり続けたら、口癖がバレた」。Mimiが中央で話している（speak-open/closed の口パク、オーナーの登録音声 `learner` で "It looks really, really nice."）。右にタイマー（0:00、「最大 3:00」、進行バー）。"really" と言うたびに白い札「really」が飛び出して残る。
- 2.7–3.4秒：「▶▶ 早送り」、タイマーが2:50へ、really が4個追加。
- 3.4–8.0秒："And the coffee looks really, really good. Really." で really がさらに3個（計9個）。8.0秒で3:00、タイマーが赤く弾む。
- 8.1–9.1秒：Mimi（confident）「3分、話しきった！」、really の札が消える。
- 9.1–14.1秒：右に実アプリのフィードバック（シミュレーター、`really-take.patch` のテストデータ）：スコア→話した内容（really が9回並ぶ文字起こし）→個別の改善ポイント（It looks really, really nice. → It looks absolutely lovely.）。キャプション「話したことを、AIがぜんぶ文字にして…」→「口癖まで、見つかる。」、Mimi（stunned）が跳ね、赤いバッジ「really ×9回」。
- 14.1–16.1秒：友だち（friend-tsukkomi）「really、言いすぎ！」、Mimi（fluster）「……really？」。
- 16.1–18.8秒：個別の修正の「改善した言い方」"It looks absolutely lovely." をオーナーの登録音声（`us`）でMimiが言う。タグ「改善した言い方」、キャプション「自分では気づけない口癖に、気づける。」
- 18.8–20.0秒：エンドカード、0.45秒後にCTAタップ。
- 英語字幕は全ての日本語に。機能・数字はアプリのコードで確かめたものだけ。Mimiの一人称は「僕」。
