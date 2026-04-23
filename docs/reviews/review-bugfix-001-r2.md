# 代码审查报告 — bugfix-001 R2（增量审查）

- **项目**: weather-app
- **PR**: #5
- **任务 ID**: review-bugfix-001-r2
- **审查轮次**: R2（增量审查，基于 R1 reject 意见）
- **审查时间**: 2026-04-23
- **结论**: **APPROVE**（附建议）

---

## R1 问题修复验证

| # | 级别 | 问题描述 | R2 状态 | 说明 |
|---|------|----------|---------|------|
| 1 | Critical | `backend/.coverage` 二进制产物不应提交 | ✅ 已修复 | 文件已删除，`.coverage` 和 `htmlcov/` 已加入 `.gitignore` |
| 2 | Warning | PR 包含前一轮 task/review 产物文件 | ⚠️ 未修复 | 仍包含 4 个产物文件（见下方说明） |
| 3 | Suggestion | 4xx 不应重试 | ✅ 已修复 | `400 <= status < 500` 直接 raise，不进入重试循环 |
| 4 | Suggestion | JSON 解析 except 加 warning 日志 | ✅ 已修复 | 使用 `logger.warning()` 记录解析失败详情 |

### Issue #2 详情

以下文件仍在 PR diff 中，属于流程产物而非代码改动：
- `docs/reports/coverage-bugfix-001.md`
- `docs/reviews/review-bugfix-001-r1.md`
- `docs/tasks/bugfix-001.done`
- `docs/tasks/review-bugfix-001-r1.done`

**评估**：由于 Critical 问题已全部修复，此项降为建议级别，不阻塞合入。

---

## 新改动审查

### 代码改动（backend/app/services/qweather.py）

| 维度 | 结果 |
|------|------|
| 正确性 | ✅ HTTPStatusError 处理逻辑正确：400 + "No Such Location" → 返回空结果；其他 4xx → 直接抛异常不重试；5xx → 重试 |
| 安全性 | ✅ 无硬编码凭证、无注入风险 |
| 代码质量 | ✅ logging 模块标准用法，异常分支清晰 |
| 性能 | ✅ 4xx 不重试避免无意义等待 |
| 文档 | ✅ 代码注释说明了 QWeather 的 400 行为 |

### 测试改动（backend/tests/test_city.py）

- 新增 3 个测试用例：
  1. `test_search_cities_qweather_no_such_location` — 端到端验证 HTTP 400 No Such Location 返回空数组
  2. `test_search_city_service_no_such_location` — Service 层单元测试
  3. `test_search_city_service_http_400_other_error` — 非 No Such Location 的 400 正确抛异常
- 全部 25 个测试通过 ✅

### 静态检查

- 无调试代码残留
- 无安全风险模式（password/secret/api_key 等）
- 无合并冲突标记

---

## 最终结论

**APPROVE** — Critical 问题已修复，代码改动质量良好，测试覆盖充分。建议后续清理产物文件（非阻塞）。
