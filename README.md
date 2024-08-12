# easybangumi 追番助手

![前端根本不会啊！！](https://github.com/plsy1/easybangumi/blob/main/pictures/frontend.png?raw=true)

## Features

- ✅ Automatically download subscribed anime
- ✅ Automatically rename anime episodes
- ✅ Receive updates notifications
- ✅ Add, collect, and delete subscriptions
- ✅ Flexible episode directory formats
  - TMDB format: Title/Season x/SXXEYY
  - Bangumi format: Title/Season 1/S01EYY
- ✅ Automatically update Bangumi watching progress (Based on file paths, subscribed anime always succeeds, non-subscribed anime usually works as well)
  - Enable for TMDB episode directory format
  - Disable for Bangumi episode directory format (for now)

## Parameters

### Bamgumi

- 📺 **BANGUMI_TOKEN**: [Bangumi token of your account](https://next.bgm.tv/demo/access-token)

### Qbittorrent

- 🌐 **QBITTORRENT_HOST**: Format as pure IP address e.g., 192.168.0.1
- 🔌 **QBITTORRENT_PORT**: QB port
- 👤 **QBITTORRENT_USERNAME**: Username
- 🔒 **QBITTORRENT_PASSWORD**: Password
- 📁 **QBITTORRENT_ROOT_FOLDER**: Root directory where anime will be downloaded
- 🔖 **QBITTORRENT_TAG**: Torrent tag, optional, default is easybangumi

### RSS

- 📡 **RSS_URL**: RSS subscription link from [Mikan Project](https://mikanani.me/home/mybangumi)
- 🔄 **RSS_SCRAPE**: Can be set to `TMDB` or `Bangumi`, default is `TMDB`

### Telegram (Optional, for receiving anime update notifications)

- 🤖 **TELEGRAM_TOKEN**: Token obtained by creating a bot
- 💬 **TELEGRAM_CHAT_ID**: Chat ID of group/user

## Deployment

### Building Image

```shell
git clone https://github.com/plsy1/easybangumi
cd easybangumi
docker build -t easybangumi .
```

### Docker Cli
```bash
docker run -d \
--name easybangumi \
--network=host \
-e TZ=Asia/Shanghai \
-e TELEGRAM_TOKEN="token" \ #optional
-e TELEGRAM_CHAT_ID="chatid" \ #optional
-e QBITTORRENT_HOST="ip" \
-e QBITTORRENT_PORT="port" \
-e QBITTORRENT_USERNAME="admin" \
-e QBITTORRENT_PASSWORD="admin" \
-e QBITTORRENT_ROOT_FOLDER="/path" \
-e QBITTORRENT_TAG="easybangumi" \ #optional
-e DATABASE_NAME="data.db" \ #optional
-e RSS_URL="your account rss url" \
-e RSS_SCRAPE="TMDB" \ #optional
-e BANGUMI_TOKEN="your token" \ #optional
-v /path/to/your/data.db:/app/data.db \
-p 1888:80 \
-p 18964:18964 \ #"The backend address, visit /docs to view the API documentation."
easybangumi
```

