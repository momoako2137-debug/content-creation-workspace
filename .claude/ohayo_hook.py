"""
おはようフック（UserPromptSubmit 用）
「おはよう」を含むメッセージが送信されたとき、引き継ぎとリマインダーを読み込み
今日のタスクをまとめるよう Claude に指示する。
"""
import sys
import json
import os
from datetime import date

# stdin / stdout を UTF-8 に統一する（Windows の cp932 問題を回避）
stdin = open(sys.stdin.fileno(), encoding="utf-8", closefd=False)
stdout_buf = sys.stdout.buffer

def utf8_print(text: str):
    """UTF-8 で stdout に直接書き出す。"""
    stdout_buf.write((text + "\n").encode("utf-8"))
    stdout_buf.flush()

# 対象ファイルのパス
HIKITSUGI = r"C:\Users\Owner\Documents\claude_workspace\momokiako\hikitsugi.txt"
TEIKI     = r"C:\Users\Owner\Documents\Obsidian\04_Claude_Work\定期リマインダールール.md"
IKKAI     = r"C:\Users\Owner\Documents\Obsidian\04_Claude_Work\一回限りのリマインダー.md"
INTERVIEW = r"C:\Users\Owner\Documents\Obsidian\04_Claude_Work\インタビュー予定管理.md"
MAILMAG   = r"C:\Users\Owner\Documents\Obsidian\04_Claude_Work\メルマガ管理.md"


def read_file(path: str) -> str:
    """ファイルを読み込む。存在しない場合は空文字を返す。"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def main():
    try:
        data = json.load(stdin)
    except Exception:
        sys.exit(0)

    # ユーザーのメッセージを取得
    message = data.get("message", "")

    # 「おはよう」を含まない場合は何もしない
    if "おはよう" not in message:
        sys.exit(0)

    # 今日の日付
    today = date.today().strftime("%Y年%m月%d日")

    # 各ファイルを読み込む
    hikitsugi = read_file(HIKITSUGI)
    teiki     = read_file(TEIKI)
    ikkai     = read_file(IKKAI)
    interview = read_file(INTERVIEW)
    mailmag   = read_file(MAILMAG)

    # Claude への指示を組み立てる
    context = (
        f"【おはようフック：自動実行】\n"
        f"今日は {today} です。\n"
        f"以下のファイルを読み込みました。内容をもとに今日のタスクを整理してモモさんに伝えてください。\n\n"
        f"手順：\n"
        f"1. 引き継ぎメモを確認し、前回の続きと未完了タスクを把握する\n"
        f"2. 一回限りのリマインダーから今日・明日が期限のものを抽出する\n"
        f"3. 定期リマインダールールに従い、該当する定期チェック項目を確認する\n"
        f"4. インタビュー予定を確認し、2週間前・3日前・当日に該当するものを伝える\n"
        f"5. メルマガ管理を確認し、残り2週間以内なら伝える\n"
        f"6. 上記をまとめて「今日のタスク」として日本語で簡潔に伝える\n\n"
        f"---\n【引き継ぎメモ】\n{hikitsugi}\n\n"
        f"---\n【一回限りのリマインダー】\n{ikkai}\n\n"
        f"---\n【定期リマインダールール】\n{teiki}\n\n"
        f"---\n【インタビュー予定管理】\n{interview}\n\n"
        f"---\n【メルマガ管理】\n{mailmag}\n"
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
