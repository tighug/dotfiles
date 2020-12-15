# alias
alias ls="exa"
alias l="ls"
alias ll="ls -l"
alias la="ls -a"
alias lla="ll -a"
alias lt="ls -T -L 1"
alias lta="lt -a"
alias c="clear"
alias ..="cd .."
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"

# plugin
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# completion
fpath=(~/.zsh/completion $fpath)
autoload -Uz compinit
compinit -u
zstyle ':completion:*:default' menu select=1

# starship
eval "$(starship init zsh)"
