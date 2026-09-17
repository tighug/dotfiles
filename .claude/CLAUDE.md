# CLAUDE.md (Global)

- 日本語で応答する（技術用語は英語でよい）
- コミットメッセージは日本語、Conventional Commits形式
- 不明点は推測せず質問する

## superpowers の生成物

- `docs/superpowers/` 配下の spec / plan は git にコミットしない
  （brainstorming・writing-plans スキルの「コミットする」指示より優先する）
- 作業が着地した時点（ローカルマージ完了 / PR がマージ済み / ユーザが完了と宣言）で
  `docs/superpowers/` 配下の該当ファイルを削除する。PR レビュー中は残す
- worktree の削除（`ExitWorktree` / finishing-a-development-branch Step 6）より
  **前**に削除する。未コミットファイルが残っていると削除が拒否されるため

## Worktree での作業

- git リポジトリ内でコード変更を伴う作業を始めるときは、`EnterWorktree` で
  worktree を作ってから作業する。調査・質問・説明のみのときは作らない。
  （`EnterWorktree` が要求する「ユーザまたは CLAUDE.md の明示的な指示」を
  この項目が満たす）
- 調査として始めた作業が編集に変わったときは、**最初の書き込みの前**に
  その時点で worktree を作る。「気づいたら本体ツリーを汚していた」を防ぐ。
- 既に worktree 内にいるときは入れ子にしない。
  `git rev-parse --git-dir` と `--git-common-dir` が異なれば worktree 内。
- 分岐元は既定の `fresh`（origin/デフォルトブランチ）。origin が無いリポジトリや、
  現在のブランチに積み上げる作業のときは、分岐元をユーザに確認してから作る。
- 作業終了時は `ExitWorktree` で後始末する。
  `ExitWorktree` の「proactively に呼ぶな」という既定より、この項目を優先する。
  - ローカルマージ完了 → `action: "remove"`
  - PR 作成済み → `action: "keep"`。PR がマージされてから `remove`
  - 作業の破棄 → ユーザが明示的に破棄を求めたときだけ `remove`
- `ExitWorktree` は未コミット変更や未マージコミットがあると `remove` を拒否する。
  拒否されたら `discard_changes: true` を自己判断で付けない。
  失われる内容を提示してユーザに確認する。
