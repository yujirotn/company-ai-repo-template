"""Block a narrow set of inline, key-like assignments in file editing tools."""

import json
import re
import sys


INLINE_KEY = re.compile(
    r"""\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)["']?\s*[:=]\s*(["'])[A-Za-z0-9_./+=-]{16,}\1""",
    re.IGNORECASE,
)


def edited_text(payload):
    tool_name = payload["tool_name"]
    tool_input = payload["tool_input"]
    if tool_name == "Write":
        return tool_input["content"]
    if tool_name == "Edit":
        return tool_input["new_string"]
    if tool_name == "apply_patch":
        return "\n".join(line[1:] for line in tool_input["command"].splitlines() if line.startswith("+"))
    return ""


def main():
    try:
        text = edited_text(json.load(sys.stdin))
        if not isinstance(text, str):
            raise TypeError("expected text")
    except (KeyError, TypeError, AttributeError, ValueError):
        print("フックが編集内容を読み取れませんでした。設定を確認してください。", file=sys.stderr)
        return 2

    if INLINE_KEY.search(text):
        print("鍵らしい値が含まれるため編集を止めました。環境変数などから参照してください。", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
