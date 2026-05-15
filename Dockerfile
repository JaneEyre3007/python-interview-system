ARG CACHE_BUST=2
# Stage 1: Build Vue.js frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/front
COPY front/package*.json ./
RUN npm install
COPY front/ .
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY back/ /app/back/

# 复制前端构建产物
COPY --from=frontend-build /app/front/dist/ /app/front/dist/

# 安装Python依赖
WORKDIR /app/back
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# 启动脚本
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
