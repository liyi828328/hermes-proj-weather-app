from __future__ import annotations

import logging
from typing import List, Optional

import httpx

from app.config import settings
from app.schemas.city import CityItem
from app.schemas.weather import WeatherNow

logger = logging.getLogger(__name__)


class QWeatherError(Exception):
    """QWeather API 错误"""
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class QWeatherTimeoutError(QWeatherError):
    """QWeather API 超时"""
    def __init__(self):
        super().__init__("UPSTREAM_TIMEOUT", "天气服务请求超时，请稍后重试")


class QWeatherService:
    """和风天气 API 服务封装"""

    def __init__(self):
        self.base_url = f"https://{settings.qweather_api_host}"
        self.headers = {"X-QW-Api-Key": settings.qweather_api_key}
        self.timeout = 10.0
        self.max_retries = 1

    async def _request(self, path: str, params: dict) -> dict:
        """发送请求，带超时和重试"""
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    base_url=self.base_url,
                    headers=self.headers,
                    timeout=self.timeout,
                ) as client:
                    resp = await client.get(path, params=params)
                    resp.raise_for_status()
                    return resp.json()
            except httpx.TimeoutException:
                last_exc = QWeatherTimeoutError()
            except httpx.HTTPStatusError as exc:
                # QWeather 对无效城市名返回 HTTP 400 + "No Such Location"
                if exc.response.status_code == 400:
                    try:
                        body = exc.response.json()
                        error_title = body.get("error", {}).get("title", "")
                        if "No Such Location" in error_title:
                            return {"code": "404", "location": []}
                    except Exception:
                        logger.warning(
                            "解析上游 400 响应 JSON 失败: path=%s status=%s",
                            path, exc.response.status_code,
                        )
                # 4xx 客户端错误不应重试，直接抛出
                if 400 <= exc.response.status_code < 500:
                    raise QWeatherError(
                        "UPSTREAM_ERROR",
                        f"上游返回客户端错误 {exc.response.status_code}",
                    )
                last_exc = QWeatherError(
                    "UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试"
                )
            except httpx.HTTPError:
                last_exc = QWeatherError(
                    "UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试"
                )
        raise last_exc  # type: ignore[misc]

    async def search_city(self, location: str) -> List[CityItem]:
        """搜索城市"""
        data = await self._request("/geo/v2/city/lookup", {"location": location})
        code = data.get("code", "")
        if code != "200":
            if code == "404":
                return []
            raise QWeatherError("UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试")
        locations = data.get("location", [])
        return [
            CityItem(
                id=loc["id"],
                name=loc["name"],
                adm1=loc["adm1"],
                adm2=loc["adm2"],
                country=loc["country"],
            )
            for loc in locations
        ]

    async def get_weather_now(self, location_id: str) -> WeatherNow:
        """获取实时天气"""
        data = await self._request("/v7/weather/now", {"location": location_id})
        code = data.get("code", "")
        if code != "200":
            raise QWeatherError("UPSTREAM_ERROR", "天气服务暂时不可用，请稍后重试")
        now = data["now"]
        return WeatherNow(
            temp=now["temp"],
            text=now["text"],
            windDir=now["windDir"],
            windScale=now["windScale"],
            humidity=now["humidity"],
            obsTime=now["obsTime"],
        )


qweather_service = QWeatherService()
