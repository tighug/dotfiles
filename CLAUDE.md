# CLAUDE.md

このファイルは、本リポジトリでコードを扱う際の Claude Code (claude.ai/code) への指示を記述する。

## 概要

tighug 個人用の dotfiles リポジトリ。設定ファイルは `install.sh` によって `~/dotfiles` から `$HOME` へシンボリックリンクされる。主な環境は Windows 上の WSL2 (Ubuntu) で、一部 macOS (Karabiner) もサポートする。

## セットアップ

```bash
# インストール（リポジトリの clone、zsh プラグインの導入、シンボリックリンクの作成）
curl -L raw.githubusercontent.com/tighug/dotfiles/main/install.sh | zsh
```

インストールスクリプトは `.zshrc`、`.gitconfig`、`.vimrc`、`.config/`、`.zsh/` をホームディレクトリにシンボリックリンクする（既存の `.zsh` と `.config` ディレクトリは置き換えられる）。注意: `.wezterm.lua` は install スクリプトの管理対象**外**で、Windows ホスト側へ手動で配置する必要がある。

## アーキテクチャ

- **シンボリックリンク方式**: すべての dotfiles はこのリポジトリに置かれ、`$HOME` にシンボリックリンクされる。ここのファイルを編集すると、有効な設定が直接更新される。
- **テーマ**: 全ツールで Catppuccin を使用。Starship は **Mocha** パレット (`catppuccin_mocha`)、Helix と WezTerm は **Macchiato**、Lazygit は Mocha の hex コードを直接使用。
- **Vim 中心**: システム全体で Vim キーバインドを使用（Zellij の hjkl ペイン移動、Helix/Vim エディタ、macOS では Karabiner で hjkl を矢印キーに割り当て）。
- **フォント**: FiraCode Nerd Font（メイン）＋ Noto Sans JP（CJK フォールバック）。Starship、WezTerm、Lazygit で Nerd Font アイコンを使用。

## 主要な設定対象ツール

| ツール | 設定パス | 用途 |
|---|---|---|
| WezTerm | `.wezterm.lua` | ターミナルエミュレータ（WSL 連携、Catppuccin タブ、タブタイトルに Claude CLI の状態を表示） |
| zsh | `.zshrc`, `.zsh/` | シェル、プラグイン (autosuggestions, syntax-highlighting)、補完 |
| Starship | `.config/starship.toml` | プロンプト（Catppuccin Mocha パレット、Nerd Font アイコン） |
| Zellij | `.config/zellij/` | ターミナルマルチプレクサ（Vim キーバインド、Claude ステータスバー用の zellaude プラグイン） |
| Helix | `.config/helix/config.toml` | エディタ（500ms で自動保存、true color、Catppuccin Macchiato） |
| Vim | `.vimrc` | エディタ（2 スペースタブ、smart case 検索） |
| Yazi | `.config/yazi/` | ファイルマネージャ（toggle-pane プラグイン） |
| Lazygit | `.config/lazygit/config.yml` | Git TUI（delta pager、エディタとして Helix を使用） |
| fastfetch | `.config/fastfetch/config.jsonc` | システム情報表示 |
| Mise | `.config/mise/config.toml` | ランタイムマネージャ (Node.js, npm) |
| Karabiner | `.config/karabiner/` | macOS のキーリマップ（Vim 風矢印、JP/EN 切替） |
| gh | `.config/gh/config.yml` | GitHub CLI（HTTPS、`pr checkout` の `co` エイリアス） |
| git | `.config/git/ignore` | グローバル gitignore（`.claude/settings.local.json` を除外） |
| uv | `.config/uv/` | Python パッケージマネージャ |

## Claude Code 連携

複数のツールが Claude Code と連携する設定を持つ:

- **WezTerm**: タブタイトルで Claude CLI の状態を表示（idle/working/permission を色・アイコンで区別）
- **Zellij**: `zellaude` WASM プラグインによるステータスバー表示（`.config/zellij/layouts/default.kdl`）
- **zsh**: `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` で Claude のターミナルタイトル変更を抑制（WezTerm 側で独自表示するため）
- **mimeapps.list**: `claude-cli://` URL スキームハンドラーを登録
- **エイリアス**: `cc`=`claude`, `ccd`=`claude --dangerously-skip-permissions`, `cca`=`claude --enable-auto-mode`

## 変更の反映

設定ファイルはシンボリックリンク経由で `$HOME` に反映されているため、ここのファイルを編集すると即座に反映される。ただし以下は再読み込みが必要:

- **zsh**: `source ~/.zshrc` またはシェル再起動
- **Starship**: 次のプロンプト表示時に自動反映
- **WezTerm**: Windows 側のファイルなので手動コピーが必要（`cp .wezterm.lua /mnt/c/Users/<user>/`）

## 規約

- `.zshrc` で `exa` を `ls` にエイリアス。その他のエイリアス: `zel` (Zellij)、ディレクトリ追跡付き Yazi の `y` 関数。
- エディタ（Vim、Helix）のタブ幅は 2 スペース。
- Git プロトコルは HTTPS（SSH ではない）。gh と Lazygit の両方で設定済み。
- `.gitignore` は `.zsh/*` を除外（`.zsh/completion/` は例外）し、`.config/yarn` も除外する。
