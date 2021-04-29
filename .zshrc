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

# less
export LESS_TERMCAP_mb=$'\e[1;32m'
export LESS_TERMCAP_md=$'\e[1;32m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[01;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;4;31m'
export GROFF_NO_SGR=1
