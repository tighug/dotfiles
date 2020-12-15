#!/usr/bin/env bash

REPO="https://github.com/tighug/dotfiles.git"
DOTFILES="${HOME}/dotfiles"

if type git >/dev/null 2>&1; then
    git clone "${REPO}" "${DOTFILES}"

    echo -e "\nInstallaing plugins..."
    git clone "https://github.com/zsh-users/zsh-autosuggestions.git" "${DOTFILES}/.zsh/zsh-autosuggestions"
    git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "${DOTFILES}/.zsh/zsh-syntax-highlighting"

    items=(".zshrc" ".gitconfig" ".config/starship.toml" ".zsh")
    rm -rf "${HOME}/.zsh"

    for i in ${items[@]}; do
        ln -snfv "${DOTFILES}/$i" "${HOME}/$i"
    done
else
    echo "Error: git is not found."
fi