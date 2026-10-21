# 制作の経緯

オーナーの言葉（Notion Content Calendar ID 17 の候補「A」について）：

> A：アクションボタンカチっはいいかな。単体で完結させたい。カチっってなるのは面白い。もっといろんなパターンでやるってモチベにつなげて

- アクションボタンとのつなぎは入れず、カフェ1場面で完結させた。
- 「カチっ」＝固まる面白さを主役に。[mimi-michi](../mimi-michi/PROCESS.md) の氷漬け（ライブラリの `ice` 小道具と `freeze`/`shatter` 効果音）を再利用し、「カチッ!」の文字で見せた。
- 最後は「いろんなパターンで」へのモチベーション：練習して注文はできたのに新しい質問（hot or iced?）でまた固まる → 今度は笑って氷を割り、会話練習のほかの場面（空港・交通・ホテル…）へ。コピー「いろんな場面で、何度でも。」

## 決めたこと

- アプリ画面はシミュレーター録画（`app-capture/RoleplayWalkthrough.swift`、`SituationUITests.swift` と差し替え）。起動引数は `SituationUITests` と同じ `--uitesting --visual-fixtures --qa-situations --qa-situations-loading --qa-roleplay-language en`、UIは日本語。会話練習 → カフェ → 「飲み物を注文する」（`roleplay-en-food`）は現在 `SituationPracticeScreen`（AIの会話相手とヒント）に入る。
- 画面の文言はすべて実際の表示から：会話相手、ヒントがほしい？、"I'd like a latte, please." / "A coffee, please."、返答を準備しています…、シチュエーション完了。フィクスチャの返答（"A latte for here, with milk, nothing else, card, no receipt." など）は合成データなので、アプリが言い方を「添削」するとは言わず「言い方に迷ったらヒントで確認」とした。左上の「デモデータ」はマスク。
- 録画はフィクスチャの読み込みに6秒あるので、ローディングは0.5秒だけ使い、ほかも短く切った（`scripts/app_track.sh` に計測値）。カテゴリ画面の「クリア 1/16」「1/2」は共有シミュレーターの以前の実行の進捗がそのまま出ている。
- カフェで話される英語は声あり（Kokoro：店員 `bf_emma`、Mimi `af_heart`。Mimiの注文はのちにオーナー本人の声へ）。日本語はすべて吹き出し・字幕。英語の吹き出しには小さく日本語訳を添えた。
- 新しい絵：カフェの背景、エプロン姿の友だち（問いかけ・笑顔）、氷を割って飛び出すMimi（`prompts/01-codex-cafe-barista.txt`）。店員はカウンターの後ろに立たせるため、背景からカウンター前面を切り出して重ねた。

## 学び

- 公式の `master.png` は透明部分に薄いアルファが残っていて `-trim` が効かない。アルファを閾値処理してから切り出す（`source/README.md`）。
- HyperFrames では時間指定した要素の中に時間指定した `<video>` を入れるとエラー。外側は時間なしの入れ物にして GSAP の opacity で出し入れした。

承認後、新しいポーズ（barista-ask / barista-smile / grin）とカフェ背景は Lanclo の `design/mimi-2d` へPRする候補。

## 声をオーナー本人の声に（2026-10-21）

> 今まで英語で発音シーンがあった動画、この声で変えて。010以外。

- Kokoroの代役をやめ、学習者とお手本の英語を、Lancloに登録したオーナー本人の声（Gemini `gemini-3.8-flash-tts`、`kits/mimi-short/scripts/ownvoice.py`）に差し替えた。Kokoroはほかの登場人物だけに残す。
- 練習のあとの注文 "For here, please. I'd like a latte!" を `us` で（それまでは af_heart）。発話10.75–12.83秒（元は10.75–12.73秒）で、次の店員の質問（13.0秒）の前に収まるので、ほかの時間は変えていない。店員（bf_emma）はKokoroのまま。
- 声のWAVは本人の生体データなので、公開リポジトリには入れない。Gitには `source/own-voice.json`（文とアクセント）と `own-voice.receipt.json`（文・指示・ハッシュ。声IDなし）だけ。WAVはDriveの `Roleplay_assets/own-voice/`。
