from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.weather import WeatherNow
from app.services.qweather import QWeatherError, QWeatherTimeoutError


@pytest.mark.anyio
async def test_get_weather_success(client):
    """测试天气查询成功"""
    mock_weather = WeatherNow(
        temp="23", text="晴", windDir="西北风", windScale="3", humidity="45", obsTime="2026-04-23T15:00+08:00"
    )
    with patch("app.routers.weather.qweather_service.get_weather_now", new_callable=AsyncMock, return_value=mock_weather):
        resp = await client.get("/api/weather", params={"location": "101010100"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "OK"
    assert data["data"]["temp"] == "23"
    assert data["data"]["text"] == "晴"
    assert data["data"]["windDir"] == "西北风"


@pytest.mark.anyio
async def test_get_weather_missing_param(client):
    """测试缺少参数"""
    resp = await client.get("/api/weather")
    assert resp.status_code == 400 or resp.status_code == 422


@pytest.mark.anyio
async def test_get_weather_upstream_error(client):
    """测试上游服务错误"""
    with patch(
        "app.routers.weather.qweather_service.get_weather_now",
        new_callable=AsyncMock,
        side_effect=QWeatherError("UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试"),
    ):
        resp = await client.get("/api/weather", params={"location": "101010100"})
    assert resp.status_code == 502
    assert resp.json()["code"] == "UPSTREAM_ERROR"


@pytest.mark.anyio
async def test_get_weather_timeout(client):
    """测试上游服务超时"""
    with patch(
        "app.routers.weather.qweather_service.get_weather_now",
        new_callable=AsyncMock,
        side_effect=QWeatherTimeoutError(),
    ):
        resp = await client.get("/api/weather", params={"location": "101010100"})
    assert resp.status_code == 504
    assert resp.json()["code"] == "UPSTREAM_TIMEOUT"


@pytest.mark.anyio
async def test_get_weather_all_fields(client):
    """测试天气数据包含所有必填字段"""
    mock_weather = WeatherNow(
        temp="-5", text="暴雪", windDir="东北风", windScale="8", humidity="95", obsTime="2026-01-15T08:00+08:00"
    )
    with patch("app.routers.weather.qweather_service.get_weather_now", new_callable=AsyncMock, return_value=mock_weather):
        resp = await client.get("/api/weather", params={"location": "101010100"})
    data = resp.json()["data"]
    assert all(k in data for k in ["temp", "text", "windDir", "windScale", "humidity", "obsTime"])


@pytest.mark.anyio
async def test_get_weather_response_format(client):
    """测试响应格式符合契约"""
    mock_weather = WeatherNow(
        temp="30", text="多云", windDir="南风", windScale="2", humidity="60", obsTime="2026-07-01T12:00+08:00"
    )
    with patch("app.routers.weather.qweather_service.get_weather_now", new_callable=AsyncMock, return_value=mock_weather):
        resp = await client.get("/api/weather", params={"location": "101010100"})
    data = resp.json()
    assert "code" in data
    assert "data" in data
    assert data["code"] == "OK"
