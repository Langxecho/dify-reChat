# 开发环境启动指南

## 📋 前置准备

### 1. 确保MySQL正在运行
```bash
# 检查MySQL服务状态
# Windows: 在"服务"中查看MySQL服务
# 或者命令行测试连接
mysql -u root -p
```

### 2. 确保安装了Python和Node.js
```bash
# 检查Python版本（需要3.10+）
python --version

# 检查Node.js版本（需要18+）
node --version
npm --version
```

---

## 🗄️ 步骤1: 初始化数据库

### 方法1: 使用SQL文件（推荐）

```bash
# 导入SQL文件创建数据库和表
mysql -u root -p < database_init.sql

# 输入MySQL密码后，等待执行完成
# 你会看到创建的表列表和"Database initialization completed successfully!"
```

### 方法2: 手动创建

```bash
# 登录MySQL
mysql -u root -p

# 执行以下SQL
CREATE DATABASE dify_rechat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dify_rechat;
exit;
```

---

## 🔧 步骤2: 配置后端环境变量

### 编辑 `backend/.env` 文件

**重要：修改数据库密码**

打开 `backend/.env` 文件，修改第2行的数据库密码：

```env
# 将 123456 改成你的MySQL root密码
DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/dify_rechat?charset=utf8mb4
```

**示例：**
```env
# 如果你的MySQL root密码是 mypassword
DATABASE_URL=mysql+pymysql://root:mypassword@localhost:3306/dify_rechat?charset=utf8mb4
```

---

## 🚀 步骤3: 启动后端

### 完整启动步骤

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（首次运行）
python -m venv venv

# 3. 激活虚拟环境
# Windows PowerShell/CMD:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# 激活成功后，提示符前会显示 (venv)

# 4. 安装依赖（首次运行或依赖更新后）
pip install -r requirements.txt

# 5. 测试数据库连接（可选但推荐）
python test_connection.py

# 6. 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 启动参数说明

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `app.main:app` - FastAPI应用位置（app目录下的main.py中的app对象）
- `--reload` - 代码修改后自动重启（仅开发环境）
- `--host 0.0.0.0` - 允许外部访问（可改为 127.0.0.1 仅本地）
- `--port 8000` - 端口号

### 简化启动（虚拟环境已创建）

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 使用批处理脚本启动（Windows）

```bash
# 双击运行
start_backend.bat
```

### 启动成功标志

你会看到类似这样的输出：
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 测试后端

打开浏览器访问：
- API文档: http://localhost:8000/api/docs
- 健康检查: http://localhost:8000/health

---

## 🎨 步骤4: 启动前端（新终端）

```bash
# 1. 打开新的终端窗口，进入前端目录
cd frontend

# 2. 安装依赖（首次运行）
npm install

# 3. 启动开发服务器
npm run dev
```

### 启动成功标志

你会看到：
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## 🌐 步骤5: 访问应用

打开浏览器访问: **http://localhost:5173**

### 首次使用

1. 点击"立即注册"
2. 输入邮箱和密码（至少6位）
3. **第一个注册的用户自动成为管理员**
4. 登录后，点击左下角"管理"进入管理后台
5. 输入Dify API密钥并保存
6. 返回聊天页面，开始对话！

---

## 🔍 故障排除

### 问题1: 数据库连接失败

**错误信息：** `Can't connect to MySQL server`

**解决方案：**
```bash
# 1. 检查MySQL是否运行
mysql -u root -p

# 2. 检查 backend/.env 中的密码是否正确
# 3. 检查数据库是否创建
mysql -u root -p
USE dify_rechat;
SHOW TABLES;
```

### 问题2: 端口被占用

**错误信息：** `Address already in use`

**解决方案：**
```bash
# 后端换端口
uvicorn app.main:app --reload --port 8001

# 前端换端口（编辑 vite.config.ts）
server: {
  port: 5174  # 改成其他端口
}
```

### 问题3: Python虚拟环境激活失败

**Windows PowerShell错误：**
```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决方案：**
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后重新激活
venv\Scripts\activate
```

### 问题4: npm install 失败

**解决方案：**
```bash
# 清理缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install

# 或使用淘宝镜像（国内）
npm config set registry https://registry.npmmirror.com
npm install
```

---

## 📝 开发常用命令

### 后端

```bash
# 启动开发服务器（热更新）
uvicorn app.main:app --reload

# 查看API文档
# 浏览器访问 http://localhost:8000/api/docs

# 测试数据库连接
python -c "from app.core.database import engine; print(engine.connect())"
```

### 前端

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

---

## 📊 开发环境架构

```
浏览器 (http://localhost:5173)
    ↓
Vue前端 (Vite Dev Server)
    ↓ API代理
后端 (http://localhost:8000)
    ↓
MySQL (localhost:3306)
    ↓
dify_rechat数据库
```

---

## ✅ 检查清单

在开始开发前，确保：

- [ ] MySQL服务正在运行
- [ ] 数据库 `dify_rechat` 已创建
- [ ] `backend/.env` 中的数据库密码正确
- [ ] Python虚拟环境已激活
- [ ] 后端依赖已安装
- [ ] 后端服务运行在 http://localhost:8000
- [ ] 前端依赖已安装
- [ ] 前端服务运行在 http://localhost:5173

---

## 🎯 下一步

1. **注册管理员账号**
2. **配置Dify API密钥**
   - 登录 https://dify.ai
   - 创建工作流
   - 获取API密钥
   - 在管理后台配置
3. **开始开发或测试！**

---

**祝开发顺利！** 🚀

如有问题，请查看：
- [完整README](../README.md)
- [项目总结](../PROJECT_SUMMARY.md)
- 或检查代码中的注释
