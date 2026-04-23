"""QWeather 服务层单元测试"""
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.qweather import QWeatherError, QWeatherService, QWeatherTimeoutError


@pytest.fixture
def service():
    return QWeatherService()


@pytest.mark.anyio
async def test_search_city_success(service):
    """测试服务层城市搜索成功"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "code": "200",
        "location": [
            {"id": "101010100", "name": "北京", "adm1": "北京", "adm2": "北京", "country": "中国"}
        ],
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        result = await service.search_city("北京")

    assert len(result) == 1
    assert result[0].name == "北京"


@pytest.mark.anyio
async def test_search_city_not_found(service):
    """测试服务层城市搜索404"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"code": "404"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        result = await service.search_city("xyznotexist")

    assert result == []


@pytest.mark.anyio
async def test_search_city_upstream_error(service):
    """测试服务层上游错误码"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"code": "500"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(QWeatherError) as exc_info:
            await service.search_city("北京")
        assert exc_info.value.code == "UPSTREAM_ERROR"


@pytest.mark.anyio
async def test_get_weather_now_success(service):
    """测试服务层天气查询成功"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "code": "200",
        "now": {
            "temp": "23", "text": "晴", "windDir": "西北风",
            "windScale": "3", "humidity": "45", "obsTime": "2026-04-23T15:00+08:00",
        },
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        result = await service.get_weather_now("101010100")

    assert result.temp == "23"
    assert result.text == "晴"


@pytest.mark.anyio
async def test_get_weather_now_upstream_error(service):
    """测试服务层天气查询上游错误"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"code": "500"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(QWeatherError):
            await service.get_weather_now("101010100")


@pytest.mark.anyio
async def test_request_timeout_with_retry(service):
    """测试超时后重试"""
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(QWeatherTimeoutError):
            await service.search_city("北京")

        # Should have retried once (2 total calls)
        assert mock_client.get.call_count == 2


@pytest.mark.anyio
async def test_request_http_error_with_retry(service):
    """测试HTTP错误后重试"""
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("connection refused"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(QWeatherError) as exc_info:
            await service.search_city("北京")
        assert exc_info.value.code == "UPSTREAM_ERROR"
        assert mock_client.get.call_count == 2
