Discord bot
# Features
- Creates new channel when user joins a specific channel

# Deploy
```
pip install -U py-cord\[audio\]
pip install dnspython

vim config.toml
cp utils/neko-bot.service ~/.config/systemd/user
systemctl --user start neko-bot
```
