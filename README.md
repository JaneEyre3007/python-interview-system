# Python面试在线答题系统

基于Django + Vue 3的前后端分离项目，接入小米MiMo大模型API，实现在线出题和在线判题功能。

## 技术栈

### 后端
- Django 4.2
- Django REST Framework
- SQLite (开发环境)
- 小米MiMo大模型API

### 前端
- Vue 3
- Element Plus
- Pinia (状态管理)
- Axios (HTTP请求)

## 项目结构

```
E:\python面试在线答题系统\
├── back/                    # 后端代码
│   ├── config/              # Django配置
│   ├── apps/                # 应用模块
│   │   ├── users/           # 用户模块
│   │   ├── questions/       # 题目模块
│   │   ├── exams/           # 考试模块
│   │   └── ai/              # AI模块
│   ├── manage.py
│   └── requirements.txt
│
└── front/                   # 前端代码
    ├── src/
    │   ├── api/             # API请求
    │   ├── views/           # 页面组件
    │   ├── components/      # 公共组件
    │   ├── router/          # 路由配置
    │   └── store/           # 状态管理
    ├── package.json
    └── vite.config.js
```

## 安装和运行

### 后端

1. 进入后端目录
```bash
cd back
```

2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
copy .env.example .env
# 编辑 .env 文件，填入MiMo API Key
```

5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 创建超级用户
```bash
python manage.py createsuperuser
```

7. 运行服务器
```bash
python manage.py runserver
```

### 前端

1. 进入前端目录
```bash
cd front
```

2. 安装依赖
```bash
npm install
```

3. 运行开发服务器
```bash
npm run dev
```

4. 访问 http://localhost:5173

## 功能模块

1. **用户模块** - 注册、登录、个人信息管理
2. **题库模块** - 题目浏览、筛选、AI生成题目
3. **考试模块** - 创建试卷、在线答题、自动判题
4. **成绩模块** - 答题记录、成绩分析、AI反馈

## API接口

### 用户接口
- `POST /api/users/register/` - 用户注册
- `POST /api/users/login/` - 用户登录
- `GET /api/users/profile/` - 获取用户信息

### 题目接口
- `GET /api/questions/` - 获取题目列表
- `POST /api/questions/` - 创建题目
- `GET /api/questions/random/` - 随机获取题目

### 考试接口
- `POST /api/exams/create_exam/` - 创建考试
- `POST /api/exams/{id}/start/` - 开始考试
- `POST /api/exams/{id}/submit_answer/` - 提交答案
- `POST /api/exams/{id}/finish/` - 完成考试
- `GET /api/exams/{id}/result/` - 获取考试结果

### AI接口
- `POST /api/ai/generate/` - AI生成题目
- `POST /api/ai/evaluate/` - AI评判答案

## MiMo API配置

在 `back/.env` 文件中配置：

```
MIMO_API_KEY=your_api_key_here
MIMO_API_URL=https://api.mimo.com/v1/chat/completions
```

## License

MIT
