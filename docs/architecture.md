# WEATHER-APP — 技术架构文档

- status: approved
- 项目代号：WEATHER-APP
- 日期：2026-04-23
- 架构师：Architect Agent

## 1. 系统概述

前后端分离的天气查询 Web 应用。后端作为 API 代理层，隐藏第三方 API Key；前端提供简洁的查询与展示界面。

## 2. 技术栈选型

| 层 | 技术 | 版本 | 选型理由 |
|----|------|------|----------|
| 后端 | Python + FastAPI | Python 3.10+, FastAPI 0.100+ | 轻量、异步友好、自带 OpenAPI 文档生成，适合 API 代理层 |
| HTTP 客户端 | httpx | 0.27+ | 原生 async 支持，与 FastAPI 配合天然 |
| 前端 | 原生 HTML + CSS + JavaScript | ES6+ | 项目简单，无需框架；减少构建依赖，本地直接打开即可 |
| 包管理 | pip + requirements.txt | — | 最简方案，无需额外工具链 |
| 测试 | pytest + pytest-asyncio + pytest-cov | — | FastAPI 标准测试方案 |
| 静态检查 | ruff | — | 快速，规则全面，替代 flake8+isort+black |

**不使用前端框架的理由**：项目仅 2 个页面交互（搜索 + 展示），原生 JS 足够，避免 Node.js 构建链路的复杂度。

## 3. 系统架构

```
┌──────────────┐     HTTP      ┌──────────────┐    HTTPS     ┌──────────────┐
│              │  ──────────►  │              │  ─────────►  │              │
│   Browser    │  JSON resp    │  FastAPI     │  JSON resp   │  QWeather    │
│  (静态前端)   │  ◄──────────  │  Backend     │  ◄─────────  │  API         │
│              │               │  :8000       │              │              │
└──────────────┘               └──────────────┘              └──────────────┘
```

- 浏览器直接请求后端 API（同源或 CORS）
- 后端代理转发请求到 QWeather，注入 API Key
- 前端为纯静态文件，由后端 serve（FastAPI StaticFiles）

## 4. 目录结构

```
weather-app/
├── docs/                       # 文档
│   ├── prd.md
│   ├── architecture.md
│   ├── contracts/
│   │   ├── api.yaml            # OpenAPI 契约
│   │   └── error-codes.md      # 错误码规范
│   ├── decisions/
│   │   └── adr-001-tech-stack.md
│   ├── tasks/
│   └── reports/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI 入口，挂载路由 + 静态文件
│   │   ├── config.py           # 配置管理（API Key, Host 等）
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── city.py         # 城市搜索路由
│   │   │   └── weather.py      # 天气查询路由
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── qweather.py     # QWeather API 调用封装
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── city.py         # 城市相关 Pydantic 模型
│   │       └── weather.py      # 天气相关 Pydantic 模型
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_city.py
│   │   └── test_weather.py
│   ├── requirements.txt
│   └── .env.example            # 环境变量示例
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── README.md
└── STATUS.md
```

## 5. 模块设计

### 5.1 后端模块

#### config.py
- 从环境变量读取 `QWEATHER_API_KEY` 和 `QWEATHER_API_HOST`
- 提供默认值用于开发环境
- 使用 pydantic-settings 的 BaseSettings

#### services/qweather.py
- `search_city(location: str) -> list[CityItem]`：调用 QWeather 城市查询
- `get_weather_now(location_id: str) -> WeatherNow`：调用实时天气接口
- 使用 httpx.AsyncClient，带超时（10s）和重试（1 次）
- 统一处理 QWeather 返回的 code 字段，非 "200" 时映射为内部错误码

#### routers/city.py
- `GET /api/cities?q={城市名}` → 返回城市列表

#### routers/weather.py
- `GET /api/weather?location={城市ID}` → 返回实时天气

#### main.py
- 注册路由
- 挂载 `frontend/` 目录为静态文件（`/` 路径）
- 配置 CORS（开发环境允许 `*`）

### 5.2 前端模块

#### index.html
- 搜索框 + 搜索按钮
- 城市下拉列表（搜索结果）
- 天气信息卡片区域

#### app.js
- `searchCity(query)`：调用 `/api/cities?q=xxx`
- `getWeather(locationId)`：调用 `/api/weather?location=xxx`
- DOM 操作渲染结果
- 错误提示处理

#### style.css
- 居中布局，卡片式设计
- 清爽配色（蓝白色调）

## 6. 关键设计决策

1. **API Key 安全**：Key 仅存在于后端环境变量中，前端不可见
2. **无数据库**：PRD 明确不做持久化，不引入数据库
3. **前端由后端 serve**：避免跨域问题，简化本地运行（只启动一个服务）
4. **统一错误响应格式**：所有 API 错误返回 `{"code": "xxx", "message": "xxx"}` 格式

## 7. 非功能性设计

- **超时**：后端请求 QWeather 超时 10 秒
- **错误处理**：QWeather 不可用时返回友好错误信息
- **CORS**：开发环境宽松配置，无安全风险（本地运行）

## 8. 待澄清事项

无。PRD 需求明确，边界清晰。

## 9. 任务拆解建议

| 任务 ID | 任务 | 依赖 | 预估 |
|---------|------|------|------|
| T1 | 后端：项目脚手架 + 配置 + QWeather 服务层 | 无 | 小 |
| T2 | 后端：城市搜索 API + 天气查询 API | T1 | 小 |
| T3 | 前端：页面 + 交互逻辑 | T2 | 小 |

注：T1 和 T2 可合并为一个任务（后端整体），因为代码量小且强耦合。建议实际拆为 2 个任务：后端（T1+T2 合并）和前端（T3）。
