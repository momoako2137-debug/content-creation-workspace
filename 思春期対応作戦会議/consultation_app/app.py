#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 個別相談カルテ管理アプリ - Flask本体

import sys
import io
import threading
import webbrowser

# Windows文字コード対策
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import re

UUID_RE = re.compile(
    r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$',
    re.IGNORECASE
)
from notion_handler import (
    get_clients, get_client, get_sessions, get_communications,
    save_session, save_communication, add_client, debug_communications_raw
)
from ai_analyzer import analyze_section_2a, analyze_section_2b
from config import APP_HOST, APP_PORT

app = Flask(__name__)


# ===========================
# 画面ルート
# ===========================

@app.route("/")
def index():
    """クライアント一覧"""
    clients = get_clients()
    return render_template("index.html", clients=clients)


@app.route("/client/<client_id>")
def client_detail(client_id):
    """クライアント詳細"""
    client = get_client(client_id)
    if not client:
        return redirect(url_for("index"))
    result = get_sessions(client_id)
    if isinstance(result, tuple):
        sessions, session_db_id = result
    else:
        sessions, session_db_id = [], None
    communications = get_communications(client_id)

    # セッション記録とコミュニケーション記録を日付順に混ぜる
    timeline = []
    for s in sessions:
        timeline.append({"type": "session", "date": s.get("date") or "", "data": s})
    for c in communications:
        timeline.append({"type": "comm", "date": c.get("date") or "", "data": c})
    timeline.sort(key=lambda x: x["date"] or "", reverse=True)

    return render_template(
        "client.html",
        client=client,
        timeline=timeline,
        session_db_id=session_db_id,
        communications=communications
    )


@app.route("/client/<client_id>/new")
def new_session(client_id):
    """新規セッション入力フォーム"""
    client = get_client(client_id)
    if not client:
        return redirect(url_for("index"))
    result = get_sessions(client_id)
    if isinstance(result, tuple):
        sessions, session_db_id = result
        session_count = len(sessions) + 1
    else:
        session_db_id = None
        session_count = 1
    return render_template(
        "new_session.html",
        client=client,
        session_db_id=session_db_id,
        session_count=session_count
    )


# ===========================
# API ルート
# ===========================

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """AI分析実行"""
    data = request.get_json()
    transcript = data.get("transcript", "")
    if not transcript:
        return jsonify({"error": "字幕テキストが空です"}), 400

    try:
        section_2a = analyze_section_2a(transcript)
        section_2b = analyze_section_2b(transcript)
        return jsonify({
            "success": True,
            "section_2a": section_2a,
            "section_2b": section_2b
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/save_session", methods=["POST"])
def api_save_session():
    """セッションをNotionに保存"""
    data = request.get_json()
    session_db_id = data.get("session_db_id", "")
    session_count = int(data.get("session_count", 1))
    session_date = data.get("session_date", "")
    analysis = data.get("analysis", "")
    messages = data.get("messages", "")

    if not session_db_id:
        return jsonify({"error": "セッションDBが見つかりません"}), 400

    # 日付バリデーション
    try:
        datetime.strptime(session_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "日付の形式が正しくありません"}), 400

    success, result = save_session(
        session_db_id, session_count, session_date,
        analysis, messages
    )
    if success:
        return jsonify({"success": True, "url": result})
    else:
        return jsonify({"error": result}), 500


@app.route("/api/save_communication", methods=["POST"])
def api_save_communication():
    """コミュニケーション記録をNotionに保存"""
    data = request.get_json()
    client_id = data.get("client_id", "")
    title = data.get("title", "").strip()
    date = data.get("date", "")
    route = data.get("route", "その他")
    direction = data.get("direction", "受信（相手から）")
    status = data.get("status", "対応済み")
    content = data.get("content", "").strip()
    memo = data.get("memo", "").strip()

    if not client_id or not title or not date:
        return jsonify({"error": "クライアントID・タイトル・日付は必須です"}), 400

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "日付の形式が正しくありません"}), 400

    success, result = save_communication(client_id, title, date, route, direction, status, content, memo)
    if success:
        return jsonify({"success": True, "url": result})
    else:
        return jsonify({"error": result}), 500


@app.route("/api/debug_comms/<client_id>")
def api_debug_comms(client_id):
    """デバッグ用：コミュニケーションDBの生データ確認"""
    return jsonify(debug_communications_raw(client_id))


@app.route("/api/debug_client/<client_id>")
def api_debug_client(client_id):
    """デバッグ用：クライアントページのプロパティ型確認"""
    import requests as req
    from notion_handler import _headers
    from config import NOTION_VERSION
    resp = req.get(f"https://api.notion.com/v1/pages/{client_id}", headers=_headers())
    if resp.status_code != 200:
        return jsonify({"error": resp.status_code, "body": resp.text})
    props = resp.json().get("properties", {})
    return jsonify({k: {"type": v.get("type"), "value": v} for k, v in props.items()})


@app.route("/api/add_client", methods=["POST"])
def api_add_client():
    """新規クライアントをNotionに追加"""
    data = request.get_json()
    name = data.get("name", "")
    first_date = data.get("first_date", "")
    issue = data.get("issue", "")
    route = data.get("route", "その他")
    child_grade = data.get("child_grade", "")

    if not name:
        return jsonify({"error": "クライアント名は必須です"}), 400

    success, result = add_client(name, first_date, issue, route, child_grade)
    if success:
        return jsonify({"success": True, "client_id": result})
    else:
        return jsonify({"error": result}), 500


# ===========================
# 起動
# ===========================

def open_browser():
    """ブラウザを自動オープン"""
    webbrowser.open(f"http://{APP_HOST}:{APP_PORT}")


if __name__ == "__main__":
    print("個別相談カルテアプリを起動中...")
    print(f"ブラウザで http://{APP_HOST}:{APP_PORT} を開きます")
    # 0.8秒後にブラウザを開く
    timer = threading.Timer(0.8, open_browser)
    timer.start()
    app.run(host=APP_HOST, port=APP_PORT, debug=False)
