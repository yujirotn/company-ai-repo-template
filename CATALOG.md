# ハーネス部品一覧

メンバーのおすすめと会社のプラグインを種類別に探せます。更新するには `python3 scripts/catalog.py` を実行します。
フック・設定は、台本や設定の全文を確認してから使う人が自分で設定に足します。

## スキル

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| スキル | minutes-in-three-lines | 見本 | 会議のメモを決定事項・次の作業・未決事項の3行にまとめる。会議後に要点を共有するときに使う。 | [SKILL.md](members/%E8%A6%8B%E6%9C%AC/skills/minutes-in-three-lines/SKILL.md) |
| スキル | dev-attack | 会社（ai-dev-steps） | 開発の手順の段9「攻撃して直す」。自分で作った道具の仕様とコードを別の AI に読ませて守りを点検する。根本原因を説明してから直し、もう一度読んで確かめる。「セキュリティを確かめたい」「穴がないか見て」「公開前の防犯点検」「dev-attack」と言われた時、または dev-start が段9を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-attack/SKILL.md) |
| スキル | dev-build | 会社（ai-dev-steps） | 開発の手順の段6「本番の実装」。完成条件（テストの場面の表・守りの条件）を先に仕上げ、1部屋ずつ作り、作った AI とは別の AI を新しく起こして厳しく点検させ、根本原因を説明してから直す、を合格まで回す。「本番を作って」「実装して」「ちゃんと作りたい」「レビューを通して」「dev-build」と言われた時、または dev-start が段6を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-build/SKILL.md) |
| スキル | dev-concept | 会社（ai-dev-steps） | 開発の手順の段1「コンセプト」。誰の、どんな困りごとを、どう解くかを、AI が聞き役になって1問ずつ引き出し、docs/00-コンセプト.md にまとめる。「何を作るか決めたい」「アイデアを整理したい」「コンセプトを作りたい」「dev-concept」と言われた時、または dev-start が段1を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-concept/SKILL.md) |
| スキル | dev-design | 会社（ai-dev-steps） | 開発の手順の段8「デザイン」。使える DESIGN.md があれば画面に当てる。決まりが無ければ雰囲気の見本（ムードボード）を3方向並べて選び、色・文字・余白などの決まりを仕事の docs/デザイン.md にまとめる。迷ったら使い捨ての HTML で案を並べて比べる。「デザインを決めたい」「見た目を整えたい」「DESIGN.md を作りたい」「ムードボード」「dev-design」と言われた時、または dev-start が段8を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-design/SKILL.md) |
| スキル | dev-pricing | 会社（ai-dev-steps） | 開発の手順の段7「価格」（売るものの時だけ。社内で使う道具なら飛ばしてよい）。費用（サーバー代・AI の利用料など）と利益を試算し、プランの段と配分（2:6:2）を決め、値段の感じ方のアンケート（安すぎる・安い・高い・高すぎるの4問）を集計して、docs/06-価格.md にまとめる。「値段を決めたい」「料金プランを作りたい」「元が取れるか試算したい」「dev-pricing」と言われた時、または dev-start が段7を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-pricing/SKILL.md) |
| スキル | dev-prototype | 会社（ai-dev-steps） | 開発の手順の段4「試作」。図面（docs/01〜03）どおりに、まず手元のパソコンで一通り動くものを、1画面ずつ端から端まで作る。本物の鍵や本番のデータは使わず、架空のデータで動かす。「試作を作って」「まず動くものを」「プロトタイプ」「モックを動かしたい」「dev-prototype」と言われた時、または dev-start が段4を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-prototype/SKILL.md) |
| スキル | dev-spec | 会社（ai-dev-steps） | 開発の手順の段2「仕様」。コンセプトをもとに、戦略・要件（何を作るか・作らないか）・構造（データの出どころと置き場所）の3層で、docs/01-要件.md と docs/03-データ.md を1問ずつ埋める。「仕様を決めたい」「要件をまとめたい」「データの置き場所を決めたい」「dev-spec」と言われた時、または dev-start が段2を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-spec/SKILL.md) |
| スキル | dev-start | 会社（ai-dev-steps） | AI と一緒に道具やサービスを作る「開発の手順 1〜9」の入口。docs/ の中を見て、今どの段まで進んでいるか・次にどのスキルを使うかを案内する。「開発を始めたい」「新しい道具を作りたい」「次は何をすればいい？」「今どこまで進んだ？」「dev-start」と言われた時、または作りかけの仕事の続きを始める時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-start/SKILL.md) |
| スキル | dev-validate | 会社（ai-dev-steps） | 開発の手順の段5「価値の検証」（売るものの時だけ。社内で使う道具なら飛ばしてよい）。試作を3〜5人に触ってもらい、「毎日使うか」「無くなったら困るか」を5段階で聞き、合格線で「次へ進む・直して聞き直す・コンセプトに戻る」を決めて docs/05-検証.md に残す。「価値を確かめたい」「お客様に試してもらいたい」「本当に使われるか知りたい」「dev-validate」と言われた時、または dev-start が段5を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-validate/SKILL.md) |
| スキル | dev-wireframe | 会社（ai-dev-steps） | 開発の手順の段3「画面」。要件から論点（最初の画面・一覧の見せ方・主な操作・画面の行き来など）を出し、論点ごとに実際の画面の見本を3案横に並べて選んでもらう「画面えらび」のページを作って渡し、選んだ結果を docs/02-画面.md にまとめる。「画面を考えたい」「ワイヤーを作って」「間取り図を描いて」「画面案を並べて」「dev-wireframe」と言われた時、または dev-start が段3を案内した時に使う。 | [SKILL.md](plugins/ai-dev-steps/skills/dev-wireframe/SKILL.md) |
| スキル | koho-sakusei | 会社（common） | 社内外に出す広報物（お知らせ・方針の1枚資料・チラシの下書き・プレゼンの1枚）を、会社のトンマナ（色・書体・言葉づかいの決まり）どおりに作る。決まりがまだ空なら、先に1問ずつ聞いて埋める。「広報物を作って」「チラシ」「お知らせを作って」「1枚資料」「トンマナ」「koho-sakusei」と言われた時に使う。 | [SKILL.md](plugins/common/skills/koho-sakusei/SKILL.md) |
| スキル | save-to-archive | 会社（common） | 変更をコミット・ブランチ・プルリクエストまで案内し、本体（main）に直接保存しないようにする。「書庫に保存して」「コミットして」「変更を保存したい」「save-to-archive」「プルリクエスト作って」と言われた時、または作業がひと区切りついて変更を残したい時に使う。 | [SKILL.md](plugins/common/skills/save-to-archive/SKILL.md) |
| スキル | design-review | 会社（sho-san） | 画面・Webページ・資料の見た目の仕上がり（余白・文字・色・改行・はみ出し）を、会社の DESIGN.md に照らして、実際の表示を見て点検するスキル。「デザインを見て」「見た目をチェック」「仕上げの確認」「デザインレビュー」と言われた時や、人に出す・公開する前に使う。使いやすさは ux-review、公開前の機械的な点検は web-preflight の担当。 | [SKILL.md](plugins/sho-san/skills/design-review/SKILL.md) |
| スキル | doc-kit | 会社（sho-san） | 会社紹介・戦略共有・仕組みの図解（データの流れ図など）を、会社の色とロゴで「縦（A4・印刷して配る）」と「横（16:9・映して話す）」の2つの形で作る資料キット。「会社紹介を作って」「戦略を共有する資料」「この仕組みを図にして、配る用と映す用で」「縦版と横版で」と言われた時に使う。見た目は DESIGN.md に合わせ、分からない中身は作らずに点線の空欄で残す。 | [SKILL.md](plugins/sho-san/skills/doc-kit/SKILL.md) |
| スキル | explain-visual | 会社（sho-san） | システムの仕組みや考え方を「大きな図＋少ない文字」の1枚のHTMLで説明する。「図解して」「絵で説明して」「仕組みを図にして」と言われた時に使う。初めて聞く技術の質問や、社内の仕組み・お客様への説明の準備の時は、勝手に作らず「図解にしますか？」と1行だけ提案する。 | [SKILL.md](plugins/sho-san/skills/explain-visual/SKILL.md) |
| スキル | grill | 会社（sho-san） | 計画・設計・決めごとを、共通理解に達するまで1問ずつ詰めるスキル（壁打ちの強化版）。各質問にAIの推奨を添える。「詰めて」「グリルして」「grill」「計画を詰めたい」「穴を潰したい」「決めきれていない」「本当にこれでいいか問い詰めて」と言われた時に使う。 | [SKILL.md](plugins/sho-san/skills/grill/SKILL.md) |
| スキル | handoff | 会社（sho-san） | 作業の区切りで、その仕事の README に「最近の動き」と「未解決事項」を書き残し、次に作業する人（別のAIの会話・別のメンバー・明日の自分）が README を読めば続きから始められるようにするスキル。最後に、新しい会話にそのまま貼れる「再開の文」を出す。「引き継ぎ」「ハンドオフ」「記録残して」「今日の分まとめて」「ここで終わる」と言われた時、または大事な決定・新しい論点が出た時に使う。 | [SKILL.md](plugins/sho-san/skills/handoff/SKILL.md) |
| スキル | nihongo | 会社（sho-san） | 人に出す日本語の文章を書く・直す時に使う（Slackやメールの下書き、お客様宛ての文、お知らせ、提案書、スライドの文言、README・技術文書、UI文言、翻訳）。「nihongoで直して」「自然な日本語に」「AIっぽさを消して」と言われた時も使う。普段の会話の返事や短い質問への答えでは使わない。 | [SKILL.md](plugins/sho-san/skills/nihongo/SKILL.md) |
| スキル | org-rebuild | 会社（sho-san） | 自分の AI 作業環境（ハーネス＝AI の周りに置く指示・設定・道具・フォルダの一式。希望すれば、みんなに配りたいものだけ会社の書庫にも入れられる）を、人と1問ずつやりとりしながら点検し、作り直すスキル。①ハーネス点検で採点 → ②グリルで決定木を1問ずつ詰める → ③移行表 → ④コピーと照合 → ⑤別の目の点検（レビュー役＋セキュリティ役）→ ⑥公開・同期 → ⑦決定ログ → ⑧再点検で点数の変化を見せる。研修向けの30分版（点検 → グリル → 決定ログ）もある。「環境を作り直したい」「ハーネスを整理したい」「フォルダ構成を作り直す」「組織づくり」「AI組織を作り直す」「org-rebuild」と言われた時に使う。 | [SKILL.md](plugins/sho-san/skills/org-rebuild/SKILL.md) |
| スキル | proposal-duplication | 会社（sho-san） | 提案書・商談資料を書き始める前に、相手（決裁者）の頭の中に入り込んで「相手が何を、どの順番で感じるか」から提案の構成を設計する壁打ちスキル。①頭の中の地図（悩み・信じていること・恐れ）②感情の順番（安心→共感→納得→期待→決断）③断る理由の先回り（高い・効くのか・今じゃない）を1問ずつ詰め、「感情設計マップ＋提案の構成案」を出す。「〇〇さんへの提案」「提案書を作る」「商談の準備」「刺さる提案にしたい」「なぜ刺さらないのか」「相手の立場で考えたい」と言われた時、または提案書・LP・見積を作り始める時に使う。 | [SKILL.md](plugins/sho-san/skills/proposal-duplication/SKILL.md) |
| スキル | slide-deck-create | 会社（sho-san） | 研修・発表・提案などのスライド資料（16:9 の横にめくるデッキ）を、1枚の自己完結HTMLで作る。「スライド作って」「研修資料」「発表資料」「プレゼン資料」「デッキを作って」と言われた時や、スライドの形が合う資料を頼まれた時に使う。色と雰囲気は毎回 DESIGN.md を読んで合わせ、足りない所は聞いてから作る。 | [SKILL.md](plugins/sho-san/skills/slide-deck-create/SKILL.md) |
| スキル | stack-diagram | 会社（sho-san） | 使っているサービスや技術のつながりを、実物のロゴ・囲み枠・直角の矢印で描く「構成図」を1枚のHTML（必要ならPNG・React部品）で作る。「構成図を描いて」「システムの全体図」「技術スタックを図に」「どのサービスがどうつながっているか絵にして」と言われた時に使う。 | [SKILL.md](plugins/sho-san/skills/stack-diagram/SKILL.md) |
| スキル | ux-review | 会社（sho-san） | 画面（Web画面・管理画面・試作HTML）が「迷わず・覚えずに・間違えずに使えるか」を、実際に操作して点検するスキル。「使いやすさを見て」「分かりにくい」「情報が多すぎる」「UXレビュー」と言われた時や、画面を作る前に設計を決める時に使う。色や余白など見た目の仕上がりは design-review の担当。 | [SKILL.md](plugins/sho-san/skills/ux-review/SKILL.md) |
| スキル | visual-design | 会社（sho-san） | HTML・LP・スライド・提案書など人が見るものの見た目（文字の組み方・並べ方・余白・目に入る順番・色）を作る・直す・点検する時の原則とレビューの型。「デザイン見て」「見た目を整えて」「レイアウト」「余白」と言われた時や、人に渡す成果物を仕上げる時に使う。 | [SKILL.md](plugins/sho-san/skills/visual-design/SKILL.md) |
| スキル | web-preflight | 会社（sho-san） | Webページ（静的なHTMLのサイト・LP）を公開・納品する前に、機械的に点検するスキル。タイトル・説明文・スマホ表示の設定の抜け、ファイルの参照切れ、ダミー文字の残り、画像の代わりの文字（alt）の抜け、空のリンクを見つける。「公開前チェック」「納品前の確認」「リンク切れを見て」と言われた時に使う。 | [SKILL.md](plugins/sho-san/skills/web-preflight/SKILL.md) |

## フック

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| フック | block-inline-key | 見本 | API キーらしい文字列をファイル編集ツールで書き込む前に止める。 | [README.md](members/%E8%A6%8B%E6%9C%AC/hooks/block-inline-key/README.md) |

## 決まり

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| 決まり | no-inline-key | 見本 | 認証情報を環境変数などから読み、コードや記録に直接書かない。 | [README.md](members/%E8%A6%8B%E6%9C%AC/rules/no-inline-key/README.md) |

## エージェント

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| エージェント | document-reviewer | 見本 | 文書を読み、決まったことと確認が必要な点を短く返す。 | [README.md](members/%E8%A6%8B%E6%9C%AC/agents/document-reviewer/README.md) |
| エージェント | attacker | 会社（ai-dev-steps） | 段9で、攻める側の目で仕様とコードを読む防御点検役。 | [attacker.md](plugins/ai-dev-steps/agents/attacker.md) |
| エージェント | build-reviewer | 会社（ai-dev-steps） | 段6で、完成条件と実装の対応を読む点検役。 | [build-reviewer.md](plugins/ai-dev-steps/agents/build-reviewer.md) |
| エージェント | security-reviewer | 会社（ai-dev-steps） | 段6で、認証やデータの扱いなどの守りを読む点検役。 | [security-reviewer.md](plugins/ai-dev-steps/agents/security-reviewer.md) |

## 設定

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| 設定 | limit-access | 見本 | 認証情報ファイルの読み取り、または点検時の書き込みを制限する設定。 | [README.md](members/%E8%A6%8B%E6%9C%AC/settings/limit-access/README.md) |

## プラグイン

| 種類 | 名前 | 持ち主 | 一言 | 場所 |
| --- | --- | --- | --- | --- |
| プラグイン | document-toolbox | 見本 | 読んだ文書から次にやることを短く整理するスキルをひとまとめにする。 | [plugin.json](members/%E8%A6%8B%E6%9C%AC/plugins/document-toolbox/.claude-plugin/plugin.json) |
| プラグイン | ai-dev-steps | 会社 | AI と一緒に道具やサービスを作る時の手順 1〜9（コンセプト・仕様・画面・試作・価値の検証・本番の実装・価格・デザイン・防犯の点検）を、1段1スキルで進める。入口の dev-start が docs/ を見て「今どの段か・次は何か」を案内する。社内で使う道具なら 5 と 7 は飛ばしてよい。Claude Code と Codex のどちらでも使える。 | [plugin.json](plugins/ai-dev-steps/.claude-plugin/plugin.json) |
| プラグイン | common | 会社 | 全社共通の道具一式。変更を安全に書庫へ保存するスキル（save-to-archive）と、会社のトンマナで広報物を作るスキル（koho-sakusei）の2本を内包する。仕事を始める時の手順は ai-dev-steps に従う。 | [plugin.json](plugins/common/.claude-plugin/plugin.json) |
| プラグイン | sho-san | 会社 | 「SHO-SAN ではこう使っている」の見本。仕事の進め方（grill・handoff・nihongo・org-rebuild・proposal-duplication）、資料作成（visual-design・explain-visual・slide-deck-create・doc-kit・stack-diagram）、画面づくり（ux-review・design-review・web-preflight）の13本を内包する。どれも汎用に書き直してあり、見た目は DESIGN.md、置き場所は CLAUDE.md に従う。要らなければ marketplace.json から外してよい。 | [plugin.json](plugins/sho-san/.claude-plugin/plugin.json) |
