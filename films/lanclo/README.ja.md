# Lanclo — 自分の声で、毎日の英語を。

**日本語** · [English](README.md)

![Lanclo Daily](../../site/posters/lanclo-daily.jpg)

**1:09 · 1920×1080 · 30fps · 日本語ナレーション / Japanese audio**

自分のAI音声、苦手に合わせた10問、いつものニュース。発音のレッスンが生活に溶け込むまでを描く完成版です。

A Japanese product film about learning with your own AI voice, personalized ten-question lessons, and daily news that becomes English learning material.

[動画と制作ノートをまとめて見る](https://videos.maepace.com/films/lanclo-daily/) · [統合プロンプト](PROMPT.md) · [全台本](NARRATION.md) · [音声入力](TTS-PROMPTS.json) · [編集ソース](source) · [タイミング](TIMING.json) · [出典](CREDITS.md)

## 制作の判断

- 冒頭1秒で問いを提示し、すぐ自分のAI音声という価値を見せる。
- 苦手の分析だけで終わらず、次の10問が自動で組み上がる過程まで可視化。
- 「さらに、いつものニュースも、あなたの英語教材に。」を挟み、機能の羅列を毎日の学習という話につなぐ。
- 研究の見出しは簡潔に、条件と出典は保持。約1.3倍は抑揚テスト得点の伸びの比較。

## 番外編と制作の変遷

r26完成版。以前の[通常版](history/r18)と[大阪弁版](extras/osaka)も保存。大阪弁版は初期版の映像を使った番外編です。

[再編集手順](../../docs/REPRODUCE.md)。分離音声はGitに含めません。必要ファイルは[MEDIA.json](MEDIA.json)。

## 制作ファイル

| ファイル | 内容 |
|---|---|
| [PROMPT.md](PROMPT.md) | 完成形を再制作するための統合指示 |
| [NARRATION.md](NARRATION.md) | 最新版の全台本 |
| [TTS-PROMPTS.json](TTS-PROMPTS.json) | 音声生成時の入力。採用テイクはTIMING.jsonで確認 |
| [TIMING.json](TIMING.json) | シーンと音声の配置 |
| [CREDITS.md](CREDITS.md) | 素材・研究の出典、利用条件 |
| [source/](source/) | 最新版の編集ソース |
| [extras/osaka/](extras/osaka/) | 大阪弁ナレーションの番外編 |
| [history/r18/](history/r18/) | 初期版の制作記録とソース |
