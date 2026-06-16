# sns-assets

SNS（Instagram / Threads）投稿用の**公開画像**を置くリポジトリ。
`ai_coach_korekara` の投稿画像・アイコン等を保管する。

> ⚠️ ここに置くものはすべて**公開**されます。投稿に使う画像のみを置き、秘密情報・非公開素材は置かないこと。

## 使い方（公開画像URLの作り方）

1. `images/` に画像をアップロード（GitHub の Web 画面でドラッグ&ドロップ、または `git add/commit/push`）
2. その画像の **raw URL** を投稿の `image_url` に使う

raw URL の形式:

```
https://raw.githubusercontent.com/takanorikoyama-dev/sns-assets/main/images/<ファイル名>
```

例: `images/post-2026-06-16.png` を置いた場合 →
`https://raw.githubusercontent.com/takanorikoyama-dev/sns-assets/main/images/post-2026-06-16.png`

## 命名の目安

- アイコン: `icon/avatar.png`
- 投稿画像: `images/post-YYYY-MM-DD.png`（投稿日で識別）

## 注意

- Instagram API は公開URLから画像を取得するため、このリポジトリは **Public** を維持する。
- 画像は JPEG/PNG 推奨。Instagram の推奨は正方形〜縦長（1:1〜4:5）。
