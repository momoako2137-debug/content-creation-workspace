"""
終了・保存フック（UserPromptSubmit 用）
「終わり」「保存して」などのキーワードを検知し、
hikitsugi.txt と Obsidian の両方に保存するよう Claude に指示する。
"""
import sys
import json
from datetime import date

# stdin / stdout を UTF-8 に統一する（Windows の cp932 問題を回避）
stdin = open(sys.stdin.fileno(), encoding="utf-8", closefd=False)
stdout_buf = sys.stdout.buffer

def utf8_print(text: str):
    """UTF-8 で stdout に直接書き出す。"""
    stdout_buf.write((text + "\n").encode("utf-8"))
    stdout_buf.flush()

# 終了・保存を意味するキーワード
SAVE_KEYWORDS = [
    "終わり", "終わります", "終わる", "終わろう",
    "保存して", "保存お願い", "保存よろしく",
    "おやすみ", "また明日", "今日は以上",
    "今日終わり", "作業終わり", "作業終了",
]

# 保存先パス
HIKITSUGI     = r"C:\Users\Owner\Documents\claude_workspace\momokiako\hikitsugi.txt"
OBSIDIAN_DIR  = r"C:\Users\Owner\Documents\Obsidian\04_Claude_Work\作業記録"


def main():
    try:
        data = json.load(stdin)
    except Exception:
        sys.exit(0)

    message = data.get("message", "")

    # キーワードを含まない場合は何もしない
    if not any(kw in message for kw in SAVE_KEYWORDS):
        sys.exit(0)

    today     = date.today().strftime("%Y-%m-%d")
    today_jp  = date.today().strftime("%Y年%m月%d日")
    obsidian_path = rf"{OBSIDIAN_DIR}\{today}_作業記録.md"

    context = (
        f"【保存フック：自動実行】\n"
        f"モモさんが今日の作業を終了しようとしています（{today_jp}）。\n"
        f"今日の会話内容をもとに、以下の2か所に保存してください。\n\n"
        f"## 保存手順\n\n"
        f"### ① hikitsugi.txt を更新する\n"
        f"保存先: {HIKITSUGI}\n"
        f"内容: 以下のフォーマットで、今日の作業内容・次のTODOを先頭に追記する（既存の内容は消さない）\n\n"
        f"```\n"
        f"# ひきつぎメモ（{today} 更新）\n\n"
        f"---\n\n"
        f"## {today} 作業まとめ\n\n"
        f"### やったこと\n"
        f"- （今日の会話で行った作業を箇条書きで記載）\n\n"
        f"### 次にやること\n"
        f"- （未完了・次回に持ち越すタスクを記載）\n\n"
        f"---\n"
        f"```\n\n"
        f"### ② Obsidian に作業記録を保存する\n"
        f"保存先: {obsidian_path}\n"
        f"内容: hikitsugi.txt と同じ内容を Markdown 形式で保存する。\n"
        f"ファイルが既に存在する場合は上書きしてよい。\n\n"
        f"## 注意\n"
        f"- 保存が完了したらモモさんに「保存しました！」と日本語で伝える。\n"
        f"- 保存先フォルダが存在しない場合は作成する。\n"
        f"- 今日の会話で具体的な作業内容がない場合は「特になし」と記載してよい。\n"
    )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    utf8_print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
