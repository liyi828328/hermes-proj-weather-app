from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.schemas.city import CitySearchResponse
from app.services.qweather import QWeatherError, QWeatherTimeoutError, qweather_service

router = APIRouter()


@router.get("/api/cities")
async def search_cities(q: str = Query(..., min_length=1, description="城市名称")):
    """城市搜索接口"""
    try:
        cities = await qweather_service.search_city(q)
        return CitySearchResponse(code="OK", data=cities)
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
