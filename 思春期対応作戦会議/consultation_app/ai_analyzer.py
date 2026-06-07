#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# AI分析ロジック（Gemini API使用）

import json
import re
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL


def _get_client():
    """Gemini クライアントを返す"""
    return genai.Client(api_key=GEMINI_API_KEY)


def analyze_section_2a(transcript: str) -> dict:
    """
    セッション記録からセクション2-A（クライアント記録）を生成
    Returns: {"課題": {"summary": "", "detail": ""}, ...}
    """
    client = _get_client()

    prompt = f"""以下のセッション記録を読んで、クライアント記録（セクション2-A）を生成してください。

【セッション記録】
{transcript}

【必ず以下のJSON形式のみで返してください（コードブロックや説明文は不要）】
{{
  "課題": {{
    "summary": "クライアントが自覚している課題とセッション内で浮かび上がった問題点を1行で",
    "detail": "具体的な背景と経過を2〜3行で詳しく"
  }},
  "やってみようと思ったこと": {{
    "summary": "クライアントが実践しようと思ったことを1行で",
    "detail": "具体的なアクションを2〜3行で詳しく"
  }},
  "その他": {{
    "summary": "その他の気になること・自由メモを1行で",
    "detail": "詳細を2〜3行で"
  }},
  "次回フォローアップ予定日": "2〜3週間後が適切な場合は具体的な日付の提案を記載（例：2週間後が目安）"
}}

日本語で出力してください。個人名は含めないでください。"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        text = response.text.strip()
        # JSONブロックが含まれる場合は抽出
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group()
        return json.loads(text)
    except Exception as e:
        return {
            "課題": {"summary": f"（生成エラー: {str(e)}）", "detail": ""},
            "やってみようと思ったこと": {"summary": "", "detail": ""},
            "その他": {"summary": "", "detail": ""},
            "次回フォローアップ予定日": ""
        }


def analyze_section_2b(transcript: str) -> dict:
    """
    セッション記録からセクション2-B（セッション分析）を生成
    Returns: {"理解できたこと": {"summary": "", "detail": ""}, ...}
    """
    client = _get_client()

    prompt = f"""以下のセッション記録を読んで、保健師モモさんの視点でセッション分析（セクション2-B）を生成してください。

【セッション記録】
{transcript}

【必ず以下のJSON形式のみで返してください（コードブロックや説明文は不要）】
{{
  "理解できたこと": {{
    "summary": "このセッションで理解できたことを1行で",
    "detail": "具体的な背景と考察を2〜3行で"
  }},
  "疑問": {{
    "summary": "疑問に思ったことを1行で",
    "detail": "詳細と次回確認したい点を2〜3行で"
  }},
  "対応と迷い": {{
    "summary": "自分の対応への振り返りと迷いを1行で",
    "detail": "具体的な場面と判断の背景を2〜3行で"
  }},
  "クライアントの反応": {{
    "summary": "クライアントの反応の特徴を1行で",
    "detail": "セッション中の印象的な反応を2〜3行で"
  }},
  "次回に向けて": {{
    "summary": "次回に向けた方針を1行で",
    "detail": "確認したいこと・取り組むことを2〜3行で"
  }},
  "調べること": {{
    "summary": "次回までに調べることを1行で",
    "detail": "調べる内容とその理由を2〜3行で"
  }},
  "その他": {{
    "summary": "その他の気づきを1行で",
    "detail": "詳細を2〜3行で"
  }}
}}

日本語で出力してください。個人名は含めないでください。"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group()
        return json.loads(text)
    except Exception as e:
        return {
            "理解できたこと": {"summary": f"（生成エラー: {str(e)}）", "detail": ""},
            "疑問": {"summary": "", "detail": ""},
            "対応と迷い": {"summary": "", "detail": ""},
            "クライアントの反応": {"summary": "", "detail": ""},
            "次回に向けて": {"summary": "", "detail": ""},
            "調べること": {"summary": "", "detail": ""},
            "その他": {"summary": "", "detail": ""}
        }
