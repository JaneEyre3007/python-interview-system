#!/bin/bash

# 运行数据库迁移
cd /app/back
python manage.py migrate --noinput

# 启动Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120
