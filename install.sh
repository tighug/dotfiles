#!/usr/bin/env zsh
set -euo pipefail

REPO="https://github.com/tighug/dotfiles.git"
DOTFILES="${HOME}/dotfiles"

if ! command -v git >/dev/null 2>&1; then
    echo "Error: git is not found."
    exit 1
fi

[[ -d "${DOTFILES}" ]] || git clone "${REPO}" "${DOTFILES}"

echo -e "\nInstalling plugins..."
[[ -d "${DOTFILES}/.zsh/zsh-autosuggestions" ]] || git clone "https://github.com/zsh-users/zsh-autosuggestions.git" "${DOTFILES}/.zsh/zsh-autosuggestions"
[[ -d "${DOTFILES}/.zsh/zsh-syntax-highlighting" ]] || git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "${DOTFILES}/.zsh/zsh-syntax-highlighting"

echo -e "\nLinking..."
items=(".zshrc" ".gitconfig" ".vimrc" ".config" ".zsh")
backup_suffix=".bak.$(date +%Y%m%d%H%M%S)"
for i in ${items[@]}; do
    target="${HOME}/$i"
    if [[ -e "${target}" && ! -L "${target}" ]]; then
        echo "Backing up existing ${target} to ${target}${backup_suffix}"
        mv "${target}" "${target}${backup_suffix}"
    fi
    ln -snfv "${DOTFILES}/$i" "${target}"
done

target="${HOME}/.claude/statusline.py"
mkdir -p "${HOME}/.claude"
if [[ -e "${target}" && ! -L "${target}" ]]; then
    echo "Backing up existing ${target} to ${target}${backup_suffix}"
    mv "${target}" "${target}${backup_suffix}"
fi
ln -snfv "${DOTFILES}/.claude/statusline.py" "${target}"

echo -e "\nDone. Run 'source ~/.zshrc' or open a new shell to apply."
