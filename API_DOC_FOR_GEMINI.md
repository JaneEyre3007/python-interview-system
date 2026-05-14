# Python 面试在线答题系统 — 后端 API 接口文档

## 项目概述

这是一个 Python 面试在线答题系统，功能包括：
- 用户注册/登录（JWT 认证）
- 题库管理（CRUD、筛选、批量删除、文件导入、AI 生成）
- 在线考试（组卷、答题、AI 评判、交卷）
- 考试历史与成绩查看
- Token 用量统计（ECharts 图表）
- 用户个人 AI 模型配置

## 认证方式

使用 JWT Bearer Token 认证。登录/注册后获取 `access` 和 `refresh` token。

请求头格式：
```
Authorization: Bearer <access_token>
```

当 access token 过期时，需要使用 refresh token 重新获取。未认证的请求返回 `401`。

## Base URL

```
后端地址: http://localhost:8000（开发环境）
所有 API 路径均以 /api/ 开头
```

---

## 一、用户模块 `/api/users/`

### 1.1 注册

```
POST /api/users/register/
```

**无需认证**

请求体：
```json
{
  "username": "testuser",
  "password": "123456",
  "email": "test@example.com"
}
```

- `username`: string, 必填
- `password`: string, 必填, 最少6位
- `email`: string, 必填

成功响应 `201`：
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "date_joined": "2025-05-12T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ...",
    "access": "eyJ..."
  }
}
```

失败响应 `400`：
```json
{
  "username": ["该用户名已被使用"],
  "password": ["确保该字段至少包含 6 个字符"]
}
```

---

### 1.2 登录

```
POST /api/users/login/
```

**无需认证**

请求体：
```json
{
  "username": "testuser",
  "password": "123456"
}
```

成功响应 `200`：
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "date_joined": "2025-05-12T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ...",
    "access": "eyJ..."
  }
}
```

失败响应 `401`：
```json
{
  "error": "用户名或密码错误"
}
```

---

### 1.3 获取用户信息

```
GET /api/users/profile/
```

**需要认证**

成功响应 `200`：
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "date_joined": "2025-05-12T10:00:00Z"
}
```

---

### 1.4 获取 AI 配置

```
GET /api/users/ai-config/
```

**需要认证**

成功响应 `200`（已配置）：
```json
{
  "id": 1,
  "provider": "openai",
  "api_key": "sk-12345678****",
  "api_url": "https://api.example.com/v1",
  "model_name": "mimo-v2.5-pro",
  "is_active": true
}
```

成功响应 `200`（未配置，返回默认值）：
```json
{
  "provider": "openai",
  "api_key": "",
  "api_url": "",
  "model_name": "",
  "is_active": false
}
```

---

### 1.5 创建/更新 AI 配置

```
POST /api/users/ai-config/
```

**需要认证**

请求体：
```json
{
  "provider": "openai",
  "api_key": "sk-xxxxxxxxxxxxx",
  "api_url": "https://api.example.com/v1",
  "model_name": "mimo-v2.5-pro",
  "is_active": true
}
```

- `provider`: string, 可选值: `"openai"` | `"custom"`, 默认 `"openai"`
- `api_key`: string, 必填
- `api_url`: string, 必填
- `model_name`: string, 默认 `"mimo-v2.5-pro"`
- `is_active`: boolean, 默认 `true`

成功响应 `200`：
```json
{
  "id": 1,
  "provider": "openai",
  "api_url": "https://api.example.com/v1",
  "model_name": "mimo-v2.5-pro",
  "is_active": true
}
```

> 注意：api_key 为 write_only，响应中不返回。

---

### 1.6 删除 AI 配置

```
DELETE /api/users/ai-config/
```

**需要认证**

成功响应 `200`：
```json
{
  "message": "配置已删除"
}
```

失败响应 `404`：
```json
{
  "error": "配置不存在"
}
```

---

## 二、题目模块 `/api/questions/`

### 2.1 获取题目列表（分页）

```
GET /api/questions/
```

**需要认证**（只返回当前用户的题目）

查询参数：
- `type`: 题目类型筛选, 可选值: `choice` | `fill` | `code` | `short`
- `difficulty`: 难度筛选, 可选值: `easy` | `medium` | `hard`
- `category`: 分类ID筛选, 整数
- `page`: 页码, 默认 1
- `page_size`: 每页数量

成功响应 `200`：
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/questions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "type": "choice",
      "difficulty": "medium",
      "category": 1,
      "category_name": "Python基础",
      "content": "Python中以下哪个不是可变类型？",
      "options": {
        "A": "list",
        "B": "dict",
        "C": "tuple",
        "D": "set"
      },
      "answer": "C",
      "explanation": "tuple是不可变类型",
      "created_by_ai": false,
      "created_at": "2025-05-12T10:00:00Z",
      "updated_at": "2025-05-12T10:00:00Z"
    }
  ]
}
```

---

### 2.2 创建题目

```
POST /api/questions/
```

**需要认证**

请求体：
```json
{
  "type": "choice",
  "difficulty": "medium",
  "category": 1,
  "content": "Python中以下哪个不是可变类型？",
  "options": {
    "A": "list",
    "B": "dict",
    "C": "tuple",
    "D": "set"
  },
  "answer": "C",
  "explanation": "tuple是不可变类型"
}
```

- `type`: string, 必填, 可选值: `"choice"` | `"fill"` | `"code"` | `"short"`
- `difficulty`: string, 可选, 可选值: `"easy"` | `"medium"` | `"hard"`, 默认 `"medium"`
- `category`: integer, 可选, 分类ID
- `content`: string, 必填, 题目内容
- `options`: object, 可选, 选择题的选项 `{"A": "...", "B": "...", "C": "...", "D": "..."}`
- `answer`: string, 必填, 正确答案
- `explanation`: string, 可选, 答案解析

成功响应 `201`：返回创建的题目对象（同 2.1 中的单个题目结构）

---

### 2.3 获取单个题目

```
GET /api/questions/{id}/
```

**需要认证**

成功响应 `200`：返回单个题目对象

---

### 2.4 更新题目

```
PUT /api/questions/{id}/
```

**需要认证**

请求体同 2.2，所有字段必填。也支持 `PATCH` 做部分更新。

---

### 2.5 删除题目

```
DELETE /api/questions/{id}/
```

**需要认证**

成功响应 `204`：无内容

---

### 2.6 随机获取题目

```
GET /api/questions/random/
```

**需要认证**

查询参数：
- `count`: 数量, 默认 10

成功响应 `200`：返回题目数组

---

### 2.7 批量删除题目

```
POST /api/questions/batch_delete/
```

**需要认证**

请求体：
```json
{
  "ids": [1, 2, 3, 4, 5]
}
```

成功响应 `200`：
```json
{
  "message": "成功删除 5 道题目"
}
```

---

### 2.8 导入题目（文件上传）

```
POST /api/questions/import_questions/
```

**需要认证**

请求格式：`multipart/form-data`

表单字段：
- `file`: 上传文件, 支持 `.json` / `.csv` / `.xlsx` / `.xls`

JSON 文件格式（数组或 `{ "questions": [...] }`）：
```json
[
  {
    "type": "choice",
    "difficulty": "easy",
    "content": "题目内容",
    "options": {"A": "选项A", "B": "选项B", "C": "选项C", "D": "选项D"},
    "answer": "A",
    "explanation": "解析"
  }
]
```

CSV 文件列名：`type, difficulty, content, option_a, option_b, option_c, option_d, answer, explanation`

Excel 文件列名同 CSV。

成功响应 `200`：
```json
{
  "message": "成功导入 10 道题目"
}
```

---

### 2.9 获取分类列表

```
GET /api/questions/categories/
```

**需要认证**

成功响应 `200`：
```json
[
  {
    "id": 1,
    "name": "Python基础",
    "description": "Python基础语法和数据类型",
    "created_at": "2025-05-12T10:00:00Z"
  }
]
```

---

### 2.10 创建分类

```
POST /api/questions/categories/
```

**需要认证**

请求体：
```json
{
  "name": "Python基础",
  "description": "Python基础语法和数据类型"
}
```

成功响应 `201`：返回分类对象

---

### 2.11 更新/删除分类

```
PUT /api/questions/categories/{id}/
PATCH /api/questions/categories/{id}/
DELETE /api/questions/categories/{id}/
```

**需要认证**

---

## 三、考试模块 `/api/exams/`

### 3.1 获取考试列表

```
GET /api/exams/
```

**需要认证**（只返回当前用户的考试）

成功响应 `200`（分页）：
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "title": "Python基础测试",
      "total_score": 100,
      "status": "completed",
      "started_at": "2025-05-12T10:00:00Z",
      "finished_at": "2025-05-12T10:30:00Z",
      "created_at": "2025-05-12T09:55:00Z",
      "questions": [
        {
          "id": 1,
          "question": {
            "id": 1,
            "type": "choice",
            "difficulty": "medium",
            "content": "题目内容...",
            "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
            "answer": "C",
            "explanation": "...",
            "created_by_ai": false,
            "created_at": "...",
            "updated_at": "..."
          },
          "order": 1,
          "score": 10
        }
      ],
      "answers": []
    }
  ]
}
```

---

### 3.2 获取单个考试

```
GET /api/exams/{id}/
```

**需要认证**

成功响应 `200`：返回单个考试对象（结构同 3.1 中的单个考试）

---

### 3.3 创建考试（组卷）

```
POST /api/exams/create_exam/
```

**需要认证**

请求体：
```json
{
  "title": "Python基础测试",
  "question_count": 10,
  "question_type": "mixed",
  "difficulty": "mixed"
}
```

- `title`: string, 必填, 最长200字
- `question_count`: integer, 可选, 默认10, 范围 1~50
- `question_type`: string, 可选, 可选值: `"choice"` | `"fill"` | `"code"` | `"short"` | `"mixed"`, 默认 `"mixed"`
- `difficulty`: string, 可选, 可选值: `"easy"` | `"medium"` | `"hard"` | `"mixed"`, 默认 `"mixed"`

成功响应 `201`：返回考试对象（包含随机抽取的题目）

失败响应 `400`：
```json
{
  "error": "题库中符合条件的题目不足，仅有5道"
}
```

---

### 3.4 开始考试

```
POST /api/exams/{id}/start/
```

**需要认证**

> 仅当考试状态为 `pending` 时可调用

成功响应 `200`：返回更新后的考试对象（status 变为 `"in_progress"`）

失败响应 `400`：
```json
{
  "error": "试卷状态不允许开始"
}
```

---

### 3.5 提交单题答案

```
POST /api/exams/{id}/submit_answer/
```

**需要认证**

> 仅当考试状态为 `in_progress` 时可调用

请求体：
```json
{
  "question_id": 1,
  "answer": "C"
}
```

- `question_id`: integer, 必填
- `answer`: string, 必填, 用户的答案

成功响应 `200`：
```json
{
  "id": 1,
  "exam": 1,
  "question": 1,
  "question_content": "Python中以下哪个不是可变类型？",
  "user_answer": "C",
  "is_correct": true,
  "score": 10,
  "ai_feedback": "回答正确！",
  "created_at": "2025-05-12T10:05:00Z"
}
```

> 选择题直接比对答案；其他题型（填空、编程、简答）会调用 AI 评判。
> 重复提交同一题目会更新之前的答案。

---

### 3.6 交卷（结束考试）

```
POST /api/exams/{id}/finish/
```

**需要认证**

> 仅当考试状态为 `in_progress` 时可调用

成功响应 `200`：
```json
{
  "exam": { ... },
  "total_score": 80,
  "correct_count": 8,
  "total_count": 10
}
```

---

### 3.7 查看考试结果

```
GET /api/exams/{id}/result/
```

**需要认证**

成功响应 `200`：
```json
{
  "exam": { ... },
  "answers": [
    {
      "id": 1,
      "exam": 1,
      "question": 1,
      "question_content": "题目内容...",
      "user_answer": "C",
      "is_correct": true,
      "score": 10,
      "ai_feedback": "回答正确！",
      "created_at": "2025-05-12T10:05:00Z"
    }
  ],
  "total_score": 80,
  "correct_count": 8
}
```

---

## 四、AI 模块 `/api/ai/`

### 4.1 AI 生成题目

```
POST /api/ai/generate/
```

**需要认证**（需要用户已配置 AI）

请求体：
```json
{
  "topic": "Python装饰器",
  "type": "choice",
  "difficulty": "medium",
  "count": 5,
  "save": true
}
```

- `topic`: string, 可选, 默认 `"Python基础"`
- `type`: string, 可选, 可选值: `"choice"` | `"fill"` | `"code"` | `"short"`, 默认 `"choice"`
- `difficulty`: string, 可选, 可选值: `"easy"` | `"medium"` | `"hard"`, 默认 `"medium"`
- `count`: integer, 可选, 默认 1
- `save`: boolean, 可选, 默认 true, 是否保存到题库

成功响应 `200`：
```json
{
  "message": "成功生成5道题目",
  "questions": [
    {
      "id": 10,
      "type": "choice",
      "difficulty": "medium",
      "content": "关于Python装饰器，以下说法正确的是？",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "answer": "B",
      "explanation": "...",
      "created_by_ai": true,
      "created_at": "..."
    }
  ]
}
```

失败响应 `500`：
```json
{
  "error": "生成题目时出错: 请先配置AI模型"
}
```

---

### 4.2 AI 评判答案

```
POST /api/ai/evaluate/
```

**需要认证**

请求体：
```json
{
  "question": "解释Python中的GIL是什么？",
  "correct_answer": "GIL是全局解释器锁...",
  "user_answer": "GIL是一种线程锁机制..."
}
```

- `question`: string, 必填
- `correct_answer`: string, 必填
- `user_answer`: string, 必填

成功响应 `200`：
```json
{
  "feedback": "回答基本正确。你正确指出了GIL是一种锁机制，但还可以补充..."
}
```

---

### 4.3 Token 用量统计

```
GET /api/ai/token-stats/
```

**需要认证**

查询参数：
- `days`: 统计天数, 默认 30

成功响应 `200`：
```json
{
  "total": {
    "prompt_tokens": 15000,
    "completion_tokens": 8000,
    "total_tokens": 23000,
    "total_calls": 45
  },
  "generate": {
    "prompt_tokens": 10000,
    "completion_tokens": 5000,
    "total_tokens": 15000,
    "call_count": 20
  },
  "evaluate": {
    "prompt_tokens": 5000,
    "completion_tokens": 3000,
    "total_tokens": 8000,
    "call_count": 25
  },
  "daily": [
    {
      "date": "2025-05-10",
      "prompt_tokens": 2000,
      "completion_tokens": 1000,
      "total_tokens": 3000,
      "call_count": 5
    }
  ],
  "daily_generate": [
    {
      "date": "2025-05-10",
      "total_tokens": 2000,
      "call_count": 3
    }
  ],
  "daily_evaluate": [
    {
      "date": "2025-05-10",
      "total_tokens": 1000,
      "call_count": 2
    }
  ],
  "recent": [
    {
      "id": 1,
      "api_type": "generate",
      "prompt_tokens": 500,
      "completion_tokens": 300,
      "total_tokens": 800,
      "model_name": "mimo-v2.5-pro",
      "created_at": "2025-05-12T10:00:00Z"
    }
  ]
}
```

---

## 五、枚举值速查

### 题目类型 (type)
| 值 | 含义 |
|---|---|
| `choice` | 选择题 |
| `fill` | 填空题 |
| `code` | 编程题 |
| `short` | 简答题 |

### 难度 (difficulty)
| 值 | 含义 |
|---|---|
| `easy` | 简单 |
| `medium` | 中等 |
| `hard` | 困难 |

### 考试状态 (status)
| 值 | 含义 |
|---|---|
| `pending` | 待开始 |
| `in_progress` | 进行中 |
| `completed` | 已完成 |

### AI 提供商 (provider)
| 值 | 含义 |
|---|---|
| `openai` | OpenAI 兼容接口 |
| `custom` | 自定义 |

### Token 用量类型 (api_type)
| 值 | 含义 |
|---|---|
| `generate` | 生成题目 |
| `evaluate` | 评判答案 |

---

## 六、页面需求（前端需要实现的页面）

### 6.1 登录页 `/login`
- 用户名 + 密码表单
- 跳转注册链接
- 登录成功后保存 token 并跳转首页

### 6.2 注册页 `/register`
- 用户名 + 邮箱 + 密码 + 确认密码 表单
- 注册成功后自动登录并跳转首页

### 6.3 首页/仪表盘 `/`
- 统计卡片：题库总数、已完成考试数、平均分、学习时长
- 快捷操作入口：开始考试、管理题库、AI生成题目、查看历史

### 6.4 题库管理 `/questions`
- 题目列表（表格，分页）
- 筛选条件：题目类型、难度、分类
- 操作：新增、编辑、删除、批量删除
- AI 生成题目弹窗（输入主题、类型、难度、数量）
- 文件导入弹窗（支持 JSON/CSV/Excel）

### 6.5 组卷页 `/exam`
- 表单：试卷标题、题目数量（滑块 1~50）、题目类型（单选）、难度（单选）
- 提交后跳转到考试页

### 6.6 考试页 `/exam/:id`
- 左侧/主区域：题目展示 + 答题区
  - 选择题：单选按钮
  - 填空题：输入框
  - 编程题：代码输入区
  - 简答题：多行文本框
- 右侧/侧边栏：答题卡（题号网格，已答/未答颜色区分）
- 上/下一题导航
- 交卷按钮

### 6.7 考试结果页 `/result/:id`
- 成绩概览：总分、正确率、圆形进度图
- 逐题回顾：题目、用户答案、正确答案、AI 反馈

### 6.8 考试历史 `/history`
- 历史记录表格：标题、状态标签、分数、时间
- 操作：查看详情、继续考试（进行中的）

### 6.9 Token 统计 `/token-stats`
- 统计卡片：总 Token 数、总调用次数、生成/评判各自统计
- 图表1：每日 Token 用量堆叠柱状图（生成 vs 评判）
- 图表2：调用类型分布饼图
- 最近调用记录表格

### 6.10 AI 配置 `/ai-config`
- 表单：提供商选择、API Key、API 地址、模型名称、启用开关
- 保存/删除操作

---

## 七、全局导航

顶部导航栏包含：
- Logo / 系统名称
- 菜单项：首页、题库管理、开始考试、考试历史、Token 统计
- 右侧：用户名下拉菜单 → AI 配置、退出登录

未登录时只显示登录/注册页，不显示导航栏。

---

## 八、技术建议

前端建议使用：
- Vue 3 + Vite（与现有后端 CORS 配置兼容）
- 任意现代 UI 方案（Tailwind CSS、Naive UI 等，追求美观）
- Axios 做 HTTP 请求
- Pinia 做状态管理
- Vue Router 做路由
- ECharts 做图表

开发时前端运行在 `http://localhost:5173`，后端已配置 CORS 允许跨域。
