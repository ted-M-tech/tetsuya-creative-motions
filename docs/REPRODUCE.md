# 動かす・作り替える

## ギャラリーを観る

Python 3とNode.js 24を用意します。リポジトリ直下で `npm run dev`。http://localhost:4173 を開きます。完成動画はsite/media/に別途配置します。READMEにファイル名を記載しています。

## 映像を編集する

各作品のsource/が独立したHyperFramesプロジェクトです。Node.js 24、FFmpeg、Chromeを用意してください。

```sh
cd films/lanclo/source
npm ci
npm run dev -- --background
```

ビジュアルソース・作品に使ったイラスト・フォントは収録しています。ナレーション・音楽・効果音はGitに含めないため、クローン直後の状態では音付きの完全再現になりません。各作品のMEDIA.jsonに、必要なファイルの相対パスを記載しています。許諾を持つ音源を配置し、必要に応じてindex.htmlのタイミングを調整します。

```sh
npm run check
npm run render -- --quality delivery --output renders/rebuilt.mp4
```

HyperFramesは保存時の版を固定しています。更新時はチェックしてからレンダーしてください。モデル・フォント・OS・エンコーダーの違いにより、生成音声や出力のバイト列は同一とは限りません。

## AIへ渡す順番

1. 作品のPROMPT.md：全体の目的と構成
2. styles/warm-illustrated-keynote/STYLE.md：見た目と演出
3. NARRATION.md：セリフ
4. TTS-PROMPTS.json：音声生成に使った演技指示
5. TIMING.json：音声の実測尺に基づく映像配置

個人の登録音声IDはYOUR_CONSENTED_VOICE_IDに置換しています。自分が利用できる音声に設定してください。APIキーは環境変数等で管理し、Gitに入れません。
