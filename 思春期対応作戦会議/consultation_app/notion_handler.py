#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Notion REST API処理

import requests
import json
from config import NOTION_API_KEY, NOTION_CLIENT_DB_ID, NOTION_COMM_DB_ID, NOTION_VERSION


def _headers():
    """Notion APIヘッダーを返す"""
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def get_clients():
    """クライアント一覧DBから全クライアントを取得"""
    url = f"https://api.notion.com/v1/databases/{NOTION_CLIENT_DB_ID}/query"
    payload = {
        "sorts": [{"property": "初回相談日", "direction": "descending"}]
    }
    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code != 200:
        return []

    results = response.json().get("results", [])
    clients = []
    for page in results:
        props = page.get("properties", {})
        client = {
            "id": page["id"],
            "url": page.get("url", ""),
            "client_number": _get_formula_or_text(props.get("顧客番号", {})),
            "name": _get_title(props.get("クライアント名（仮名・イニシャル）", {})),
            "first_date": _get_date(props.get("初回相談日", {})),
            "next_date": _get_date(props.get("次回フォローアップ日", {})),
            "issue": _get_text(props.get("主訴・相談内容", {})),
            "child_grade": _get_text(props.get("子どもの学年", {})),
            "route": _get_select(props.get("経路", {})),
        }
        clients.append(client)
    return clients


def get_client(client_id):
    """指定クライアントの詳細情報を取得"""
    url = f"https://api.notion.com/v1/pages/{client_id}"
    response = requests.get(url, headers=_headers())
    if response.status_code != 200:
        return None

    page = response.json()
    props = page.get("properties", {})
    return {
        "id": page["id"],
        "url": page.get("url", ""),
        "client_number": _get_formula_or_text(props.get("顧客番号", {})),
        "name": _get_title(props.get("クライアント名（仮名・イニシャル）", {})),
        "first_date": _get_date(props.get("初回相談日", {})),
        "next_date": _get_date(props.get("次回フォローアップ日", {})),
        "issue": _get_text(props.get("主訴・相談内容", {})),
        "child_grade": _get_text(props.get("子どもの学年", {})),
        "child_count": _get_number(props.get("子どもの人数", {})),
        "route": _get_select(props.get("経路", {})),
        "gender": _get_select(props.get("性別", {})),
        "lifestage": _get_select(props.get("ライフステージ", {})),
        "heart_weather": _get_select(props.get("こころの天気", {})),
        "reason": _get_text(props.get("参加理由・知りたい内容", {})),
        "memo": _get_text(props.get("メモ", {})),
    }


def _extract_section_detail(analysis_text, section_name):
    """分析テキストから指定セクションの詳細版（なければ概要版）を抽出する"""
    if not analysis_text:
        return ""
    import re
    # セクション名を含む行から次の **セクション** までを取得
    section_match = re.search(
        r'\*{0,2}' + re.escape(section_name) + r'[^\n]*\*{0,2}\n([\s\S]*?)(?=\n\*{2}[^\n]|\Z)',
        analysis_text
    )
    if not section_match:
        return ""
    section = section_match.group(1)
    # 詳細版を優先
    detail = re.search(r'■\s*詳細版\s*\n→\s*([\s\S]*?)(?=\n■|\Z)', section)
    if detail:
        return detail.group(1).strip()[:400]
    # 概要版
    summary = re.search(r'■\s*概要版\s*\n→\s*([\s\S]*?)(?=\n■|\Z)', section)
    if summary:
        return summary.group(1).strip()[:400]
    return section.strip()[:400]


def _ensure_next_action_property(session_db_id):
    """セッションDBに次回に向けてプロパティがなければ追加する"""
    url = f"https://api.notion.com/v1/databases/{session_db_id}"
    response = requests.get(url, headers=_headers())
    if response.status_code != 200:
        return
    props = response.json().get("properties", {})
    to_add = {}
    if "概要" not in props:
        to_add["概要"] = {"rich_text": {}}
    if "次回に向けて" not in props:
        to_add["次回に向けて"] = {"rich_text": {}}
    if "やってみようと思ったこと" not in props:
        to_add["やってみようと思ったこと"] = {"rich_text": {}}
    if to_add:
        requests.patch(url, headers=_headers(), json={"properties": to_add})


def get_sessions(client_page_id):
    """指定クライアントページ内のセッション記録DBを探して一覧を取得"""
    # クライアントページ内のブロックを検索してDBを見つける
    url = f"https://api.notion.com/v1/blocks/{client_page_id}/children"
    response = requests.get(url, headers=_headers())
    if response.status_code != 200:
        return []

    blocks = response.json().get("results", [])
    session_db_id = None

    # セッション記録データベースを探す
    for block in blocks:
        if block.get("type") == "child_database":
            title = block.get("child_database", {}).get("title", "")
            if "セッション" in title:
                session_db_id = block["id"]
                break

    if not session_db_id:
        return [], None

    # 必要なプロパティがなければ自動追加
    _ensure_next_action_property(session_db_id)

    # セッション記録DBのページ一覧を取得
    url = f"https://api.notion.com/v1/databases/{session_db_id}/query"
    payload = {
        "sorts": [{"property": "セッション日", "direction": "descending"}]
    }
    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code != 200:
        return [], None

    results = response.json().get("results", [])
    sessions = []
    for page in results:
        props = page.get("properties", {})
        session = {
            "id": page["id"],
            "url": page.get("url", ""),
            "name": _get_title(props.get("セッション名", {})),
            "date": _get_date(props.get("セッション日", {})),
            "count": _get_number(props.get("回数", {})),
            "next_date": _get_date(props.get("次回フォローアップ予定日", {})),
            "status": _get_select(props.get("ステータス", {})),
            "summary": _get_text(props.get("概要", {})),
            "next_action": _get_text(props.get("次回に向けて", {})),
            "try_next": _get_text(props.get("やってみようと思ったこと", {})),
        }
        sessions.append(session)
    return sessions, session_db_id


def get_communications(client_page_id):
    """指定クライアントのコミュニケーション記録を取得（全件取得→Python側で照合）"""
    target_id = client_page_id.replace("-", "")

    url = f"https://api.notion.com/v1/databases/{NOTION_COMM_DB_ID}/query"
    payload = {
        "sorts": [{"property": "日付", "direction": "descending"}],
        "page_size": 100
    }
    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code != 200:
        print(f"[コミュニケーション取得エラー] status={response.status_code} body={response.text[:300]}")
        return []

    results = response.json().get("results", [])
    comms = []
    for page in results:
        props = page.get("properties", {})
        # リレーションプロパティ名を動的に探す（日本語名が異なる場合に対応）
        relation_prop = None
        for key, val in props.items():
            if val.get("type") == "relation":
                relation_prop = val
                break
        if relation_prop is None:
            continue
        relation_items = relation_prop.get("relation", [])
        related_ids = [r.get("id", "").replace("-", "") for r in relation_items]
        if target_id not in related_ids:
            continue
        comms.append({
            "id": page["id"],
            "url": page.get("url", ""),
            "title": _get_title(props.get("タイトル", {})),
            "date": _get_date(props.get("日付", {})),
            "route": _get_select(props.get("経路", {})),
            "direction": _get_select(props.get("方向", {})),
            "content": _get_text(props.get("内容", {})),
            "status": _get_select(props.get("対応状況", {})),
            "memo": _get_text(props.get("メモ", {})),
        })
    return comms


def debug_communications_raw(client_page_id):
    """デバッグ用：コミュニケーションDBの生データを返す"""
    url = f"https://api.notion.com/v1/databases/{NOTION_COMM_DB_ID}/query"
    payload = {"page_size": 10}
    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code != 200:
        return {"error": response.status_code, "body": response.text}
    data = response.json()
    # 最初の1件のプロパティ構造だけ返す
    results = data.get("results", [])
    if not results:
        return {"message": "DBにレコードが0件です", "total": 0}
    first = results[0]
    props_summary = {k: v.get("type") for k, v in first.get("properties", {}).items()}
    # リレーション値も確認
    for k, v in first.get("properties", {}).items():
        if v.get("type") == "relation":
            props_summary[f"{k}(relation_ids)"] = [r.get("id") for r in v.get("relation", [])]
    # 実際の値も確認
    first_props = first.get("properties", {})
    content_val = "".join(t.get("plain_text", "") for t in first_props.get("内容", {}).get("rich_text", []))
    memo_val = "".join(t.get("plain_text", "") for t in first_props.get("メモ", {}).get("rich_text", []))
    return {
        "total_records": len(results),
        "client_page_id": client_page_id,
        "client_id_normalized": client_page_id.replace("-", ""),
        "first_record_props": props_summary,
        "内容_value": content_val,
        "メモ_value": memo_val,
    }


def save_communication(client_page_id, title, date, route, direction, status, content, memo=""):
    """コミュニケーション記録をNotionに保存"""
    # くみさんのページURLを組み立て（ダッシュなし形式で渡す）
    normalized = client_page_id.replace("-", "")
    client_url = f"https://app.notion.com/p/{normalized}"

    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_COMM_DB_ID},
        "properties": {
            "タイトル": {"title": [{"text": {"content": title}}]},
            "日付": {"date": {"start": date}},
            "経路": {"select": {"name": route}},
            "方向": {"select": {"name": direction}},
            "対応状況": {"select": {"name": status}},
            "内容": {"rich_text": [{"text": {"content": content}}]},
            "メモ": {"rich_text": [{"text": {"content": memo}}]},
            "クライアント": {"relation": [{"id": client_page_id}]},
        }
    }
    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code == 200:
        return True, response.json().get("url", "")
    else:
        print(f"[コミュニケーション保存エラー] {response.status_code}: {response.text[:300]}")
        return False, response.text


def save_session(session_db_id, session_count, session_date, analysis, messages):
    """セッション記録をNotionに保存"""
    # DBの現在のプロパティ一覧を取得
    db_resp = requests.get(
        f"https://api.notion.com/v1/databases/{session_db_id}",
        headers=_headers()
    )
    existing_props = set(db_resp.json().get("properties", {}).keys()) if db_resp.status_code == 200 else set()

    session_name = f"第{session_count}回 {session_date}"

    # ブロックを構築
    blocks = []
    blocks.append(_heading2("セッション分析"))
    chunk_size = 600
    max_blocks = 90
    for i in range(0, len(analysis), chunk_size):
        if len(blocks) >= max_blocks:
            blocks.append(_paragraph("（文字数が多いため残りは省略されました）"))
            break
        blocks.append(_paragraph(analysis[i:i+chunk_size]))

    if messages:
        blocks.append({"object": "block", "type": "divider", "divider": {}})
        blocks.append(_heading2("セッション間メッセージ記録"))
        for i in range(0, len(messages), chunk_size):
            if len(blocks) >= max_blocks:
                break
            blocks.append(_paragraph(messages[i:i+chunk_size]))

    # 各セクションをテキストから抽出
    summary = analysis[:100].replace("\n", " ").strip() if analysis else ""
    next_action = _extract_section_detail(analysis, "次回に向けてどうするか")
    try_next = _extract_section_detail(analysis, "やってみようと思ったこと")

    # 基本プロパティ（必ず存在する）
    props = {
        "セッション名": {"title": [{"text": {"content": session_name}}]},
        "セッション日": {"date": {"start": session_date}},
        "回数": {"number": session_count},
        "ステータス": {"select": {"name": "記録済み"}},
    }
    # DBに存在する場合のみ追加プロパティを書き込む
    if "概要" in existing_props:
        props["概要"] = {"rich_text": [{"text": {"content": summary}}]}
    if "次回に向けて" in existing_props:
        props["次回に向けて"] = {"rich_text": [{"text": {"content": next_action}}]}
    if "やってみようと思ったこと" in existing_props:
        props["やってみようと思ったこと"] = {"rich_text": [{"text": {"content": try_next}}]}

    # セッションページを作成
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": session_db_id},
        "properties": props,
        "children": blocks
    }

    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code == 200:
        return True, response.json().get("url", "")
    else:
        print(f"[保存エラー] ステータス: {response.status_code}")
        print(f"[保存エラー] 内容: {response.text}")
        return False, response.text


def add_client(name, first_date, issue, route, child_grade):
    """新規クライアントをNotionに追加"""
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_CLIENT_DB_ID},
        "properties": {
            "クライアント名（仮名・イニシャル）": {
                "title": [{"text": {"content": name}}]
            },
            "初回相談日": {
                "date": {"start": first_date}
            },
            "主訴・相談内容": {
                "rich_text": [{"text": {"content": issue}}]
            },
            "経路": {
                "select": {"name": route}
            },
            "子どもの学年": {
                "rich_text": [{"text": {"content": child_grade}}]
            }
        },
        "children": [
            _heading2("事前アンケート"),
            _paragraph("※ アンケート回答をここに記録"),
            _heading2("セッション記録"),
            _paragraph("※ セッションごとの記録はサブデータベースで管理します"),
        ]
    }

    response = requests.post(url, headers=_headers(), json=payload)
    if response.status_code == 200:
        page_id = response.json()["id"]
        # セッション記録用サブDBを作成
        _create_session_db(page_id)
        return True, page_id
    else:
        return False, response.text


def _create_session_db(parent_page_id):
    """クライアントページ内にセッション記録DBを作成"""
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "セッション記録"}}],
        "properties": {
            "セッション名": {"title": {}},
            "セッション日": {"date": {}},
            "回数": {"number": {"format": "number"}},
            "次回フォローアップ予定日": {"date": {}},
            "ステータス": {
                "select": {
                    "options": [
                        {"name": "記録済み", "color": "green"},
                        {"name": "記録中", "color": "yellow"},
                        {"name": "未記録", "color": "gray"},
                    ]
                }
            },
            "概要": {"rich_text": {}},
            "次回に向けて": {"rich_text": {}},
            "やってみようと思ったこと": {"rich_text": {}}
        }
    }
    requests.post(url, headers=_headers(), json=payload)


def _build_session_blocks(section_2a, section_2b, messages):
    """セッション記録ページのブロック構造を生成"""
    blocks = []

    # セクション2-A
    blocks.append(_heading2("セクション2-A：クライアント記録"))

    items_2a = [
        ("課題", section_2a.get("課題", {})),
        ("やってみようと思ったこと", section_2a.get("やってみようと思ったこと", {})),
        ("その他", section_2a.get("その他", {})),
    ]
    for label, item in items_2a:
        blocks.append(_heading3(label))
        blocks.append(_paragraph(f"■ 概要版\n→ {item.get('summary', '')}"))
        blocks.append(_paragraph(f"■ 詳細版\n→ {item.get('detail', '')}"))

    next_date = section_2a.get("次回フォローアップ予定日", "")
    blocks.append(_heading3("次回フォローアップ予定日"))
    blocks.append(_paragraph(next_date))

    # 区切り
    blocks.append({"object": "block", "type": "divider", "divider": {}})

    # セクション2-B
    blocks.append(_heading2("セクション2-B：セッション分析"))

    items_2b = [
        ("そのセッションで理解できたこと", section_2b.get("理解できたこと", {})),
        ("疑問に思ったこと", section_2b.get("疑問", {})),
        ("自分の対応と迷い", section_2b.get("対応と迷い", {})),
        ("クライアントの反応", section_2b.get("クライアントの反応", {})),
        ("次回に向けてどうするか", section_2b.get("次回に向けて", {})),
        ("次回までに調べること", section_2b.get("調べること", {})),
        ("その他の気づき", section_2b.get("その他", {})),
    ]
    for label, item in items_2b:
        blocks.append(_heading3(label))
        blocks.append(_paragraph(f"■ 概要版\n→ {item.get('summary', '')}"))
        blocks.append(_paragraph(f"■ 詳細版\n→ {item.get('detail', '')}"))

    # 区切り
    blocks.append({"object": "block", "type": "divider", "divider": {}})

    # セクション3
    blocks.append(_heading2("セクション3：セッション間メッセージ記録"))
    if messages:
        for msg in messages:
            date = msg.get("date", "")
            content = msg.get("content", "")
            if date or content:
                blocks.append(_paragraph(f"【{date}】\n{content}"))
    else:
        blocks.append(_paragraph("※ セッション間のメッセージをここに記録"))

    return blocks


# --- ブロック生成ヘルパー ---

def _heading2(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }


def _heading3(text):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}
    }


def _paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:2000]}}]}
    }


# --- プロパティ取得ヘルパー ---

def _get_title(prop):
    items = prop.get("title", [])
    return "".join(t.get("plain_text", "") for t in items)


def _get_text(prop):
    items = prop.get("rich_text", [])
    return "".join(t.get("plain_text", "") for t in items)


def _get_date(prop):
    date = prop.get("date", {})
    return date.get("start", "") if date else ""


def _get_select(prop):
    sel = prop.get("select", {})
    return sel.get("name", "") if sel else ""


def _get_number(prop):
    return prop.get("number", 0) or 0


def _get_formula_or_text(prop):
    """unique_id・フォーミュラ・テキスト・数値いずれの型でも顧客番号を取得"""
    if not prop:
        return ""
    prop_type = prop.get("type", "")
    if prop_type == "unique_id":
        uid = prop.get("unique_id", {})
        prefix = uid.get("prefix") or ""
        number = uid.get("number")
        if number is None:
            return ""
        return f"{prefix}-{number}" if prefix else str(number)
    if prop_type == "formula":
        formula = prop.get("formula", {})
        return str(formula.get("string") or formula.get("number") or "")
    if prop_type == "rich_text":
        return _get_text(prop)
    if prop_type == "number":
        val = prop.get("number")
        return f"CL-{val}" if val is not None else ""
    return ""
