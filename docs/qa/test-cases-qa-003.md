# 测试用例 — qa-003

| ID | 类型 | 描述 | 输入 | 预期结果 | 实际结果 | 状态 |
|----|------|------|------|----------|----------|------|
| TC-01 | API | 城市搜索（中文） | GET /api/cities?q=北京 | code:"OK", data 数组含北京(101010100) | 返回10条结果，首条为北京 101010100 | PASS |
| TC-02 | API | 城市搜索（拼音） | GET /api/cities?q=beijing | code:"OK", data 数组含北京 | 返回10条结果，首条为北京 101010100 | PASS |
| TC-03 | API | 实时天气查询 | GET /api/weather?location=101010100 | code:"OK", data 含 temp/text/windDir/windScale/humidity/obsTime | 返回完整 WeatherNow 对象 | PASS |
| TC-04 | API | 缺少 q 参数 | GET /api/cities | HTTP 400, code:"INVALID_PARAM" | 400 + INVALID_PARAM | PASS |
| TC-05 | API | q 参数为空 | GET /api/cities?q= | HTTP 400, code:"INVALID_PARAM" | 400 + INVALID_PARAM | PASS |
| TC-06 | API | 缺少 location 参数 | GET /api/weather | HTTP 400, code:"INVALID_PARAM" | 400 + INVALID_PARAM | PASS |
| TC-07 | 契约 | CityItem schema | — | id/name/adm1/adm2/country 字段齐全且为 string | 全部符合 | PASS |
| TC-08 | 契约 | WeatherNow schema | — | temp/text/windDir/windScale/humidity/obsTime 字段齐全且为 string | 全部符合 | PASS |
| TC-09 | 契约 | ErrorResponse schema | — | code/message 字段齐全 | 全部符合 | PASS |
| TC-10 | E2E | 页面加载 | 访问 http://localhost:8000/ | 显示标题、输入框、搜索按钮 | 标题"🌤️ 天气查询"、输入框、搜索按钮均存在 | PASS |
| TC-11 | E2E | 城市搜索交互 | 输入"北京"点搜索 | 显示城市列表 | 显示10个城市选项 | PASS |
| TC-12 | E2E | 天气展示 | 点击"北京" | 显示温度°C、天气描述、风向、风力 | 显示 23°C 晴 南风 2级 湿度36% | PASS |
| TC-13 | E2E | UI布局 | 视觉检查 | 布局整洁美观 | 蓝色渐变背景+白色卡片，居中布局，层次清晰 | PASS |
| TC-14 | 安全 | API Key 不暴露 | 检查前端源码 | 无 API Key | 前端无 API Key，通过后端代理 | PASS |
