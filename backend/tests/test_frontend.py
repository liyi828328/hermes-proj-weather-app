"""前端静态文件服务测试"""

import pytest


@pytest.mark.asyncio
async def test_index_html_served(client):
    """访问 / 能返回 index.html"""
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "天气查询" in resp.text


@pytest.mark.asyncio
async def test_style_css_accessible(client):
    """静态资源 /style.css 可访问"""
    resp = await client.get("/style.css")
    assert resp.status_code == 200
    assert "text/css" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_app_js_accessible(client):
    """静态资源 /app.js 可访问"""
    resp = await client.get("/app.js")
    assert resp.status_code == 200
    assert "javascript" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_index_html_has_search_input(client):
    """index.html 包含搜索输入框"""
    resp = await client.get("/")
    assert 'id="search-input"' in resp.text


@pytest.mark.asyncio
async def test_index_html_has_search_button(client):
    """index.html 包含搜索按钮"""
    resp = await client.get("/")
    assert 'id="search-btn"' in resp.text


@pytest.mark.asyncio
async def test_index_html_has_city_list(client):
    """index.html 包含城市列表容器"""
    resp = await client.get("/")
    assert 'id="city-list"' in resp.text


@pytest.mark.asyncio
async def test_index_html_has_weather_card(client):
    """index.html 包含天气卡片区域"""
    resp = await client.get("/")
    assert 'id="weather-card"' in resp.text


@pytest.mark.asyncio
async def test_index_html_has_error_msg(client):
    """index.html 包含错误提示区域"""
    resp = await client.get("/")
    assert 'id="error-msg"' in resp.text


@pytest.mark.asyncio
async def test_app_js_has_search_function(client):
    """app.js 包含 searchCity 函数"""
    resp = await client.get("/app.js")
    assert "searchCity" in resp.text


@pytest.mark.asyncio
async def test_app_js_has_weather_function(client):
    """app.js 包含 getWeather 函数"""
    resp = await client.get("/app.js")
    assert "getWeather" in resp.text


@pytest.mark.asyncio
async def test_style_css_has_card_styles(client):
    """style.css 包含天气卡片样式"""
    resp = await client.get("/style.css")
    assert ".weather-card" in resp.text
