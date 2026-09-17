# CLAUDE.md

このファイルは、本リポジトリでコードを扱う際の Claude Code (claude.ai/code) への指示を記述する。

## 概要

tighug 個人用の dotfiles リポジトリ。設定ファイルは `install.sh` によって `~/dotfiles` から `$HOME` へシンボリックリンクされる。主な環境は Windows 上の WSL2 (Ubuntu) で、一部 macOS (Karabiner) もサポートする。

## セットアップ

```bash
# インストール（リポジトリの clone、zsh プラグインの導入、シンボリックリンクの作成）
curl -L raw.githubusercontent.com/tighug/dotfiles/main/install.sh | zsh
```

インストールスクリプトは `.zshrc`、`.gitconfig`、`.vimrc`、`.config/`、`.zsh/`、`.claude/statusline.py` をホームディレクトリにシンボリックリンクする。リンク先にシンボリックリンクでない実体が既にある場合はタイムスタンプ付きでバックアップしてから上書きするため、再実行しても安全。注意: `.wezterm.lua` は install スクリプトの管理対象**外**で、Windows ホスト側へ手動で配置する必要がある。

## アーキテクチャ

- **シンボリックリンク方式**: すべての dotfiles はこのリポジトリに置かれ、`$HOME` にシンボリックリンクされる。ここのファイルを編集すると、有効な設定が直接更新される。
- **フォント**: FiraCode Nerd Font（メイン）＋ Noto Sans JP（CJK フォールバック）。Starship で Nerd Font アイコンを使用。

## 主要な設定対象ツール

| ツール | 設定パス | 用途 |
|---|---|---|
| zsh | `.zshrc`, `.zsh/` | シェル、プラグイン (autosuggestions, syntax-highlighting)、補完 |
| Starship | `.config/starship.toml` | プロンプト |
| Vim | `.vimrc` | エディタ（2 スペースタブ、smart case 検索） |
| fastfetch | `.config/fastfetch/config.jsonc` | システム情報表示 |
| Mise | `.config/mise/config.toml` | ランタイムマネージャ (Node.js, npm) |
| Karabiner | `.config/karabiner/` | macOS のキーリマップ（Vim 風矢印、JP/EN 切替） |
| gh | `.config/gh/config.yml` | GitHub CLI（HTTPS、`pr checkout` の `co` エイリアス） |
| git | `.config/git/ignore` | グローバル gitignore（`.claude/settings.local.json` を除外） |
| mimeapps.list | `.config/mimeapps.list` | `claude-cli://` スキームハンドラーの登録 |
| Claude Code | `.claude/statusline.py` | カスタムステータスライン |

## Claude Code 連携

- **zsh**: `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` で Claude のターミナルタイトル変更を抑制
- **mimeapps.list**: `claude-cli://` URL スキームハンドラーを登録
- **エイリアス**: `cc`=`claude`, `ccd`=`claude --dangerously-skip-permissions`, `cca`=`claude --enable-auto-mode`

## 変更の反映

設定ファイルはシンボリックリンク経由で `$HOME` に反映されているため、ここのファイルを編集すると即座に反映される。ただし以下は再読み込みが必要:

- **zsh**: `source ~/.zshrc` またはシェル再起動
- **Starship**: 次のプロンプト表示時に自動反映
- **WezTerm**: リポジトリ管理外。Windows 側のファイルを手動編集する（`/mnt/c/Users/<user>/.wezterm.lua`）

## 規約

- `.zshrc` で `exa` を `ls` にエイリアス。
- エディタ（Vim）のタブ幅は 2 スペース。
- Git プロトコルは HTTPS（SSH ではない）。gh と git 両方で設定済み。
- `.gitignore` は `.zsh/*` を除外（`.zsh/completion/` は例外）し、`.config/yarn`、`.config/uv/`、`.config/gh/hosts.yml`、`.config/karabiner/automatic_backups/` も除外する。
