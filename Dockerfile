# 使用 Ubuntu 官方最新镜像
FROM ubuntu:latest

# 更新系统，并安装 nginx 和所需依赖
RUN apt-get update && apt-get install -y nginx curl ca-certificates

# 复制 Nginx 配置文件到正确位置
COPY nginx.conf /etc/nginx/nginx.conf

# 创建 media 目录
RUN mkdir -p /opt/render/project/media/

# 设置 nginx 的静态文件目录
WORKDIR /opt/render/project

# 让 Render 识别 media 目录
VOLUME /opt/render/project/media

# 暴露 80 端口
EXPOSE 80

# 让 Nginx 以前台模式运行
CMD ["nginx", "-g", "daemon off;"]