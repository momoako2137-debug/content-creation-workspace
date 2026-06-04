---
globs: "**/*.py"
---

# Python スクリプトルール

## 実行コマンド

```bash
# Google スライド自動生成（要 credentials.json / token.json）
python create_slides.py

# WordPress ページ投稿（要 wp_config.py）
python wp_post.py

# PDF → PPTX 変換
python pdf_to_pptx.py

# Notion 操作（要 notion_config.py）
python notion_setup.py
python notion_add_content.py
```

## 構文チェック（テスト）

```bash
python -m py_compile momokiako/<ファイル名>.py
```

## 設定ファイル（Git 管理外・読み書き禁止）

| ファイル | 用途 |
|---|---|
| `credentials.json` | Google API OAuth 認証情報 |
| `token.json` | Google API アクセストークン（自動生成） |
| `wp_config.py` | WordPress URL・ユーザー・アプリパスワード |
| `notion_config.py` | Notion API トークン |

ひな形は `*.example.py` として Git 管理されている。

## コーディング規則

- コメントは必ず日本語で書く。
- 既存スクリプトを大幅に書き換える前に、方針をモモさんに説明する。
- 新しい外部ライブラリを追加する際は事前に確認を取る。
