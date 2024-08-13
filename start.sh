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
  tag: "$QBITTORRENT_TAG"

database:
  name: "$DATABASE_NAME"

rss:
  url: "$RSS_URL"
  scrape: "$RSS_SCRAPE"
  
bangumi:
  token: "$BANGUMI_TOKEN"
EOF

mv config.yaml /app/conf/config.yaml



# 获取容器的 IP 地址
IP_ADDRESS=$(hostname -I | awk '{print $1}')
# 替换配置文件中的 localhost 为容器的 IP 地址
find /usr/share/nginx/html/ -type f -name "main*.js" -exec sed -i "s|http://localhost:18964|http://${IP_ADDRESS}:18964|g" {} +

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf


