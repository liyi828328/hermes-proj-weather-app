from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，从环境变量读取"""
    qweather_api_key: str = "a5d3a7d4e32c4c7d880025b161cc9f15"
    qweather_api_host: str = "k73wt3h522.re.qweatherapi.com"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
