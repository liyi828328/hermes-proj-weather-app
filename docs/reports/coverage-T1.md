# 覆盖率报告 — T1 后端 API

- 日期：2026-04-23
- 工具：pytest-cov
- 总覆盖率：**98%**

## 模块明细

| 模块 | 语句数 | 未覆盖 | 覆盖率 | 未覆盖行 |
|------|--------|--------|--------|----------|
| app/__init__.py | 0 | 0 | 100% | — |
| app/config.py | 6 | 0 | 100% | — |
| app/main.py | 20 | 2 | 90% | 38, 47（全局异常处理函数体，ASGI测试客户端无法触发） |
| app/routers/__init__.py | 0 | 0 | 100% | — |
| app/routers/city.py | 14 | 0 | 100% | — |
| app/routers/weather.py | 14 | 0 | 100% | — |
| app/schemas/__init__.py | 0 | 0 | 100% | — |
| app/schemas/city.py | 12 | 0 | 100% | — |
| app/schemas/weather.py | 16 | 0 | 100% | — |
| app/services/__init__.py | 0 | 0 | 100% | — |
| app/services/qweather.py | 50 | 0 | 100% | — |
| **TOTAL** | **132** | **2** | **98%** | — |

## 测试统计

- 总测试数：22
- 通过：22
- 失败：0
