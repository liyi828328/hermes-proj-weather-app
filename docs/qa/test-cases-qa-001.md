# 测试用例表 — QA-001

| ID | 测试名称 | 类型 | 输入 | 期望结果 | 实际结果 | 状态 |
|----|----------|------|------|----------|----------|------|
| T01 | 城市搜索-英文(beijing) | 功能/契约 | GET /api/cities?q=beijing | 200, code=OK, data含城市列表，每项含id/name/adm1/adm2/country | 符合预期 | PASS |
| T02 | 城市搜索-中文(北京) | 功能/契约 | GET /api/cities?q=北京 | 200, code=OK, data含城市列表 | 符合预期 | PASS |
| T03 | 城市搜索-不存在城市 | 功能/错误码 | GET /api/cities?q=xyznotacity999 | 200, code=OK, data=[] (按error-codes.md CITY_NOT_FOUND规范) | 502, code=UPSTREAM_ERROR | **FAIL** |
| T04 | 城市搜索-缺少q参数 | 错误码 | GET /api/cities | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T05 | 城市搜索-q为空字符串 | 错误码 | GET /api/cities?q= | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T06 | 天气查询-有效城市ID | 功能/契约 | GET /api/weather?location=101010100 | 200, code=OK, data含temp/text/windDir/windScale/humidity/obsTime | 符合预期 | PASS |
| T07 | 天气查询-缺少location | 错误码 | GET /api/weather | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T08 | 天气查询-location为空 | 错误码 | GET /api/weather?location= | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T09 | 天气查询-无效location | 错误码 | GET /api/weather?location=99999999 | 502, code=UPSTREAM_ERROR | 符合预期 | PASS |
| T10 | Content-Type验证 | 契约 | GET /api/cities?q=beijing | Content-Type含application/json | 符合预期 | PASS |
| T11 | 边界-超长城市名(500字符) | 边界 | GET /api/cities?q=aaa...500个a | 200或合理错误 | 502 UPSTREAM_ERROR | **FAIL** (同T03根因) |
| T12 | 边界-特殊字符(<script>) | 边界 | GET /api/cities?q=<script> | 200或合理错误 | 502 UPSTREAM_ERROR | **FAIL** (同T03根因) |
| T13 | 错误响应包含message字段 | 契约 | GET /api/cities (触发400) | 响应含code和message字段 | 符合预期 | PASS |

## 统计

- 总计：13
- 通过：10
- 失败：3（归为1个根因缺陷）
