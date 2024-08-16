#!/bin/bash

# 生成 YAML 配置文件
cat <<EOF > config.yaml
telegram:
  token: "$TELEGRAM_TOKEN"
  chat_id: "$TELEGRAM_CHAT_ID"

qbittorrent:
  host: "$QBITTORRENT_HOST"
  port: $QBITTORRENT_PORT
  username: "$QBITTORRENT_USERNAME"
  password: "$QBITTORRENT_PASSWORD"
  root_folder: "$QBITTORRENT_ROOT_FOLDER"

rss:
  url: "$RSS_URL"
  scrape: "$RSS_SCRAPE"
  
bangumi:
  token: "$BANGUMI_TOKEN"
EOF

mkdir -p conf && mv config.yaml conf/config.yaml

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf


