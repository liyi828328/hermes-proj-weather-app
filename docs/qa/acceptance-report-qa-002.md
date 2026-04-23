# 验收报告 — QA-002（回归验证）

- 项目：weather-app
- 任务 ID：qa-002
- 测试日期：2026-04-23
- 测试类型：回归验证（BUG-001 修复后）
- status: passed

## 回归目标

验证 BUG-001（城市搜索对不存在的城市返回502而非200空数组）修复后：
1. 原失败用例 T03/T11/T12 是否通过
2. 城市搜索模块其他用例是否受影响（无回归）
3. 天气查询接口基本功能是否正常（Smoke Test）

## 测试结果

| ID | 测试名称 | 类型 | 输入 | 期望结果 | 实际结果 | 状态 |
|----|----------|------|------|----------|----------|------|
| T03 | 城市搜索-不存在城市 | 回归 | GET /api/cities?q=xyznotacity999 | 200, code=OK, data=[] | 200, code=OK, data=[] | **PASS** ✅ |
| T11 | 边界-超长城市名(500字符) | 回归 | GET /api/cities?q=aaa...500个a | 200, code=OK, data=[] | 200, code=OK, data=[] | **PASS** ✅ |
| T12 | 边界-特殊字符 | 回归 | GET /api/cities?q=<script> | 200, code=OK, data=[] | 200, code=OK, data=[] | **PASS** ✅ |
| T01 | 城市搜索-英文(beijing) | 回归检查 | GET /api/cities?q=beijing | 200, code=OK, data含城市列表 | 符合预期 | PASS |
| T02 | 城市搜索-中文(北京) | 回归检查 | GET /api/cities?q=北京 | 200, code=OK, data含城市列表 | 符合预期 | PASS |
| T04 | 城市搜索-缺少q参数 | 回归检查 | GET /api/cities | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T05 | 城市搜索-q为空字符串 | 回归检查 | GET /api/cities?q= | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T06 | 天气查询-有效城市ID | Smoke | GET /api/weather?location=101010100 | 200, code=OK, data含完整天气字段 | 符合预期 | PASS |
| T07 | 天气查询-缺少location | Smoke | GET /api/weather | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T08 | 天气查询-location为空 | Smoke | GET /api/weather?location= | 400, code=INVALID_PARAM | 符合预期 | PASS |
| T09 | 天气查询-无效location | Smoke | GET /api/weather?location=99999999 | 502, code=UPSTREAM_ERROR | 符合预期 | PASS |
| T10 | Content-Type验证 | 契约 | GET /api/cities?q=beijing | Content-Type含application/json | 符合预期 | PASS |
| T13 | 错误响应包含message字段 | 契约 | GET /api/cities (触发400) | 响应含code和message字段 | 符合预期 | PASS |

## 统计

- 总计：13
- 通过：13
- 失败：0

## 验收标准检查

| 编号 | 验收标准 | 结果 |
|------|----------|------|
| F1 | 输入"北京"或"beijing"能返回正确的城市列表 | PASS |
| F2 | 选择城市后能获取到实时天气数据（温度、天气状况、风向） | PASS |
| F3 | 页面清晰展示温度（°C）、天气描述文字、风向风力信息 | N/A — 前端UI测试未在本轮范围内 |
| F4 | 页面在主流浏览器中正常显示 | N/A — 前端UI测试未在本轮范围内 |

## 契约合规验证

| 检查项 | 结果 |
|--------|------|
| /api/cities 响应格式符合api.yaml | PASS |
| /api/weather 响应格式符合api.yaml | PASS |
| 错误码符合error-codes.md | PASS — 不存在城市现在正确返回200+code=OK+data=[] |
| Content-Type为application/json | PASS |
| 错误响应含code+message字段 | PASS |

## 缺陷汇总

| ID | 严重等级 | 描述 | 状态 |
|----|----------|------|------|
| BUG-001 | P1 | 城市搜索对不存在的城市返回502而非200空数组 | **已修复** ✅ |

无新增缺陷。

## 非功能性需求

| 检查项 | 结果 |
|--------|------|
| API Key不暴露在前端 | PASS — Key配置在后端config.py/环境变量中 |

## 结论

**验收通过**。BUG-001 已修复，原失败用例 T03/T11/T12 全部通过。城市搜索模块和天气查询模块无回归问题，契约合规验证全部通过。
