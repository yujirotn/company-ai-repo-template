# 取り込み元

- 元: https://github.com/AnIT012/nihongo （MIT License。著作権表示は同じフォルダの `LICENSE`）
- 版: v2.1.2・commit `82c60760cd1c77f4c106b03dec6c22e86f70aa56`
- 取り込んだもの: `nihongo/` フォルダと LICENSE だけ（tests・evaluations・assets は入れていない）
- 更新する時は、元の差分を読んでから入れ直す（自動では追いかけない）

## 元から変えた所
1. SKILL.md の description: 人に出す文章を書く・直す時だけ動くように絞った（元は会話の返事まで含んでいて、毎回長い本文が読まれるため）
2. SKILL.md のスクリプトの手順: 原文・直した文は作業用の一時フォルダに置き、書庫には入れない、と書き足した
3. ALWAYS.md（短い版）は、常に読み込む設定にはしていない。毎回効かせたい会社は、`CLAUDE.md` / `AGENTS.md` から読むように書き足す
