# 代码审查报告 — bugfix-001（第 1 轮）

- 日期：2026-04-23
- PR：#5
- 审查员：Reviewer Agent
- 结论：**REQUEST-CHANGES**

## 前置检查清单

| 检查项 | 结果 |
|--------|------|
| PR 与 main 无冲突 | ✅ 通过 |
| 包含测试文件 | ✅ 3 个新增测试用例 |
| 测试全部通过 | ✅ 25/25 passed |
| 覆盖率报告存在 | ✅ docs/reports/coverage-bugfix-001.md |
| 覆盖率 ≥ 85% | ✅ 97% |
| 静态检查通过 | ✅ ruff check: All checks passed |
| PR body 格式完整 | ✅ 包含 issue 关联、根因分析、修复方案、自测结果 |
| 契约变更合规 | ✅ 未修改 docs/contracts/ 下的文件 |

## 安全审查

- SQL 注入：N/A
- XSS：N/A
- 硬编码密钥：未在本 PR diff 中新增（已有问题不在本次范围）
- 不安全反序列化：未发现
- 路径遍历：未发现
- 敏感信息日志：未发现

## 性能审查

- 无新增性能问题
- `HTTPStatusError` 对 "No Such Location" 直接返回不重试 — 正确

## 代码规范审查

- 函数长度：合理
- 命名规范：✅
- 异常处理：✅ 分层清晰（HTTPStatusError → HTTPError → TimeoutException）
- 注释：✅ 中文注释说明了 QWeather 行为

## 重复代码检测

- 无新增重复代码

## 依赖安全审查

- 无新增依赖

## 问题清单

| # | 严重度 | 文件 | 问题 | 状态 |
|---|--------|------|------|------|
| 1 | 🔴 Critical | backend/.coverage | 二进制运行时产物提交到 PR，应加入 .gitignore 并 git rm --cached | 待修复 |
| 2 | ⚠️ Warning | docs/reviews/review-T1-r1.md, docs/tasks/T1.done, docs/tasks/review-T1-r1.done | PR 范围污染：包含前一轮 task/review 产物，不属于本次 bugfix 范围 | 待修复 |
| 3 | 💡 Suggestion | backend/app/services/qweather.py:60 | 非 "No Such Location" 的 HTTP 400 不应重试（客户端错误非瞬时故障），建议直接 raise | 非阻塞 |
| 4 | 💡 Suggestion | backend/app/services/qweather.py:58 | bare `except Exception: pass` 吞掉 JSON 解析异常，建议加 logging.warning | 非阻塞 |

## 改进建议

1. 将 `.coverage` 加入 `.gitignore`，执行 `git rm --cached backend/.coverage` 从版本控制移除
2. 从本 PR 移除不属于 bugfix-001 范围的文件（review-T1-r1.md、T1.done、review-T1-r1.done）
3. 对非瞬时 HTTP 错误（4xx）直接抛出而非进入重试循环
4. 在 JSON 解析失败的 except 分支添加 warning 日志

## 总结

bugfix 代码逻辑正确且测试覆盖全面，准确修复了 #4 描述的问题。但 PR 中包含了不应提交的二进制文件和不属于本次修复范围的产物文件，需要清理后才能 merge。
