#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

# Start Hyprland on tty1
if [ "$(tty)" = "/dev/tty1" ]; then
  exec Hyprland
fi
