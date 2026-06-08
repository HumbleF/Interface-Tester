# ProtoTester 前端界面设计

## 概述

为 ProtoTester 后端 API 构建用户友好的中文 Web 界面，支持接口调试（单发/并发）、模拟充值、任务推进和配置管理。

## 技术栈

- Vue 3 (Composition API + `<script setup>`)
- Element Plus (中文 locale)
- Pinia (状态管理)
- Vite (构建工具)
- TypeScript
- Axios (HTTP 客户端)

## 布局

左侧固定导航栏 + 右侧内容区：

```
┌───────────────────────────────────────────────────┐
│  ProtoTester 接口测试工具                 [配置]   │
├──────────┬────────────────────────────────────────┤
│          │                                        │
│ 接口调试  │   请求配置区 + 响应结果区               │
│ 并发测试  │                                        │
│ 模拟充值  │                                        │
│ 任务推进  │                                        │
│ 系统配置  │                                        │
│          │                                        │
└──────────┴────────────────────────────────────────┘
```

## 功能模块

### 1. 接口调试 (DebugView)

单发请求的完整工作流：

- 输入 Service 名称和 Method 名称
- 填写 Headers（numid、areaid 等）
- JSON 编辑器填写请求 Body
- 点击「发送」，展示响应（状态码、耗时、Body JSON 高亮）

### 2. 并发测试 (ConcurrentView)

多用户同时发送：

- 输入 Service/Method
- 输入多个用户 ID（支持批量粘贴）
- 填写通用 areaid 和请求 Body
- 点击「并发发送」，结果列表展示每个用户的响应
- 汇总信息：总耗时、成功数、失败数

### 3. 模拟充值 (MockPurchaseView)

两步充值流程的一键操作：

- 输入 numid、areaid
- 输入 product_id 和 event
- 点击「执行充值」，展示两步流程的结果
- 显示 pre_order_no 和最终成功/失败状态

### 4. 任务推进 (TaskCmdView)

TaskSys/TestCmd 操作：

- 输入 numid、areaid
- 选择 cmd 类型：finish / clear_data
- 输入任务 ID 列表（支持多个）
- 点击「执行」，展示结果

### 5. 系统配置 (ConfigView)

全局配置管理：

- 服务器地址（host + port）
- 默认区服 ID
- 常用用户 ID 列表（增删改）
- 保存/加载配置

## 目录结构

```
E:\Interface_Testing\frontend\
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── config.ts             # 服务器配置状态（全局共享）
│   │   └── history.ts            # 请求历史记录
│   ├── api/
│   │   ├── index.ts              # axios 实例 + 拦截器
│   │   ├── request.ts            # sendSingle / sendConcurrent
│   │   ├── mock.ts               # mockPurchase / taskCmd
│   │   └── config.ts             # loadConfig / saveConfig
│   ├── views/
│   │   ├── DebugView.vue
│   │   ├── ConcurrentView.vue
│   │   ├── MockPurchaseView.vue
│   │   ├── TaskCmdView.vue
│   │   └── ConfigView.vue
│   ├── components/
│   │   ├── RequestForm/
│   │   │   └── RequestForm.vue   # Service/Method/Headers/Body 表单
│   │   ├── ResponsePanel/
│   │   │   └── ResponsePanel.vue # JSON 高亮 + 状态码 + 耗时
│   │   ├── ServerSelector/
│   │   │   └── ServerSelector.vue # 服务器地址选择
│   │   └── UserIdInput/
│   │       └── UserIdInput.vue   # 多用户 ID 输入
│   └── layouts/
│       └── MainLayout.vue
├── index.html
├── vite.config.ts
├── package.json
└── tsconfig.json
```

## 关键设计决策

1. **前后端完全解耦**：`frontend/` 独立目录，通过 Vite devServer proxy 转发 `/api/*` 到后端 `http://localhost:8000`
2. **API 层统一封装**：所有后端调用在 `src/api/` 中封装为函数，View 组件不直接写 URL
3. **配置全局共享**：服务器地址/区服通过 Pinia configStore 管理，各模块自动获取
4. **中文界面**：Element Plus 设置 zhCn locale，所有 UI 文案为中文
5. **组件复用**：ServerSelector、UserIdInput、ResponsePanel 等跨页面复用

## 数据流

```
View 组件
  ↓ 调用
api/ 封装函数（拼接 configStore 中的 server 信息）
  ↓ axios
Vite proxy → 后端 FastAPI (localhost:8000)
  ↓ 响应
View 组件展示结果
```

## 后端 API 对应关系

| 前端模块 | 后端接口 |
|---------|---------|
| 接口调试 | `POST /api/request/send` |
| 并发测试 | `POST /api/request/concurrent` |
| 模拟充值 | `POST /api/mock/purchase` |
| 任务推进 | `POST /api/mock/task-cmd` |
| 系统配置 | `GET /api/config/load` / `POST /api/config/save` |
