##构建前端
FROM node AS builder

WORKDIR /frontend
COPY /frontend /frontend

RUN yarn && yarn run build

FROM nginx:stable-alpine

COPY --from=builder /frontend/dist/my-app/browser /usr/share/nginx/html

##构建后端

FROM python:3.9.19-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh


##暴露端口
EXPOSE 80 18964

## 安装supervisor
RUN apt-get update && \
    apt-get install -y supervisor nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

