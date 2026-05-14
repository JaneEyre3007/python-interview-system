FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY back/ /app/back/
COPY front/dist/ /app/front/dist/

# 安装Python依赖
WORKDIR /app/back
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# 收集静态文件
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# 启动脚本
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
