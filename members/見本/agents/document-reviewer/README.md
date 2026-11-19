---
name: document-reviewer
description: 文書を読み、決まったことと確認が必要な点を短く返す。
---

# 文書点検役

文書の内容を短時間で確認したい時に使います。頼む時は対象ファイルと用途を添えます。

- [Claude Code の定義](claude-code/document-reviewer.md)は読み取り系の道具を使います。`.claude/agents/` にコピーします。
- [Codex の定義](codex/document-reviewer.toml)は指示で読み取りに限ります。実際の権限は親のセッションから引き継ぎます。`.codex/agents/` にコピーします。

[Claude Code のエージェント](https://code.claude.com/docs/en/sub-agents) / [Codex のエージェント](https://learn.chatgpt.com/docs/agent-configuration/subagents)
