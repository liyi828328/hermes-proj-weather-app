from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.schemas.city import CityItem
from app.services.qweather import QWeatherError, QWeatherService, QWeatherTimeoutError


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


@pytest.mark.anyio
async def test_search_cities_qweather_no_such_location(client):
    """测试 QWeather 返回 HTTP 400 No Such Location 时返回空数组（BUG-001 修复验证）"""
    # 模拟 QWeather 对无效城市名返回 HTTP 400 + No Such Location
    mock_response = httpx.Response(
        status_code=400,
        json={"error": {"status": 400, "title": "No Such Location"}},
        request=httpx.Request("GET", "https://example.com/geo/v2/city/lookup"),
    )
    http_error = httpx.HTTPStatusError(
        "Bad Request", request=mock_response.request, response=mock_response
    )
    with patch(
        "app.services.qweather.httpx.AsyncClient"
    ) as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_response.raise_for_status = lambda: (_ for _ in ()).throw(http_error)  # noqa: E501
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        resp = await client.get("/api/cities", params={"q": "xyznotacity999"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == "OK"
    assert data["data"] == []


@pytest.mark.anyio
async def test_search_city_service_no_such_location():
    """测试 QWeatherService.search_city 对 No Such Location 返回空列表"""
    service = QWeatherService()
    mock_response = httpx.Response(
        status_code=400,
        json={"error": {"status": 400, "title": "No Such Location"}},
        request=httpx.Request("GET", "https://example.com/geo/v2/city/lookup"),
    )
    http_error = httpx.HTTPStatusError(
        "Bad Request", request=mock_response.request, response=mock_response
    )

    def raise_for_status():
        raise http_error

    mock_response.raise_for_status = raise_for_status

    with patch("app.services.qweather.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        result = await service.search_city("xyznotacity999")
    assert result == []


@pytest.mark.anyio
async def test_search_city_service_http_400_other_error():
    """测试 QWeatherService 对非 No Such Location 的 HTTP 400 仍抛出 QWeatherError"""
    service = QWeatherService()
    mock_response = httpx.Response(
        status_code=400,
        json={"error": {"status": 400, "title": "Invalid Parameter"}},
        request=httpx.Request("GET", "https://example.com/geo/v2/city/lookup"),
    )
    http_error = httpx.HTTPStatusError(
        "Bad Request", request=mock_response.request, response=mock_response
    )

    def raise_for_status():
        raise http_error

    mock_response.raise_for_status = raise_for_status

    with patch("app.services.qweather.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(QWeatherError) as exc_info:
            await service.search_city("test")
        assert exc_info.value.code == "UPSTREAM_ERROR"
