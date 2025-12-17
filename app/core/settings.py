import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class DatabaseSettings(BaseSettings):
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=3306, env="DB_PORT")
    db_name: str = Field(default="llmagent", env="DB_NAME")
    db_charset: str = Field(default="utf8mb4", env="DB_CHARSET")
    
    # SQLAlchemy 설정
    pool_size: int = Field(default=5, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DB_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="DB_ECHO")

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}"


class ChromaDBSettings(BaseSettings):
    host: str = Field(default="localhost", env="CHROMA_HOST")
    port: int = Field(default=8800, env="CHROMA_PORT")
    collection_name: str = Field(default="upstage_embeddings", env="CHROMA_COLLECTION_NAME")


class UpstageSettings(BaseSettings):
    api_key: str = Field(..., env="UPSTAGE_API_KEY")
    base_url: str = Field(default="https://api.upstage.ai/v1", env="UPSTAGE_BASE_URL")
    embedding_model: str = Field(default="solar-embedding-1-large-query", env="UPSTAGE_EMBEDDING_MODEL")
    chat_model: str = Field(default="solar-1-mini-chat", env="UPSTAGE_CHAT_MODEL")


class AppSettings(BaseSettings):
    app_name: str = Field(default="Upstage Network Project", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    chromadb: ChromaDBSettings = ChromaDBSettings()
    upstage: UpstageSettings = UpstageSettings()
    app: AppSettings = AppSettings()

    class Config:
        env_file = ".env"
        case_sensitive = False


# 전역 설정 인스턴스
settings = Settings()