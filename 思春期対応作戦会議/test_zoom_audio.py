#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

# Windows文字コード対策
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# .envファイルを読み込む
load_dotenv()

def test_zoom_audio_transcription():
    """Zoomセッション音声ファイルの書き起こし＋AI分析テスト"""

    # ファイルパス
    audio_file_path = r"C:\Users\Owner\Documents\Zoom\2026-06-05 14.02.20 不登校相談（かたやま りえさん）\audio1297228026.m4a"

    # ファイルの存在確認
    if not Path(audio_file_path).exists():
        print(f"[ERROR] ファイルが見つかりません: {audio_file_path}")
        return

    print(f"[OK] ファイル確認: {Path(audio_file_path).name}")
    print(f"[OK] ファイルサイズ: {Path(audio_file_path).stat().st_size / 1024 / 1024:.2f} MB")

    # Anthropic クライアント初期化
    client = Anthropic()

    print("\n[START] 処理開始\n")

    # ステップ1: 音声ファイルの読み込みと書き起こし
    print("[STEP 1] 音声の自動書き起こしを処理中...")

    import base64

    with open(audio_file_path, 'rb') as f:
        audio_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Claude APIで音声を処理（書き起こし＋分析）
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """このZoomセッションの音声ファイルから、以下の情報を抽出してください。

【タスク】
1. セッションの内容を簡潔に書き起こす（3～5行）
2. セッション内で出た主要なテーマを3～5個列挙
3. クライアントが述べた課題・悩みを箇条書き（3～5項目）

【フォーマット】
=== 書き起こし概要 ===
[内容]

=== 主要テーマ ===
- テーマ1
- テーマ2
...

=== クライアントの課題 ===
- 課題1
- 課題2
...
"""
                    },
                    {
                        "type": "audio",
                        "media_type": "audio/m4a",
                        "data": audio_data,
                    }
                ],
            }
        ],
    )

    transcription_result = message.content[0].text
    print("\n[OK] 書き起こし完了\n")
    print("=== [STEP 1 RESULT] 書き起こしと分析 ===\n")
    print(transcription_result)

    # ステップ2: セッション分析セクション（2-B）の案を生成
    print("\n\n[STEP 2] セッション分析セクション（2-B）の案を生成中...\n")

    analysis_message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": f"""以下のZoomセッション内容をもとに、セッション分析セクション（2-B）の7項目の案を、パターン①（概要+詳細版）形式で生成してください。

【セッション内容】
{transcription_result}

【出力形式：パターン①（概要+詳細版）】
各項目について、以下のように出力してください：

【項目名】
■ 概要版（1行）
　→ 〇〇について気づいたこと

■ 詳細版（2～3行）
　→ セッション内での具体的な背景、モモさんの考察を含める

---

【必須項目】
1. そのセッションで理解できたこと
2. 疑問に思ったこと
3. 自分の対応と迷い
4. クライアントの反応
5. 次回に向けてどうするか
6. 次回までに調べること
7. その他の気づき

各項目を上記形式で出力してください。クライアント名などの個人情報は含めないでください。
"""
            }
        ],
    )

    analysis_result = analysis_message.content[0].text
    print("[OK] 分析完了\n")
    print("=== [STEP 2 RESULT] セッション分析セクション（2-B）の案 ===\n")
    print(analysis_result)

    print("\n\n[SUCCESS] テスト完了しました！")
    print("\n[EVALUATION]")
    print("- 書き起こし精度：確認してください")
    print("- AI分析案の質：確認してください")
    print("- セクション2-Aの案（課題、やってみようと思ったこと）も生成しますか？")

if __name__ == "__main__":
    test_zoom_audio_transcription()
