# 覆盖率报告 — T2: 前端开发

- 日期：2026-04-23
- 任务 ID：T2
- 测试命令：`python3 -m pytest tests/ --cov=app --cov-report=term-missing`

## 覆盖率结果

| 文件 | 语句数 | 未覆盖 | 覆盖率 | 未覆盖行 |
|------|--------|--------|--------|----------|
| app/__init__.py | 0 | 0 | 100% | — |
| app/config.py | 6 | 0 | 100% | — |
| app/main.py | 20 | 1 | 95% | 38 |
| app/routers/__init__.py | 0 | 0 | 100% | — |
| app/routers/city.py | 14 | 0 | 100% | — |
| app/routers/weather.py | 14 | 0 | 100% | — |
| app/schemas/__init__.py | 0 | 0 | 100% | — |
| app/schemas/city.py | 12 | 0 | 100% | — |
| app/schemas/weather.py | 16 | 0 | 100% | — |
| app/services/__init__.py | 0 | 0 | 100% | — |
| app/services/qweather.py | 64 | 2 | 97% | 61-62 |
| **TOTAL** | **146** | **3** | **98%** | — |

## 测试总数

- 总计：36 个测试全部通过
- 前端相关测试：11 个（test_frontend.py）
