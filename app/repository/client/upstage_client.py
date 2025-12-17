from typing import List
from openai import OpenAI

from app.core.settings import settings


class UpstageClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.upstage.api_key,
            base_url=settings.upstage.base_url
        )

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                model=settings.upstage.embedding_model,
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            raise RuntimeError(f"Failed to create embeddings: {str(e)}")

    def create_embedding(self, text: str) -> List[float]:
        return self.create_embeddings([text])[0]

    def create_chat_completion(self, messages: list, temperature: float = 0.3, max_tokens: int = 500) -> str:
        try:
            response = self.client.chat.completions.create(
                model=settings.upstage.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to create chat completion: {str(e)}")