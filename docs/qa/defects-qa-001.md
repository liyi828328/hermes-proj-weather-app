# 缺陷报告 — QA-001

## BUG-001: 城市搜索对不存在的城市返回502而非200空数组

- 严重等级：P1
- 影响功能：F1 城市搜索
- 相关规范：error-codes.md — CITY_NOT_FOUND 应返回 HTTP 200, code=OK, data=[]

### 复现步骤

1. 启动后端服务
2. 发送请求：`GET /api/cities?q=xyznotacity999`
3. 观察返回结果

### 期望行为

```json
{"code": "OK", "data": []}
```

HTTP 状态码：200

### 实际行为

```json
{"code": "UPSTREAM_ERROR", "message": "天气服务暂时不可用，请稍后重试"}
```

HTTP 状态码：502

### 根因分析

`backend/app/services/qweather.py` 第60-63行，`search_city` 方法仅处理了 QWeather 返回 `code == "404"` 的情况。但 QWeather API 对无效城市名返回 HTTP 400 + `{"error": {"status": 400, "title": "No Such Location"}}` 格式，不经过 `code` 字段逻辑，直接被 `httpx.HTTPError` 捕获后抛出 `QWeatherError`，最终返回 502。

需要在 `_request` 或 `search_city` 中识别 QWeather 的 "No Such Location" 错误，将其作为正常的空结果返回。

### 关联测试用例

T03, T11, T12（三个失败用例同一根因）
