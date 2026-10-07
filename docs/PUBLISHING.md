# ギャラリーを公開する

公開先は **https://videos.maepace.com/**。Cloudflare Workersの静的アセットでギャラリーと完成MP4を配信します。動画パス `/media/*` だけは小さなWorkerでHTTP Rangeに対応し、途中シークを可能にしています。Worker名は `tetsuya-creative-motions`。ポートフォリオ本体のWorkerとは独立しています。

## 構成

- GitHub：コード、プロンプト、台本、制作ノート、サムネイル。
- 静的ホスティング：site/をビルドしたdist/。ポートフォリオのサブドメインに割り当てる。
- 完成MP4：同じホストのmedia/、または動画配信に使えるオブジェクトストレージ/CDN。

相対URLで書いているためサブドメインにもサブディレクトリにも配置可能です。Custom Domainはwrangler.jsoncで管理します。

## ローカル確認とビルド

```sh
npm run check
npm run dev
npm run build
```

通常ビルドはMP4を除外。完成映像の公開範囲と音源条件を確認したうえで、手元のMP4も含める場合は：

```sh
npm run build -- --include-media
```

公開対象はdist/だけです。声の元録音・登録音声ID・APIキー・分離音声は不要です。完成MP4のGitHub Releasesへの保管は可能ですが、ギャラリーで安定してシークする用途ではRange対応の配信先を用意してください。外部配信する場合はsite/index.htmlのvideo srcを書き換えます。

## GitHub側

READMEのサムネイルと作品ページは相対リンク。ギャラリーからの制作ノートリンクはこのリポジトリのmainを指します。push前はリンク先が存在しないので、公開時に確認してください。README冒頭とGitHub Aboutからギャラリーへ誘導します。

## 更新を公開する

Cloudflareへのログインを確認してから `npm run deploy`。チェック、MP4を含むビルド、静的アセットのデプロイを順に実行します。自動デプロイは設定していません。Gitのpushだけでは動画サイトは更新されません。

完成MP4の保管先はGitHub Releasesの `films` リリース。クローン後は、プロジェクトのルートで次のコマンドから復元できます。

```sh
gh release download films --repo ted-M-tech/tetsuya-creative-motions --dir site/media --pattern '*.mp4'
```

新しい完成版を追加するときは、既存作品を上書きせず新しいファイル名またはリリースを使用してください。

## 動画は静的配信（2026-10-07）

`videos.maepace.com/media/*.mp4` は Workers Static Assets から直接配信します。
`main`、`run_worker_first`、独自Range処理は置きません。旧URLの移動は `site/_redirects` に記述します。
保存・静的リクエストには追加料金がなく、Workerの実行回数を消費しない構成です。
既存アカウントの他サービス・基本料金は別です。R2、Stream、有料変換処理は使いません。

1. 完成MP4をGit管理外の `site/media/` に配置。
2. 各ファイルを25MiB以下にし、Web再生用のH.264/AAC・faststartを推奨。
3. `npm run deploy` で検査・ビルド・公開。
4. 実配信で再生・シーク・旧URLの移動を確認。静的ホストはRange要求に200を返すため、作品詳細ページではMP4全体をfetchし、Blob URLでブラウザ標準プレイヤーへ渡します。最初に読み込み待ちが入り、その後のシークは端末内で処理します。

[料金](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/)

`site/_headers` は作品集のオリジンへのCORSを許可します。再生コードはMaePace側の `src/scripts/static-video.ts`。動画そのもののURLは維持し、公開ファイルの上限はビルドで検査します。
