# Backup Restore Guide

## To restore after fresh install:

### 1. Shell configs
```bash
cp dotfiles/.bash* dotfiles/.zsh* dotfiles/.zprofile dotfiles/.shell_common dotfiles/.gitconfig dotfiles/.gtkrc-2.0 ~/
```

### 2. Config directories
```bash
mkdir -p ~/.config
cp -r config/* ~/.config/
```

### 3. SSH and GPG (be careful with permissions!)
```bash
cp -r ssh/.ssh ~/
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*
cp -r gnupg/.gnupg ~/
chmod 700 ~/.gnupg
```

### 4. Local share
```bash
mkdir -p ~/.local/share
cp -r local/share/* ~/.local/share/
```

### 5. Scripts and wallpapers
```bash
cp -r scripts ~/cp -r wallpapers ~/
```

## Packages to reinstall:
- hyprland waybar kitty rofi mako
- yazi lazygit
- nvim (Neovim)
- zsh oh-my-zsh
- yay (AUR helper)
- nwg-bar nwg-look uwsm
