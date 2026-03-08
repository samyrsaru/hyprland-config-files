# If not running interactively, don't do anything
[[ $- != *i* ]] && return

source ~/.shell_common

# nvm (slow loading, bash only)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
alias current-theme="gsettings get org.gnome.desktop.interface gtk-theme"
export TERM=xterm-256color

eval "$(zoxide init bash)"
eval "$(fzf --bash)"

# opencode
export PATH=/home/samyr/.opencode/bin:$PATH
