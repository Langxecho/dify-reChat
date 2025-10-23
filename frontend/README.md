# Dify ReChat - 前端

基于Vue 3 + TypeScript的现代化前端应用。

## 技术栈

- Vue 3 (Composition API)
- TypeScript
- Vite
- Vue Router
- Pinia
- Tailwind CSS
- Axios
- Marked (Markdown渲染)

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 项目结构

```
src/
├── api/              # API调用
│   ├── client.ts     # Axios配置
│   ├── auth.ts       # 认证API
│   └── chat.ts       # 聊天API
├── components/       # Vue组件
│   ├── auth/         # 认证相关
│   ├── chat/         # 聊天相关
│   └── common/       # 通用组件
├── router/           # 路由配置
│   └── index.ts
├── stores/           # Pinia状态管理
│   ├── auth.ts       # 认证状态
│   └── chat.ts       # 聊天状态
├── views/            # 页面组件
│   ├── Login.vue     # 登录页
│   ├── Register.vue  # 注册页
│   ├── Chat.vue      # 聊天页
│   └── Admin.vue     # 管理页
├── App.vue
├── main.ts
└── style.css
```

## 功能说明

### 认证系统

- 登录/注册
- JWT Token管理
- 路由守卫
- 自动登出（Token过期）

### 聊天功能

- 实时流式对话（SSE）
- Markdown渲染
- 对话历史
- 对话管理（重命名、删除）

### 状态管理

使用Pinia管理全局状态：
- `authStore`: 用户认证状态
- `chatStore`: 聊天和对话状态

## 环境配置

开发环境会自动代理API请求到 `http://localhost:8000`

配置文件：`vite.config.ts`

```typescript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## 部署

### Docker部署

使用项目根目录的 `docker-compose.yml` 一键部署。

### 手动部署

1. 构建：
```bash
npm run build
```

2. 将 `dist/` 目录部署到Web服务器（Nginx、Apache等）

3. 配置Nginx反向代理（参考 `nginx.conf`）
