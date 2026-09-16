# alias
alias ls="eza"
alias l="ls"
alias ll="ls -l"
alias la="ls -a"
alias lla="ll -a"
alias lt="ls -T -L 1"
alias lta="lt -a"
alias c="clear"
alias python="python3"
alias cc="claude"
alias ccd="claude --dangerously-skip-permissions"
alias cca="claude agents --dangerously-skip-permissions"

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

# mise
eval "$("$HOME/.local/bin/mise" activate zsh)"

# claude
export CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1

# ssh-agent
if [ -z "$SSH_AUTH_SOCK" ]; then
  eval "$(ssh-agent -s)" > /dev/null
  ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi

# windows terminal cwd
keep_current_path() {
  printf "\e]9;9;%s\e\\" "$(wslpath -w "$PWD")"
}
precmd_functions+=(keep_current_path)

# Windows Terminal は 24bit 色に対応（Claude Code などの truecolor 判定用）
export COLORTERM=truecolor
