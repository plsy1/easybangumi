FROM nginx

RUN apt-get update && \
    apt-get install -y supervisor python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

##frontend   
WORKDIR /frontend
COPY  /frontend/dist/my-app/browser /usr/share/nginx/html


##backend
WORKDIR /app
COPY . /app
RUN pip install --break-system-packages -r requirements.txt

COPY generate_config.sh /app/generate_config.sh
RUN chmod +x /app/generate_config.sh

##暴露端口
EXPOSE 80 18964

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

