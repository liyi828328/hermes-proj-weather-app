from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class WeatherNow(BaseModel):
    """实时天气数据"""
    temp: str
    text: str
    windDir: str
    windScale: str
    humidity: str
    obsTime: str


class WeatherResponse(BaseModel):
    """天气查询响应"""
    code: str = "OK"
    data: Optional[WeatherNow] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    code: str
    message: str
