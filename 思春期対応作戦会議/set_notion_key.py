#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Notion APIキーを.envに設定するスクリプト

import sys
import io
import os
import re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

print("=" * 50)
print("Notion APIキー設定ツール")
print("=" * 50)
print()
print("NotionのアクセストークンをここにコピペしてEnterを押してください：")
print("（secret_ntn_ で始まる文字列）")
print()

token = input("> ").strip()

if not token:
    print("[ERROR] 何も入力されませんでした")
    input("Enterを押して終了...")
    sys.exit(1)

if not token.startswith("secret_"):
    print(f"[WARNING] トークンが secret_ で始まっていません（入力値: {token[:20]}...）")

print(f"\n入力されたトークン長: {len(token)}文字")

# .envファイルを読み込んで更新
env_path = os.path.join(os.path.dirname(__file__), '.env')

with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()

# NOTION_API_KEYの行を更新または追加
if 'NOTION_API_KEY' in content:
    content = re.sub(r'NOTION_API_KEY=.*', f'NOTION_API_KEY={token}', content)
else:
    content += f'\nNOTION_API_KEY={token}\n'

with open(env_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n[OK] .envファイルに保存しました")

# 接続テスト
import requests
headers = {
    'Authorization': f'Bearer {token}',
    'Notion-Version': '2022-06-28'
}
print("\nNotion接続テスト中...")
res = requests.get('https://api.notion.com/v1/users/me', headers=headers)
if res.status_code == 200:
    print("[OK] 接続成功！Notionに繋がりました。")
else:
    print(f"[ERROR] 接続失敗: {res.json().get('message', '')}")

print()
input("Enterを押して終了...")
