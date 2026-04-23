# WEATHER-APP — 统一错误码规范

## 响应格式

所有 API 响应统一使用以下格式：

```json
{
  "code": "OK",
  "data": { ... }
}
```

错误时：

```json
{
  "code": "错误码",
  "message": "人类可读描述"
}
```

## 错误码列表

| 错误码 | HTTP Status | 含义 | 触发场景 |
|--------|-------------|------|----------|
| OK | 200 | 成功 | 正常响应 |
| INVALID_PARAM | 400 | 参数错误 | 缺少必填参数或参数格式不合法 |
| CITY_NOT_FOUND | 200 | 未找到匹配城市 | 搜索结果为空（正常情况，data 为空数组） |
| UPSTREAM_ERROR | 502 | 上游服务错误 | QWeather API 返回非 200 状态或 code 非 "200" |
| UPSTREAM_TIMEOUT | 504 | 上游服务超时 | 请求 QWeather 超过 10 秒未响应 |
| INTERNAL_ERROR | 500 | 内部错误 | 未预期的服务端异常 |

## 说明

- `CITY_NOT_FOUND` 不视为错误，HTTP 状态码仍为 200，`data` 返回空数组 `[]`
- 前端根据 `code` 字段判断是否成功，不依赖 HTTP 状态码
- 所有 5xx 错误的 `message` 不暴露内部细节，仅返回用户友好提示
