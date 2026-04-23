# 代码审查报告 — T1 后端 API（第 1 轮）

- 日期：2026-04-23
- PR：#3
- 审查员：Reviewer Agent
- 结论：**REQUEST-CHANGES**

## 前置检查清单

| 检查项 | 结果 |
|--------|------|
| PR 与 main 无冲突 | ✅ 通过 |
| 包含测试文件 | ✅ 4 个测试文件，22 个测试用例 |
| 测试全部通过 | ✅ 22/22 passed |
| 覆盖率报告存在 | ✅ docs/reports/coverage-T1.md |
| 覆盖率 ≥ 85% | ✅ 98% |
| 静态检查通过 | ✅ ruff check: All checks passed |
| PR body 格式完整 | ✅ 包含 issue 关联、契约声明、测试结果、覆盖率、静态检查 |
| 契约变更合规 | ✅ 未越界修改契约文件 |

## 安全审查

| # | 严重度 | 文件 | 行 | 问题 |
|---|--------|------|----|------|
| 1 | 🔴 Critical | backend/app/config.py | 6 | 硬编码 API 密钥，真实 key 泄露到 Git 历史 |
| 2 | ⚠️ Warning | backend/app/main.py | 14-20 | CORS allow_origins=["*"] + allow_credentials=True 不安全 |

- SQL 注入：N/A（无数据库）
- XSS：N/A（纯 API 服务）
- 不安全反序列化：未发现
- 路径遍历：未发现
- 敏感信息日志：未发现
- 认证授权：N/A（公开 API）

## 性能审查

| # | 严重度 | 文件 | 行 | 问题 |
|---|--------|------|----|------|
| 3 | ⚠️ Warning | backend/app/services/qweather.py | 44 | 每次请求创建新的 AsyncClient，无法复用 TCP 连接 |

- N+1 查询：N/A
- 不必要循环嵌套：未发现
- 资源未关闭：AsyncClient 使用 context manager 正确关闭
- 未分页查询：N/A
- 缓存缺失：可考虑对城市搜索结果缓存（非阻塞建议）
- 内存泄漏：未发现

## 代码规范审查

- 函数过长（>50 行）：未发现
- 类过大（>500 行）：未发现
- 魔法数字：`self.timeout = 10.0`、`self.max_retries = 1` — 可接受，语义清晰
- 命名规范：✅ 符合 Python 规范
- 必要注释：✅ 中文 docstring 覆盖
- 过深嵌套：未发现
- 异常处理：✅ 完整
- 日志：⚠️ 缺少任何 logging 调用（建议在 _request 重试时记录 warning 日志）

## 重复代码检测

| # | 严重度 | 位置 | 问题 |
|---|--------|------|------|
| 4 | 💡 Suggestion | routers/city.py & weather.py | try/except QWeatherTimeoutError/QWeatherError 模式完全重复，可提取为公共处理 |

## 依赖安全审查

| # | 严重度 | 文件 | 行 | 问题 |
|---|--------|------|----|------|
| 5 | ⚠️ Warning | requirements.txt | 9 | httpx 重复声明（第 3 行已有 httpx>=0.27.0） |

- 已知漏洞：未发现
- 版本过旧：所有依赖使用较新版本范围
- 不必要重量级依赖：未发现
- License 兼容：均为 MIT/BSD 兼容

## 其他问题

| # | 严重度 | 文件 | 问题 |
|---|--------|------|------|
| 6 | 🔴 Critical | backend/.coverage | 二进制运行时产物提交到仓库，应加入 .gitignore |
| 7 | 💡 Suggestion | backend/app/config.py:7 | qweather_api_host 也不应有硬编码默认值 |

## 改进建议

1. **添加请求日志**：在 `_request` 方法中添加 `logging.warning` 记录重试事件和最终失败，便于线上排查。
2. **使用 httpx 连接池**：将 `AsyncClient` 提升为实例属性或通过 FastAPI lifespan 管理，提升并发性能。
3. **CORS 收紧**：生产环境前务必将 origins 改为具体域名列表。

## 总结

代码整体结构清晰，测试覆盖率 98%，契约合规。但存在 2 个 Critical 问题（API 密钥泄露、二进制文件提交）和 3 个 Warning（CORS 配置、重复依赖、AsyncClient 未复用），必须修复后才能 merge。
