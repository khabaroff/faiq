from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-12-01-preview"
    azure_deployment_smart: str
    azure_deployment_fast: str | None = None
    github_token: str | None = None
    data_dir: Path = Path("data")
    prompts_dir: Path = Path("guides/prompts")

    model_config = SettingsConfigDict(env_file=".env")
