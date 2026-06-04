"""
機密ファイル保護フック
PreToolUse イベントで呼び出され、機密ファイルへの操作をブロックする。
"""
import sys
import io
import json
import re

# Windows で UTF-8 出力を強制する
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 保護対象のファイル名パターン
SENSITIVE_PATTERNS = [
    r"(^|[\\/])\.env(\.|$)",   # .env, .env.local など
    r"credentials\.json$",
    r"token\.json$",
    r"wp_config\.py$",
    r"notion_config\.py$",
    r"\.pem$",
    r"\.key$",
]

def is_sensitive(path: str) -> bool:
    return any(re.search(p, path, re.IGNORECASE) for p in SENSITIVE_PATTERNS)

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    target = ""

    if tool in ("Edit", "Write", "Read"):
        target = tool_input.get("file_path", "")
    elif tool == "Bash":
        cmd = tool_input.get("command", "")
        # コマンド内に機密ファイルが含まれているか確認
        target_match = re.search(
            r"([\w./\\-]*(?:\.env[\w.]*|credentials\.json|token\.json|wp_config\.py|notion_config\.py|[\w-]+\.pem|[\w-]+\.key))",
            cmd,
            re.IGNORECASE,
        )
        if target_match:
            target = target_match.group(1)
        else:
            sys.exit(0)

    if target and is_sensitive(target):
        result = {
            "continue": False,
            "stopReason": (
                f"🚨 機密ファイルへの操作をブロックしました。\n"
                f"対象ファイル: {target}\n"
                f"このファイルは保護されています。操作が必要な場合は、モモさんが直接確認・許可してください。"
            ),
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
