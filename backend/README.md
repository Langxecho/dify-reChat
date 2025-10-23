# Dify ReChat - 后端

基于FastAPI的后端服务，为Dify工作流提供API封装。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 数据库配置（使用你的MySQL服务器）
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/dify_rechat?charset=utf8mb4

# JWT密钥（请修改为随机字符串）
SECRET_KEY=your-super-secret-key-min-32-chars

# Dify API配置
DIFY_API_URL=https://api.dify.ai
```

### 3. 创建数据库

登录MySQL创建数据库：

```sql
CREATE DATABASE dify_rechat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 运行数据库迁移

```bash
# 生成初始迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 开发模式（热更新）
uvicorn app.main:app --reload

# 或使用
python -m app.main
```

服务将在 `http://localhost:8000` 启动

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由
│   │   ├── deps.py       # 依赖注入
│   │   └── v1/           # API v1版本
│   │       ├── auth.py   # 认证相关
│   │       ├── chat.py   # 聊天相关
│   │       ├── conversations.py
│   │       └── admin.py  # 管理员相关
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   ├── database.py   # 数据库配置
│   │   └── security.py   # 安全相关（JWT、密码）
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模型
│   ├── services/         # 业务逻辑
│   │   └── dify_client.py # Dify API客户端
│   └── main.py           # 应用入口
├── alembic/              # 数据库迁移
├── requirements.txt
└── .env.example
```

## 主要功能

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户信息

### 聊天
- `POST /api/v1/chat/stream` - 流式聊天（SSE）

### 对话管理
- `GET /api/v1/conversations` - 获取对话列表
- `GET /api/v1/conversations/{id}` - 获取对话详情
- `GET /api/v1/conversations/{id}/messages` - 获取对话消息
- `PATCH /api/v1/conversations/{id}` - 更新对话
- `DELETE /api/v1/conversations/{id}` - 删除对话

### 管理员
- `GET /api/v1/admin/dify/config` - 获取Dify配置
- `POST /api/v1/admin/dify/config` - 设置Dify API密钥
- `DELETE /api/v1/admin/dify/config` - 删除Dify配置

## 常见问题

### 1. 数据库连接失败
检查 `.env` 中的 `DATABASE_URL` 是否正确，确保MySQL服务正在运行。

### 2. 导入错误
确保在 `backend` 目录下运行命令。

### 3. 迁移失败
删除 `alembic/versions/` 下的迁移文件，重新生成。
