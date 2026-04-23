# 覆盖率报告 — bugfix-001

- 日期：2026-04-23
- 任务：bugfix-001（城市搜索对不存在城市返回502）
- 总覆盖率：97%

## 详细覆盖

| 文件 | 语句数 | 未覆盖 | 覆盖率 | 未覆盖行 |
|------|--------|--------|--------|----------|
| app/__init__.py | 0 | 0 | 100% | — |
| app/config.py | 6 | 0 | 100% | — |
| app/main.py | 20 | 2 | 90% | 38, 47 |
| app/routers/city.py | 14 | 0 | 100% | — |
| app/routers/weather.py | 14 | 0 | 100% | — |
| app/schemas/city.py | 12 | 0 | 100% | — |
| app/schemas/weather.py | 16 | 0 | 100% | — |
| app/services/qweather.py | 60 | 2 | 97% | 58-59 |
| **TOTAL** | **142** | **4** | **97%** | — |

## 新增测试用例

- `test_search_cities_qweather_no_such_location` — 端到端验证 HTTP 400 No Such Location 返回 200 + 空数组
- `test_search_city_service_no_such_location` — 服务层单元测试验证返回空列表
- `test_search_city_service_http_400_other_error` — 验证非 No Such Location 的 400 仍正确抛出 QWeatherError
