# LPスキルをまとめて導入・更新する

Python 3.9以降とGitがあれば、次の3つを同時に導入できます。

- `lp-create`：制作工程・検証・再現記録
- `impeccable`：主なデザイン支援
- `design-taste-frontend`：Taste Skillによる別案・批評

```sh
git clone https://github.com/ted-M-tech/tetsuya-creative-motions.git
cd tetsuya-creative-motions
python3 scripts/install-lp-skills.py
```

導入先は `$CODEX_HOME/skills`、未設定なら `~/.codex/skills`。別環境では `--dest /path/to/skills` を指定します。新しいターン／セッションから読み込ませてください。導入後は `$lp-create` で依頼します。3つを毎回実行するのではなく、必要なものを読みます。

更新も同じコマンドです。

```sh
git pull --ff-only
python3 scripts/install-lp-skills.py
python3 scripts/install-lp-skills.py --check
```

`--check` は通信せず、配布側で固定した内容との一致を確認します。初回と更新時はGitHubへ接続します。一致済みなら再ダウンロードしません。第三者スキルは公式リポジトリから直接取得し、ライセンス・NOTICEを保持します。取得するスキルのインストールスクリプトやCLIは、この導入処理では実行しません。

## 既に同名スキルがある場合

この導入ツールが管理していない版や、導入後に編集したファイルは上書きしません。既存版をバックアップしてから再実行するか、別の `--dest` で試してください。`--force` はありません。管理中の未編集版だけを更新し、通常の更新失敗時は旧版に戻します。OS停止などで `.lp-bundle-install.lock` が残った場合は、別の導入プロセスが動いていないことを確認してからその空ディレクトリを削除してください。

## 自動導入しないもの

Product Design等のプラグイン、agent-reach、ブラウザ本体、サービスへのログインは別です。利用環境にあれば必要に応じて使い、なければ利用可能な調査・ブラウザツールで進めます。これらがないだけで基本のLP制作を止めない設計です。

Impeccable本体は利用時に公式CLIの初回取得を行う場合があります。今回固定するのはスキルパッケージです。実際に使う外部CLI・ブラウザ・AIモデルの版は制作記録に別途残します。導入成功は、それらの起動や出力品質まで保証するものではありません。

## 配布側の保守

[lockファイル](../skills/lp-bundle.lock.json)が依存関係の正本です。常に最新版へ追従する仕組みにはしません。

1. `lp-create`を変更するか、更新したい公式スキルの`ref`を完全なコミットSHAへ変更する。
2. `python3 scripts/install-lp-skills.py --refresh-lock`でハッシュを更新する。この操作はインストールしない。
3. 一時ディレクトリを`--dest`に指定して導入・再実行・`--check`を確認し、`npm test`と`npm run check`を実行する。
4. 内容とライセンスをレビューしてソース・lockを一緒に公開する。

利用者側は上記の更新コマンドだけで、確認済みの組み合わせへ揃えられます。個々の作品が使った過去のスキル版・プロンプトの記録は書き換えません。
