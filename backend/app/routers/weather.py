from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.schemas.weather import WeatherResponse
from app.services.qweather import QWeatherError, QWeatherTimeoutError, qweather_service

router = APIRouter()


@router.get("/api/weather")
async def get_weather(location: str = Query(..., min_length=1, description="城市ID")):
    """实时天气查询接口"""
    try:
        weather = await qweather_service.get_weather_now(location)
        return WeatherResponse(code="OK", data=weather)
    except QWeatherTimeoutError:
        return JSONResponse(
            status_code=504,
            content={"code": "UPSTREAM_TIMEOUT", "message": "天气服务请求超时，请稍后重试"},
        )
    except QWeatherError:
        return JSONResponse(
            status_code=502,
            content={"code": "UPSTREAM_ERROR", "message": "天气服务暂时不可用，请稍后重试"},
        )
