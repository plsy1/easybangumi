# 使用官方 Python 镜像作为基础镜像
FROM python:3.9.19-slim

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录下的所有文件复制到 /app 中
COPY . /app

# 安装依赖
RUN pip install -r requirements.txt

# 复制启动脚本到容器中
COPY start.sh /app/start.sh

RUN mkdir -p /app/conf

# 定义容器启动时要运行的命令
CMD ["bash", "start.sh"]
