"""main.py 异常处理测试"""
import pytest


@pytest.mark.anyio
async def test_validation_error_returns_400(client):
    """测试验证错误返回400"""
    resp = await client.get("/api/cities", params={"q": ""})
    assert resp.status_code == 400
    data = resp.json()
    assert data["code"] == "INVALID_PARAM"


@pytest.mark.anyio
async def test_validation_error_missing_param(client):
    """测试缺少必填参数返回400"""
    resp = await client.get("/api/cities")
    assert resp.status_code == 400
    assert resp.json()["code"] == "INVALID_PARAM"


@pytest.mark.anyio
async def test_weather_validation_error(client):
    """测试天气接口验证错误"""
    resp = await client.get("/api/weather", params={"location": ""})
    assert resp.status_code == 400
    assert resp.json()["code"] == "INVALID_PARAM"
