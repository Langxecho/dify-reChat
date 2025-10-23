# 快速开始指南

## 🎯 5分钟快速体验

### 方式1：本地开发（最快）

#### 前置条件
- Python 3.10+
- Node.js 18+
- MySQL已安装并运行

#### 步骤

**1. 克隆项目**
```bash
cd F:\CodeProject\dify-reChat
```

**2. 创建MySQL数据库**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE dify_rechat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

**3. 启动后端**
```bash
cd backend

# 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境
copy .env.example .env
# 编辑 .env，修改数据库密码

# 运行迁移
alembic revision --autogenerate -m "Initial"
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

**4. 启动前端**（新终端）
```bash
cd frontend

# 安装依赖
npm install

# 启动
npm run dev
```

**5. 访问应用**

打开浏览器访问：http://localhost:5173

---

### 方式2：Docker部署（生产环境）

#### 前置条件
- Docker Desktop已安装

#### 步骤

**1. 配置环境变量**
```bash
copy .env.production.example .env
# 编辑 .env，修改密码
```

**2. 启动所有服务**
```bash
docker-compose up -d
```

**3. 访问应用**

打开浏览器访问：http://localhost

---

## 📱 使用流程

### 1. 注册账号
- 访问应用
- 点击"立即注册"
- 输入邮箱和密码（至少6位）
- **第一个注册的用户自动成为管理员**

### 2. 配置Dify API（管理员）
- 登录后点击左下角"管理"
- 输入Dify API密钥
- 点击"保存配置"

**获取Dify API密钥：**
1. 登录 https://dify.ai
2. 创建或打开工作流
3. 点击"API访问"
4. 生成API密钥

### 3. 开始对话
- 返回聊天页面
- 输入消息
- 享受AI对话！

---

## ⚡ 常用命令

### 后端
```bash
# 启动开发服务器
cd backend
uvicorn app.main:app --reload

# 创建数据库迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

### 前端
```bash
# 启动开发服务器
cd frontend
npm run dev

# 构建生产版本
npm run build
```

### Docker
```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔧 故障排除

### 后端无法启动
```bash
# 检查Python版本
python --version  # 需要 3.10+

# 检查数据库连接
mysql -u root -p
```

### 前端无法启动
```bash
# 检查Node版本
node --version  # 需要 18+

# 清除缓存重装
rm -rf node_modules package-lock.json
npm install
```

### Docker问题
```bash
# 清理Docker
docker system prune -a

# 查看容器状态
docker-compose ps

# 查看容器日志
docker-compose logs backend
docker-compose logs frontend
```

---

## 📚 更多文档

- [完整README](README.md)
- [后端文档](backend/README.md)
- [前端文档](frontend/README.md)

---

**祝你使用愉快！** 🎉
