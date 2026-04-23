from unittest.mock import AsyncMock, patch

import pytest

from app.schemas.city import CityItem
from app.services.qweather import QWeatherError, QWeatherTimeoutError


@pytest.mark.anyio
async def test_search_cities_success(client):
    """测试城市搜索成功"""
    mock_cities = [
        CityItem(id="101010100", name="北京", adm1="北京", adm2="北京", country="中国")
    ]
    with patch("app.routers.city.qweather_service.search_city", new_callable=AsyncMock, return_value=mock_cities):
        resp = await client.get("/api/cities", params={"q": "北京"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "OK"
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "北京"


@pytest.mark.anyio
async def test_search_cities_empty(client):
    """测试城市搜索无结果"""
    with patch("app.routers.city.qweather_service.search_city", new_callable=AsyncMock, return_value=[]):
        resp = await client.get("/api/cities", params={"q": "xyznotexist"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "OK"
    assert data["data"] == []


@pytest.mark.anyio
async def test_search_cities_missing_param(client):
    """测试缺少参数"""
    resp = await client.get("/api/cities")
    assert resp.status_code == 400 or resp.status_code == 422


@pytest.mark.anyio
async def test_search_cities_upstream_error(client):
    """测试上游服务错误"""
    with patch(
        "app.routers.city.qweather_service.search_city",
        new_callable=AsyncMock,
        side_effect=QWeatherError("UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试"),
    ):
        resp = await client.get("/api/cities", params={"q": "北京"})
    assert resp.status_code == 502
    assert resp.json()["code"] == "UPSTREAM_ERROR"


@pytest.mark.anyio
async def test_search_cities_timeout(client):
    """测试上游服务超时"""
    with patch(
        "app.routers.city.qweather_service.search_city",
        new_callable=AsyncMock,
        side_effect=QWeatherTimeoutError(),
    ):
        resp = await client.get("/api/cities", params={"q": "北京"})
    assert resp.status_code == 504
    assert resp.json()["code"] == "UPSTREAM_TIMEOUT"


@pytest.mark.anyio
async def test_search_cities_multiple_results(client):
    """测试多个城市结果"""
    mock_cities = [
        CityItem(id="101010100", name="北京", adm1="北京", adm2="北京", country="中国"),
        CityItem(id="101200101", name="北京路", adm1="广东", adm2="广州", country="中国"),
    ]
    with patch("app.routers.city.qweather_service.search_city", new_callable=AsyncMock, return_value=mock_cities):
        resp = await client.get("/api/cities", params={"q": "北京"})
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2
