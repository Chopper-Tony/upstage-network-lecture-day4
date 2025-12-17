from typing import List

from app.repository.client.upstage_client import UpstageClient


class EmbeddingService:
    def __init__(self):
        self._client = UpstageClient()

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._client.create_embeddings(texts=texts)
    
    def create_embedding(self, text: str) -> List[float]:
        return self._client.create_embedding(text)