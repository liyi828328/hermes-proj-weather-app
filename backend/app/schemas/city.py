from __future__ import annotations

from typing import List

from pydantic import BaseModel


class CityItem(BaseModel):
    """城市信息"""
    id: str
    name: str
    adm1: str
    adm2: str
    country: str


class CitySearchResponse(BaseModel):
    """城市搜索响应"""
    code: str = "OK"
    data: List[CityItem] = []
