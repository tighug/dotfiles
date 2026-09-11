# dotfiles

tighug 個人用の dotfiles。主な対象環境は Windows 上の WSL2 (Ubuntu)、Karabiner のみ macOS 向け。

## Installation

```bash
curl -L raw.githubusercontent.com/tighug/dotfiles/main/install.sh | zsh
```

`.zshrc`、`.gitconfig`、`.vimrc`、`.config/`、`.zsh/` を `$HOME` にシンボリックリンクする。

## 管理対象外のファイル

`.wezterm.lua` はこのリポジトリの管理対象外で、Windows ホスト側 (`C:\Users\<user>\.wezterm.lua`) へ手動で配置する必要がある。

## 設定変更の反映

シンボリックリンク経由のため、ファイルを編集すると即座に反映される。ただし zsh のみ `source ~/.zshrc` または新しいシェルの起動が必要。

## License

[MIT](./LICENSE)
