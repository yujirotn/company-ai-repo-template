#!/usr/bin/env bash
# 書庫を開いた時に、GitHub から最新を取ってくる小さな仕組み。
#
# - Claude Code は .claude/settings.json の SessionStart フックから、
#   Codex は .codex/hooks.json の SessionStart フックから、これを動かす。
# - 人が手で動かしてもよい:  bash scripts/pull-latest.sh --text
#
# 危ない操作（reset・強制・stash・履歴の書き換え）は一切しない。
# 「早送りで取り込める時だけ取り込む（git merge --ff-only）」以外は、何も変えずに一言だけ出す。
# 失敗しても、AI の起動は止めない（いつも 0 で終わる）。

set -u

MODE="json"
if [ "${1:-}" = "--text" ]; then
  MODE="text"
fi

# 結果を出す。人に見せる一言（systemMessage）と、AI に渡す一言（additionalContext）を同じ文にする。
say() {
  msg="【書庫の同期】$1"
  if [ "$MODE" = "text" ]; then
    printf '%s\n' "$msg"
  else
    # JSON の文字列として壊れないよう、\ と " と改行を逃がす
    esc=$(printf '%s' "$msg" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' | awk 'BEGIN{ORS="\\n"} {print}' | sed -e 's/\\n$//')
    printf '{"systemMessage":"%s","hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$esc" "$esc"
  fi
  exit 0
}

# 書庫の一番上へ移る（フックから呼ばれた時は CLAUDE_PROJECT_DIR が入っている）
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# パスワードを聞く画面で止まらないようにする（聞かれたら失敗として扱う）
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes -o ConnectTimeout=10}"

GIT_DIR_PATH=$(git rev-parse --git-dir)
if [ -e "$GIT_DIR_PATH/MERGE_HEAD" ] || [ -d "$GIT_DIR_PATH/rebase-merge" ] || [ -d "$GIT_DIR_PATH/rebase-apply" ]; then
  say "取り込みの途中（merge・rebase の途中）のため、最新の取り込みは見送りました。AI に「書庫の取り込みが途中で止まっている。直し方を教えて」と相談してください。"
fi

BRANCH=$(git symbolic-ref --quiet --short HEAD 2>/dev/null) || \
  say "今は特定の枝（ブランチ）の上にいないため、最新の取り込みは見送りました。AI に「main に戻りたい」と頼んでください。"

UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null) || \
  say "枝「${BRANCH}」はまだ GitHub とつながっていないため、取り込みは省きました（自分で作った作業用の枝なら、このままで問題ありません）。"

# 手元に保存していない変更（追跡中のファイルの変更）があれば、何も触らない
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
  say "手元に保存（コミット）していない変更があるため、最新の取り込みは見送りました。変更を保存してから開き直すか、AI に「書庫に保存して」と頼んでください。"
fi

if ! git fetch --quiet 2>/dev/null; then
  say "GitHub につながらず、最新かどうかを確かめられませんでした。インターネットにつながっているか、ターミナルで gh auth status を実行して GitHub にログインできているかを確かめてください。手元の内容のまま作業はできます。"
fi

BEHIND=$(git rev-list --count "HEAD..@{u}" 2>/dev/null || echo 0)
AHEAD=$(git rev-list --count "@{u}..HEAD" 2>/dev/null || echo 0)

if [ "$BEHIND" -eq 0 ] && [ "$AHEAD" -eq 0 ]; then
  say "この書庫は最新です（${UPSTREAM} と同じ）。"
fi

if [ "$BEHIND" -eq 0 ]; then
  say "この書庫は最新です。手元に、まだ GitHub へ送っていない保存が ${AHEAD} 件あります（送るときは AI に「書庫に保存して」と頼んでください）。"
fi

if [ "$AHEAD" -gt 0 ]; then
  say "手元と GitHub の記録が分かれているため（手元だけに ${AHEAD} 件・GitHub だけに ${BEHIND} 件）、自動では取り込みませんでした。AI に「書庫の記録が分かれている。安全な直し方を教えて」と相談してください。"
fi

BEFORE=$(git rev-parse HEAD)
if ! git merge --ff-only --quiet "@{u}" >/dev/null 2>&1; then
  say "GitHub の更新が ${BEHIND} 件ありますが、手元のファイルとぶつかるため取り込めませんでした。AI に「書庫の最新を取り込めない。理由を調べて」と相談してください。"
fi

NOTE=""
if ! git diff --quiet "$BEFORE" HEAD -- plugins .claude-plugin 2>/dev/null; then
  NOTE=" 会社の道具（plugins/）も新しくなりました。Claude Code では /reload-plugins を実行すると、今の会話にも反映されます。"
fi
say "最新を取ってきました（GitHub の更新 ${BEHIND} 件を取り込みました）。${NOTE}"
