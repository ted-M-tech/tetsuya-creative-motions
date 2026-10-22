# 2Dキャラクターアニメ制作ガイド

[English](2D-CHARACTER-ANIMATION.md) · **日本語**

承認済みの2Dキャラクターを、その絵柄のまま動かして縦型ショートにする手順です。Mimi（Lanclo）のシリーズ（`films/mimi-*/`）で通した流れをまとめています。各作品に `PROCESS.md`（制作過程）、`PROMPT.md`、`source/README.md`（作り直す手順）があります。最初の1本は「自分の声、むり」（[films/mimi-jibun-no-koe](../films/mimi-jibun-no-koe/PROCESS.md)）。共通部品は [Mimiショート共通キット](../kits/mimi-short/README.md)。3Dの手順は [3Dキャラクター制作ガイド](3D-CHARACTER-WORKFLOW.ja.md)。

## 2Dと3Dの使い分け

| | 2D（このガイド） | 3D |
|---|---|---|
| 向いている | 表情と感情、ブランドの絵柄そのまま、短いショートの量産、アプリでの再利用（Rive） | 振り向き、カメラの回り込み、立体の空間 |
| Mimiでの判断 | 同じ3ポーズを3D・3Dトゥーン・2Dで比べ、依頼者が2Dを「明らかに一番」と判断 | 正本は残し、回り込みが要る回と参照に使う |

Duolingoもアプリ内のキャラクターは2DのRive。3Dは2Dに見せるために使っている。

## 動かし方は2通り

| | Riveの骨（初期の作品） | ポーズの差し替え＋GSAP（今の標準） |
|---|---|---|
| やり方 | ポーズごとに網と骨を入れ、キーで演技、1コマずつ書き出してHyperFramesに置く | 切り抜いたポーズ（WebP）をHyperFramesの編集に直接置き、拍ごとにポーズを差し替え、GSAPで潰れ・弾み・揺れ・すべり・ポップを付ける |
| 作品 | jibun-no-koe、think-sink、michi、nikki、shashin、daily、action-add（swipeはRiveのショット1つ） | roleplay、debate、voice、tuning、frozen-abroad、quitter、watching、発音ディザスターほか大半 |
| 向いている | 体の連続した演技や、キャラクター自身の口パクが要るショット | シリーズの量産、書き出しなしの時間調整、複数のキャラクターが並ぶ場面 |

まずポーズの差し替えで作り、止まって見えるところだけRiveのショットを足す。

## 道具

| 道具 | 役割 | 入れ方 |
|---|---|---|
| Codex（`codex-p`） | 公式の絵柄でポーズ・表情・背景を描く、レビュー | `codex-p exec --image a.png,b.png - < prompt.txt` |
| HyperFrames | GSAPのタイムライン1本で字幕・UI・効果・締めを合成、`npx hyperframes check`、書き出し、Kokoroの音声（`npx hyperframes tts`） | Claudeは hyperframes 系スキル、Codexは公式プラグイン |
| ffmpeg / ImageMagick / Python | 切り抜き、動画化、音のミックス | `brew install ffmpeg imagemagick`、`uv` |
| Xcodeのシミュレーター | 実際のアプリの録画 | Xcode |
| Rive CLI（Riveのときだけ） | 骨で動かす2Dアニメ、1コマずつの書き出し | `brew install --cask rive-app/tap/rive-cli`、`rive update`。書式はAIの学習より新しいので `rive docs` / `rive schema` を引く |

## 手順

1. **話と冒頭**：秒数つきの節目の表にする（下の「話の型」）。商品の機能はアプリのコードで先に確かめ、あるものだけを見せる。
2. **ポーズ**：まずライブラリと前の回のポーズを使う。新しいポーズは codex-p に毎回キャストの絵を添付して描く（ひな形は [cast/README.md](../kits/mimi-short/cast/README.md)）。同じ線・色・頭身・小物の向き・同じ斜めの向き・同じ縮尺・白背景・文字なし、を明記。
3. **切り抜く**：`kits/mimi-short/scripts/cutout.sh`（白背景を四隅から塗りつぶして透明化、余白をトリム、WebP）。背景は1080×1920に。カウンターの手前は背景から切り出してキャラクターの前に重ねられる。
4. **大きさをそろえる**：絵の高さでなく頭の大きさで拡大率を決め、足を同じ位置に置く（キットの背景は足の位置が (480, 1330)）。
5. **声とアプリの録画**（下の節）。
6. **音**：`scripts/mix.py` で合図の表から `sfx.Mix` を組む。時刻は `hf/index.html` と共通。
7. **合成**：`kits/mimi-short/stage.sh <hf>` でキットの見た目（`hf/kit.css`、`hf/kit.js`）・ブランド・フォントを入れ、ポーズ・字幕・吹き出し・スマホ・カード・締めを1本のGSAPタイムラインで時刻どおりに出す。
8. **確認と書き出し**：`npx hyperframes check`、主要なコマ、最後に別のAIのレビュー、音は通しで聴く。`kits/mimi-short/render-cuts.sh <hf> <name>` で2本を書き出す。

Riveで作るときは3〜7の間に：リグ（格子＋ドロネーの網、位置からウェイト、5本の骨：頭・耳・左右の手・接地）、口パク（口を開けた絵を音節の山でだけ表示、`rig2d.lipsync()`）、コマごとに `rive --screenshot --advance=N`（`scripts/render_rive.sh`）。落とし穴：先に書いた要素が手前に描かれる／`--screenshot` は1回の呼び出しで1コマ／書き出しは不透明／不透明度のキーは property 18、骨の回転は15、位置は90 / 91。例：[films/mimi-think-sink](../films/mimi-think-sink/PROCESS.md)。

## キャスト

シリーズのキャストは [kits/mimi-short/cast/](../kits/mimi-short/cast/README.md) で固定。メインの2人（Mimiと友だち）が話を回し、Androidのうさぎがたまに出る。ほかの役（ネイティブ、店員、デートの相手など）は少人数の共通キャスト（くまのブルーノ、アヒルのピッパ、ねこのココ。Kokoroの声もそれぞれ固定）が演じる。1回のために新しいキャラクターを作らない。増やすときは先に依頼者に提案する。役ごとの衣装は可。Lancloだけの文字の決まりもそこにある（Mimiの日本語の一人称は「僕」）。

## 声

- **共通キャストやほかの役**：Kokoro をローカルで。`npx hyperframes tts "<せりふ>" -v <声> -o assets/voice/<file>.wav`（各回の `source/scripts/voices.sh`）。このWAVはGitに入れる。Kokoroの日本語は崩れたので、日本語のせりふは吹き出しと字幕にする。
- **学習者とお手本の英語**：オーナー本人がGemini TTSに登録した声。`kits/mimi-short/scripts/ownvoice.py` と各回の `own-voice.json`。アクセントは `us`・`uk`・`learner`（日本人の初心者）・`native`（`language` を付ける）。`style` で指示を差し替えられる（例：間違った語をはっきり言う学習者）。声は本人の生体データなので、WAVはGitに入れずその回のDriveのフォルダだけに置く。Gitには `own-voice.receipt.json`（文・指示・ハッシュ。声IDなし）。1回の呼び出しが本人の声の有料生成なので、必要なせりふだけ作る（できているものは飛ばす。作り直しは `--force <id>`）。
- **言い間違いの確認**：文字起こしは証拠にならない。Whisperは言語モデルが間違った語を正しい語に直してしまう。Whisperは単語の時刻を測るだけにし、音そのもの（Praatのフォルマント、摩擦音の周波数の重心、silencedetectで語の始まり）で確かめ、人の耳で聴く。例：[mimi-disaster-coke](../films/mimi-disaster-coke/PROCESS.md) の各テイクの記録、[mimi-tuning](../films/mimi-tuning/PROCESS.md) のアメリカ英語とイギリス英語の確認。

## 実際のアプリを見せるとき

製品をシミュレーターで、QA用のデモデータ（個人データなし、毎回同じ画面）で動かし、機能を操作するUIテストを流しながら録る：`kits/mimi-short/app-capture/capture.sh <walkthrough.swift> <置き換えるUITestsのファイル> <Class/testMethod> <out.mov>`。アプリの作業コピーとビルドはキャッシュされるので、時間がかかるのは初回だけ。

- **撮影用だけのパッチ**：デモデータで話に要る画面が出ないとき（別の場面のせりふ、連続30日など）は、文字で一致させる小さなパッチを書き `PATCH=<file>` で渡す。`apply-patch.py` が撮影用の作業コピーにだけ当て、撮影後に戻す。アプリにはコミットしない。撮影ごとに `PATCH` を消す（`env -u PATCH`）。
- **共有のシミュレーター**：ほかのセッションも同じ端末を使うので、録画中はロックを取る：`until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done` → 録画 → `rmdir /tmp/lanclo-capture.lock`。画面が変わっていなければ前の回の録画（Drive）を使ってよい。
- `app-capture/cut.sh` が可変フレームレートの録画を60 fpsにそろえて切る。各回の `scripts/app_track.sh` に、作品の時刻に合わせて測った時間を書く。
- デモデータだけの文字（「デモデータ」、QA用の題名）は編集で隠す。伝えたい1点は寄りと大きなカードで出す。録画が不安定な画面（ホーム画面のウィジェット、ロック画面）は、アプリのコードと文言どおりにHTMLで描き、コピーカードに注記する。例：[mimi-frozen-abroad](../films/mimi-frozen-abroad/PROCESS.md)、[mimi-quitter](../films/mimi-quitter/PROCESS.md)、[mimi-shashin](../films/mimi-shashin/PROCESS.md)。

## 話の型

- **フックが先**：フックの文字は1フレーム目から出し、1.5秒以内に止める。全体15〜25秒、速いテンポ。そのあと、自分ごとの失敗 → 実際のアプリで解決 → オチ → 締め。
- **オチが先**（発音ディザスター）：1フレーム目がオチ（Mimiの反応、★で伏せた語、モノのギャグ）、巻き戻し、そこから言い間違い → 凍る → 口のカード（正しい音と間違った音の唇と舌、両方の声）→ アプリのレッスン → 言い直し。節目の表と回ごとに替えるもの：[films/mimi-disaster-sit/README.md](../films/mimi-disaster-sit/README.md#series-template-episodes-26)。
- **2本の書き出し**：日本語だけと英語字幕つき（`.sub` のクリップを `<body class="no-subs">` で隠す）。どちらも `render-cuts.sh`。
- **音**：主役は声。テーマBGMは声の間は下げ、効果音はやわらかく小さく。大きな音は使わない。声のない作品は、キットのloudnormでなく作品全体に1つのゲインにすることがある（[mimi-watching](../films/mimi-watching/PROCESS.md)）。
- **締め**：`k.end(at)` のあと `k.tapCta(at + 0.6)` でCTAのボタンをタップ。音は `sfx.pochi()`。
- **画面**：字幕は上部。下端約400 pxはSNSのボタン用に空ける。端末の中のUIは雰囲気で、意味は大きなラベルで伝える。顔は隠さない。

## 自分のキャラクターでシリーズを作る

キットはLanclo用だが、型はそのまま使える。`kits/mimi-short/` を `kits/<シリーズ名>/` に写して、次を差し替える。

| 差し替えるもの | キットの場所 |
|---|---|
| キャラクターのライブラリ | `library/`（ポーズ、小道具、背景、公式の絵）。`sync-library.sh` はLancloのものを取ってくるので、自分のものは手で入れるか自分用の同期を書く |
| キャスト | `cast/`：メインのキャラクターと参照画像、共通キャストとKokoroの声、キャラクターの特徴を書いた codex-p のひな形 |
| ブランド | `brand/`（締めのキャラクター、ロゴ、ストアのバッジ）と、`hf/kit.js`（`endCard`、`tapCta`）・`hf/kit.css` の締めの文字 |
| BGM | `library/bgm/everyone-get-up.mp3`（`scripts/sfx.py` の `THEME`。Gitに入れない。テーマ曲は別の権利）。無ければ `sfx.py` がコードで作る伴奏を流す |
| 声 | 全員Kokoro、または `ownvoice.py` の代わりに自分の登録した声（アカウントと声の名前はLancloのもの） |

最小の手順：

1. 承認済みのキャラクターの絵をそろえる：参照シートを `cast/`、ポーズを `library/poses/` に。
2. 1フレーム目にフックを置いた節目の表を書く。
3. 足りないポーズを参照から codex-p で描き、`cutout.sh`。
4. 声を作る（Kokoroか自分の声）。アプリを見せるなら録画する。
5. 前の回の `source/`（例：`films/mimi-disaster-sit/source/`）を `films/<id>/source/` に写し、中の `kits/mimi-short` のパスを自分のキットに向け、`scripts/mix.py` と `hf/index.html` の絵・せりふ・時刻を差し替える。
6. `stage.sh`、`npx hyperframes check`、`render-cuts.sh`。レビューして通しで聴く。
7. 記録を残す（下）。

## 記録の残し方

作品ごとに `films/<id>/` に：`README.md` / `README.ja.md`（何の作品か、形式、完成ファイルの場所）、`PROMPT.md`（統合プロンプト）、`PROCESS.md`（依頼者の指示の原文、判断、修正、学んだこと）、`prompts/`（codex-p のプロンプトとログの原文）、`process/`（軽いJPGのコマ）、`source/`（作り直すコマンドを書いた `README.md`、スクリプト、絵、`own-voice.json` と受領記録、編集）、`CREDITS.md`。Gitに入れないもの：本人の声のWAV、シミュレーターの録画、`hf/assets/`、書き出し、BGM。置き場所は source の README に書く（Lancloでは、Notion Content CalendarのIDで名付けたその回のDriveのフォルダ）。[作品を追加する](ADDING-A-FILM.md)。

## エージェントで回す

LancloのSNSショートは、企画から固定ルール、制作、Drive・Notionへの納品、確定、YouTubeと作品集への公開、まとめて作るときの進め方までを、1つのエージェント用スキルにまとめている：[lanclo-sns-short](../skills/lanclo-sns-short/SKILL.md)。
