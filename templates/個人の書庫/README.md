# 個人の書庫のひな形

会社の書庫の AI が「この人の個人の書庫がまだ無い」と気づいた時に、本人の同意を取ってから、
このフォルダの中身を元に**本人専用の非公開の書庫**を作ります（手順は会社の書庫の `CLAUDE.md` / `AGENTS.md`
の「置き場所の3段」を参照）。人が手で作る場合も同じ中身をコピーすれば足ります。

## 中身

```
<自分の呼び名>-ai/                … 本人専用の書庫（GitHub 上は非公開）
├── CLAUDE.md / AGENTS.md         … この書庫で AI が守ること（中身は同じ）
├── README.md                     … このファイル（作った後は自分用の説明に書き換える）
├── .claude-plugin/marketplace.json … 自分の道具の目録
├── plugins/me/                   … 自分だけのスキルの箱（skills/<名前>/SKILL.md）
└── memo/                         … 自分だけのメモ
```

## 作った後にやること

1. `【自分の呼び名】` を、自分の呼び名に書き換える（`CLAUDE.md` `AGENTS.md` `marketplace.json` `plugin.json`）
2. 自分のスキルを使えるようにする（1回だけ）:
   ```bash
   claude plugin marketplace add ./<自分の呼び名>-ai
   claude plugin install me@my-ai
   ```
   Codex なら `codex plugin marketplace add ./<自分の呼び名>-ai` → `codex plugin add me@my-ai`
3. スキルを足したり直したりした時:
   - Claude Code は手元のフォルダを直接読むので、次に Claude Code を起動した時から効く
   - Codex は写しを取って使うので、`codex plugin add me@my-ai` をもう一度実行して取り込み直す
