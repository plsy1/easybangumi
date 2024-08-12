##构建前端
FROM node AS builder

WORKDIR /frontend
COPY /frontend /frontend

RUN yarn && yarn run build


FROM nginx

COPY --from=builder /frontend/dist/my-app/browser /usr/share/nginx/html

## 安装supervisor
RUN apt-get update && \
    apt-get install -y supervisor python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


##构建后端

WORKDIR /app
COPY . /app

RUN pip install --break-system-packages -r requirements.txt

COPY generate_config.sh /app/generate_config.sh
RUN chmod +x /app/generate_config.sh


##暴露端口
EXPOSE 80 18964

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

