FROM nginx

COPY  /frontend/dist/my-app/browser /usr/share/nginx/html

RUN apt-get update && \
    apt-get install -y supervisor python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY /backend /app

RUN pip install --break-system-packages -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 12450

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
CMD ["bash", "start.sh"]