#!/usr/bin/env zsh

REPO="https://github.com/tighug/dotfiles.git"
DOTFILES="${HOME}/dotfiles"

if type git >/dev/null 2>&1; then
    git clone "${REPO}" "${DOTFILES}"

    echo -e "\nInstallaing plugins..."
    git clone "https://github.com/zsh-users/zsh-autosuggestions.git" "${DOTFILES}/.zsh/zsh-autosuggestions"
    git clone "https://github.com/zsh-users/zsh-syntax-highlighting.git" "${DOTFILES}/.zsh/zsh-syntax-highlighting"

    items=(".zshrc" ".gitconfig" ".vimrc" ".config" ".zsh")
    rm -rf "${HOME}/.zsh"
    rm -rf "${HOME}/.config"

    echo -e "\nLinking..."
    for i in ${items[@]}; do
        ln -snfv "${DOTFILES}/$i" "${HOME}/$i"
    done

    echo -e "\nReloading..."
    source "${HOME}/.zshrc"
else
    echo "Error: git is not found."
fi
