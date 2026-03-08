# ⚠️ IMPORTANT - SSH and GPG Keys Not in Git

Your SSH and GPG keys have been **excluded** from this Git repository for security reasons.

These files are still in your backup folder locally:
- `ssh/.ssh/` - SSH keys and config
- `gnupg/.gnupg/` - GPG keys

## How to backup these separately:

### Option 1: Keep local backup only
The files are in `~/hyprland-config-files/ssh/` and `~/hyprland-config-files/gnupg/` - copy these manually after reinstall.

### Option 2: Private GitHub repo
```bash
# Create a private repo
gh repo create hyprland-secrets --private

# Initialize and push only the sensitive files
cd ~/hyprland-config-files
git init secrets-backup
cd secrets-backup
cp -r ../ssh ../gnupg .
git add .
git commit -m "SSH and GPG keys backup"
git remote add origin git@github.com:samyrsaru/hyprland-secrets.git
git push -u origin main
```

### Option 3: GPG-encrypted archive
```bash
cd ~/hyprland-config-files
tar czf secrets.tar.gz ssh/ gnupg/
gpg -c secrets.tar.gz  # Encrypt with passphrase
# Upload secrets.tar.gz.gpg to cloud storage
rm secrets.tar.gz
```

## What to restore after reinstall:

1. Clone this public repo: `git clone https://github.com/samyrsaru/hyprland-config-files`
2. Copy configs as per RESTORE.md
3. Manually copy your SSH/GPG files from your secure backup

---
**Last updated:** March 2026
