# period-tracker-app

## ブランチ命名規則
基本構造: {領域} + {目的} + {内容}

領域:
- fe: フロントエンド
- be: バックエンド
- doc: ドキュメント

目的:
- feat: 新機能開発
- fix: バグ修正
- chore: その他の変更

例:
- fe/feat/chat-ui
- be/feat/auth

## Commitメッセージ / Pull Requestのタイトル　命名規則

目的（feat, fix, chore）: 内容を簡潔に記述

ex） feat: チャットUIの修正
ex） fix: api通信のバグを修正


## ブランチの作成
ブランチを作成する前に、以下のコマンドを実行してブランチを作成してください。

```bash
git pull origin main
git checkout -b {領域}/{目的}/{内容}
```
## ブランチの削除
マージ後のブランチは削除する。

```bash
git branch -d {ブランチ名}
```
