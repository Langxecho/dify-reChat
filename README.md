# Dify ReChat

基于Dify工作流API的AI对话平台，提供类似ChatGPT的Web界面。

## 🎯 功能特性

- ✅ 用户注册/登录系统（邮箱+密码）
- ✅ 实时流式AI对话（SSE）
- ✅ 对话历史管理
- ✅ 管理员配置Dify API密钥
- ✅ 响应式UI设计（模仿Open WebUI风格）
- ✅ Markdown渲染支持
- ✅ Docker一键部署

## 🏗️ 技术栈

### 后端
- **FastAPI** - 高性能异步Web框架
- **MySQL** - 数据库（开发+生产）
- **SQLAlchemy** - ORM
- **Alembic** - 数据库迁移
- **JWT** - 身份认证
- **PyMySQL** - MySQL驱动

### 前端
- **Vue 3** - 渐进式前端框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Tailwind CSS** - 样式框架
- **Marked** - Markdown渲染

## 📁 项目结构

```
dify-reChat/
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   ├── alembic/            # 数据库迁移
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Vue 3前端
│   ├── src/
│   │   ├── api/            # API调用
│   │   ├── components/     # Vue组件
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # Pinia状态
│   │   ├── views/          # 页面组件
│   │   └── main.ts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Docker编排
└── README.md
```

## 🚀 快速开始

### 方式1：本地开发（推荐用于开发）

#### 前置要求
- Python 3.10+
- Node.js 18+
- MySQL 5.7+

#### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写你的MySQL配置
```

**.env 配置示例：**
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/dify_rechat?charset=utf8mb4
SECRET_KEY=your-super-secret-key-min-32-chars
DIFY_API_URL=https://api.dify.ai
```

**创建数据库：**
```sql
mysql -u root -p
CREATE DATABASE dify_rechat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**运行迁移：**
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

**启动后端：**
```bash
uvicorn app.main:app --reload
```

后端将运行在 http://localhost:8000

#### 2. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:5173

### 方式2：Docker部署（推荐用于生产）

#### 前置要求
- Docker
- Docker Compose

#### 1. 配置环境变量

```bash
cp .env.production.example .env
# 编辑 .env 文件，修改密码和密钥
```

**.env 示例：**
```env
MYSQL_ROOT_PASSWORD=your-strong-root-password
MYSQL_PASSWORD=your-strong-user-password
SECRET_KEY=your-super-secret-key-please-change-this-to-random-string
DIFY_API_URL=https://api.dify.ai
```

#### 2. 启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

服务将运行在：
- 前端：http://localhost
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/api/docs

## 📖 使用指南

### 1. 注册账号

访问 http://localhost（或 http://localhost:5173 如果是本地开发）

- 点击"立即注册"
- 填写邮箱和密码（至少6位）
- **第一个注册的用户自动成为管理员**

### 2. 配置Dify API（管理员）

登录后，如果你是管理员：

1. 点击左下角"管理"进入管理后台
2. 输入Dify工作流的API密钥
3. 点击"保存配置"

**获取Dify API密钥：**
1. 登录 https://dify.ai
2. 创建或进入你的工作流
3. 在"API访问"中生成API密钥

### 3. 开始对话

1. 返回聊天页面
2. 输入消息并发送
3. AI将实时流式响应
4. 对话自动保存

## 🔧 API文档

启动后端后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 主要API端点

#### 认证
- `POST /api/v1/auth/register` - 注册
- `POST /api/v1/auth/login` - 登录
- `GET /api/v1/auth/me` - 获取当前用户

#### 聊天
- `POST /api/v1/chat/stream` - 流式聊天

#### 对话管理
- `GET /api/v1/conversations` - 对话列表
- `GET /api/v1/conversations/{id}/messages` - 消息列表
- `DELETE /api/v1/conversations/{id}` - 删除对话

#### 管理员
- `GET /api/v1/admin/dify/config` - 获取配置
- `POST /api/v1/admin/dify/config` - 设置API密钥

## 🛠️ 开发

### 后端开发

```bash
cd backend

# 创建新的数据库迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 运行测试
pytest
```

### 前端开发

```bash
cd frontend

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 📝 环境变量说明

### 后端环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | MySQL连接字符串 | 必填 |
| `SECRET_KEY` | JWT密钥（至少32位） | 必填 |
| `JWT_ALGORITHM` | JWT算法 | HS256 |
| `JWT_EXPIRE_MINUTES` | Token过期时间（分钟） | 43200 (30天) |
| `DIFY_API_URL` | Dify API地址 | https://api.dify.ai |
| `DEBUG` | 调试模式 | True |

## ⚠️ 注意事项

1. **安全性**
   - 生产环境务必修改 `SECRET_KEY`
   - 使用强密码保护MySQL
   - 建议配置HTTPS

2. **性能优化**
   - 生产环境建议使用Nginx反向代理
   - 配置数据库连接池
   - 启用gzip压缩

3. **Dify配置**
   - 确保Dify工作流已发布
   - API密钥需要有足够的调用额度
   - 流式响应模式需要Dify支持

## 🐛 常见问题

### 1. 数据库连接失败

**问题：** `Can't connect to MySQL server`

**解决：**
- 检查MySQL是否运行：`mysql -u root -p`
- 确认 `.env` 中的数据库配置正确
- 检查数据库是否已创建

### 2. 前端无法连接后端

**问题：** `Network Error` 或 CORS错误

**解决：**
- 确保后端运行在 http://localhost:8000
- 检查后端 `CORS_ORIGINS` 配置
- 本地开发使用Vite代理配置

### 3. Dify API调用失败

**问题：** 聊天无响应或报错

**解决：**
- 确认管理员已配置API密钥
- 检查Dify工作流状态
- 查看后端日志：`docker-compose logs backend`

### 4. Docker构建失败

**问题：** 构建镜像时出错

**解决：**
```bash
# 清理Docker缓存
docker system prune -a

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

## 📄 License

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请提交GitHub Issue。

---

**Powered by FastAPI + Vue 3 + Dify**
