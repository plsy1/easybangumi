# easybangumi 自动追番

### Features

- 订阅自动下载
- 番剧自动重命名
- 推送更新通知
- 添加订阅、收集订阅功能
- 可选择的剧集目录格式
  - TMDB格式：Title/Season x/SXXEYY
  - Bangumi格式：Title/Season 1/S01EYY

## Parameters

### Bamgumi

- **BANGUMI_TOKEN**

### Qbittorrent

- **QBITTORRENT_HOST** 形式为纯IP地址 例如：192.168.0.1

- **QBITTORRENT_PORT** QB端口 

- **QBITTORRENT_USERNAME** 用户名

- **QBITTORRENT_PASSWORD** 密码

- **QBITTORRENT_ROOT_FOLDER** 根文件目录 番剧将被下载到里

- **QBITTORRENT_TAG** 种子标签，可不填，默认为easybangumi

### RSS

- **RSS_URL** 账号RSS地址

- **RSS_SCRAPE** 可设置为TMDB或Bangumi，默认为TMDB

### Telegram 用于发送番剧更新提醒 可选

- **TELEGRAM_TOKEN**  创建机器人获得

- **TELEGRAM_CHAT_ID** 群组/用户的chatid

## 部署

#### Docker Cli
```bash
docker run  \
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
-v /path/to/your/data.db:/app/data.db \
easybangumi
```

