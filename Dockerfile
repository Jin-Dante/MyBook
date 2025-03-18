# 使用 Ubuntu 作为基础镜像
FROM ubuntu:latest

# 安装 Nginx
RUN apt-get update && apt-get install -y nginx

# 复制 nginx 配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 创建 media 目录
RUN mkdir -p /opt/render/project/media/

# 设置 nginx 的静态文件目录
WORKDIR /opt/render/project

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]