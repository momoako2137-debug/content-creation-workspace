"""
自動テストランナー（Stop フック用）
作業終了時に自動実行される。失敗時は exit(2) で Claude を起こし、自動修正を試みさせる。
"""
import sys
import io
import json
import subprocess
import os

# Windows で UTF-8 出力を強制する
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.join(os.path.dirname(__file__), "..", "momokiako")
HOOK = os.path.join(os.path.dirname(__file__), "protect_hook.py")

# 構文チェック対象スクリプト
CHECK_SCRIPTS = [
    "create_slides.py",
    "wp_post.py",
    "notion_add_content.py",
    "pdf_to_pptx.py",
    "wp_week0.py",
    "wp_landing.py",
]

errors = []

# ① 各スクリプトの構文チェック
for name in CHECK_SCRIPTS:
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        continue
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        errors.append(f"構文エラー [{name}]: {result.stderr.strip()}")

# ② 機密ファイル保護フックの動作確認（ブロックされるべきケース）
if os.path.exists(HOOK):
    test_input = '{"tool_name":"Edit","tool_input":{"file_path":"credentials.json"}}'
    result = subprocess.run(
        [sys.executable, HOOK],
        input=test_input,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 2:
        errors.append(
            f"protect_hook が機密ファイルをブロックしませんでした（終了コード: {result.returncode}）"
        )

    # 通常ファイルはスルーされるべきケース
    test_input_ok = '{"tool_name":"Edit","tool_input":{"file_path":"wp_post.py"}}'
    result_ok = subprocess.run(
        [sys.executable, HOOK],
        input=test_input_ok,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result_ok.returncode != 0:
        errors.append(
            f"protect_hook が通常ファイルを誤ってブロックしました（終了コード: {result_ok.returncode}）"
        )

# 結果を出力
if errors:
    error_list = "\n".join(f"- {e}" for e in errors)
    output = {
        "systemMessage": (
            "【自動テスト失敗】原因を分析して修正を試みます。\n" + error_list
        ),
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": (
                "自動テストが失敗しました。以下のエラーを分析し、自分で修正してください。"
                "修正できない場合のみモモさんに日本語で報告してください。\n\n"
                + error_list
            ),
        },
    }
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(2)

# 全テスト通過 → 静かに終了
sys.exit(0)
