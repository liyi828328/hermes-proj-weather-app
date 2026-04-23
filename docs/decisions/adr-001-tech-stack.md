# ADR-001: 技术栈选型

- 状态：已决定
- 日期：2026-04-23

## 背景

WEATHER-APP 是一个简单的天气查询应用，前后端分离，后端仅做 API 代理。

## 决策

- 后端：Python + FastAPI
- 前端：原生 HTML/CSS/JS（无框架）
- 测试：pytest
- 静态检查：ruff

## 理由

1. **FastAPI**：自带 async、OpenAPI 文档、Pydantic 校验，API 代理层最优选择
2. **原生前端**：仅 1 个页面 2 个交互，引入 React/Vue 是过度设计
3. **前端由后端 serve**：FastAPI StaticFiles 挂载，一个命令启动全栈，无跨域问题

## 备选方案

- Express.js + React：对此项目过重
- Flask：缺少原生 async 和自动文档

## 后果

- 开发者需要 Python 3.10+ 环境
- 前端无热更新（可手动刷新，对此项目无影响）
