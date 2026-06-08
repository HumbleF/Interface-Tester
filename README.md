# ProtoTester 接口测试工具

棋牌手游服务端接口调试工具，用于绕过游戏客户端直接调用游戏服务端 HTTP API。

## 功能

- **接口调试** — 自由填写 Service/Method，向游戏服务端发送 POST 请求
- **并发测试** — 多用户同时发送请求，验证并发场景
- **模拟充值** — 两步流程（RechargeCreate + RechargeDelivery）模拟内购
- **任务推进** — 调用 TaskSys/TestCmd 批量完成或清除任务数据

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + TypeScript + Element Plus + Pinia + Vite |
| 后端 | Python FastAPI + aiohttp |
| 通信 | 前端 Vite 代理 → 后端 → 游戏服务端 |

## 快速启动

### 环境要求

- Node.js 18+
- Python 3.10+

### 后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

启动后访问 `http://localhost:3000`，局域网内可通过 `http://192.168.14.14:3000` 访问。

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── api/          # 路由（request, mock, config）
│   │   ├── core/         # HTTP 客户端
│   │   ├── models/       # Pydantic 数据模型
│   │   ├── config.py     # 应用配置
│   │   └── main.py       # FastAPI 入口
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/          # Axios 请求封装
│   │   ├── components/   # 通用组件（ResponsePanel）
│   │   ├── layouts/      # 主布局
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── views/        # 页面视图
│   │   └── router/       # 路由配置
│   └── vite.config.ts
└── docs/
```

## 游戏服务端约定

- 请求方式：`POST /{Service}/{Method}`
- 请求头：`numid`（用户 ID）、`areaid`（区服 ID）
- 响应格式：`{"code": 0, "data": {...}}`，`code=0` 表示业务成功
