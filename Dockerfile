# 使用官方 Ubuntu 作为基础镜像
FROM ubuntu:latest

# 更新包管理器并安装 Nginx
RUN apt-get update && apt-get install -y nginx

# 创建 media 目录（确保目录存在）
RUN mkdir -p /opt/render/project/media/

# 复制本地 media 目录到容器中
COPY media /opt/render/project/media/

# 复制 Nginx 配置文件到正确的位置
COPY nginx.conf /etc/nginx/nginx.conf

# 设置工作目录
WORKDIR /opt/render/project

# 暴露 80 端口（和 Render 配置的 PORT 变量一致）
EXPOSE 80

# 让 Nginx 以前台模式运行
CMD ["nginx", "-g", "daemon off;"]