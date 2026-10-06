# 初回公開記録

- 日付：2026-10-06
- ギャラリー：https://videos.maepace.com/
- GitHub：https://github.com/ted-M-tech/tetsuya-creative-motions
- 完成動画：https://github.com/ted-M-tech/tetsuya-creative-motions/releases/tag/films
- Cloudflare Worker：tetsuya-creative-motions
- Worker version：abfabb8e-9779-40b7-8e21-6bc3ba8fa364
- 公開方式：CLIによる手動デプロイ。mainへのpushだけではサイトは更新しない。

## 確認

公開用ファイルの個人パス・登録音声ID・APIキーのチェック、Markdownリンク検証、HTTP Rangeの4テストを実行。公開サイトのHTML 200、動画Range 206を確認。Chromeで2本の再生、終盤へのシーク、再生終了、390px幅で横はみ出しがないことを確認。

CloudflareとGoogleの公開DNSで解決を確認。初回検証時はローカルDNSに負のキャッシュが残っていたため、ブラウザ検証では公開DNSで得たIPをホスト解決に指定し、正規ホスト名のHTTPS証明書を検証した。

## MP4のSHA-256

- `lanclo.mp4`: `01bb9c7f8afb8c8ea943329f3ff77008ec0fc7a3d09d620132e0cdb75c7b7450`
- `lanclo-osaka.mp4`: `a60fab03082cc7af99fb56aab20c0e5337c01524ef6bebdb410636318907ef35`
