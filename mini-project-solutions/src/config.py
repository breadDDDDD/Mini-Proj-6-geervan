from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    generator_mode: str = "fake"
    data_dir: str = "./data"
    vector_db_path: str = "./storage/vector_index.json"
    log_path: str = "./logs/app.jsonl"
    top_k: int = 4
    max_context_chars: int = 5000
    idr_per_usd: float = 16200.0
    input_usd_per_1m_tokens: float = 0.15
    output_usd_per_1m_tokens: float = 0.60

    @property
    def data_path(self) -> Path:
        return Path(self.data_dir)

    @property
    def vector_path(self) -> Path:
        return Path(self.vector_db_path)

    @property
    def app_log_path(self) -> Path:
        return Path(self.log_path)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

