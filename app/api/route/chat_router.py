from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse

from app.deps import get_chat_service
from app.models.schemas.chat import ChatRequest
from app.service.chat_service import ChatService


chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("")
def chat(message: ChatRequest,
               chat_service: ChatService = Depends(get_chat_service)):
    return chat_service.upstage_chat(message)


