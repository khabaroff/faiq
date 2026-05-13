from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_api_version: str = "2024-12-01-preview"
    azure_deployment_smart: str
    azure_deployment_fast: str | None = None
    langfuse_enabled: bool = False
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_host: str = "https://cloud.langfuse.com"
    github_token: str | None = None
    jina_api_key: str | None = None
    telegram_bot_token: str | None = None
    telegram_channel_id: str | None = None
    inbox_dir: Path = _ROOT / "inbox"
    logs_dir: Path = _ROOT / "logs"
    prompts_dir: Path = _ROOT / "prompts"
    ocr_model: str = "gpt-5.4"

    model_config = SettingsConfigDict(env_file=".env")
