import logging
import chromadb
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

logger = logging.getLogger(__name__)


# MySQL Database Configuration
engine = create_engine(
    settings.database.database_url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency로 사용할 데이터베이스 세션을 생성하고 반환.
    요청이 끝나면 자동으로 세션을 닫음.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ChromaDB Configuration
class ChromaDBConnection:
    _instance: Optional['ChromaDBConnection'] = None
    _client: Optional[chromadb.HttpClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = chromadb.HttpClient(
                host=settings.chromadb.host, 
                port=settings.chromadb.port
            )

    @property
    def client(self) -> chromadb.HttpClient:
        return self._client

    def get_collection(self, collection_name: str = None):
        name = collection_name or settings.chromadb.collection_name
        return self._client.get_or_create_collection(
            name=name,
            metadata={"description": "Upstage Solar2 embeddings collection"}
        )


def get_chroma_client() -> chromadb.HttpClient:
    """
    FastAPI dependency로 사용할 ChromaDB 클라이언트를 생성하고 반환.
    요청별로 새로운 클라이언트 인스턴스를 제공.
    """
    try:
        client = chromadb.HttpClient(
            host=settings.chromadb.host, 
            port=settings.chromadb.port
        )
        yield client
    except Exception as e:
        logger.error(f"Failed to connect to ChromaDB: {e}")
        raise
    finally:
        # ChromaDB HttpClient는 자동으로 연결을 관리하므로 명시적 해제 불필요
        pass


def get_chroma_collection(collection_name: str = None):
    """ChromaDB 컬렉션을 반환하는 의존성 함수"""
    connection = ChromaDBConnection()
    return connection.get_collection(collection_name)