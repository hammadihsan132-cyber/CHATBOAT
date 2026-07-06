from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse
from services.gemini_service import get_chat_response
from google.genai.errors import ServerError

router = APIRouter()   # ← this line must exist before any @router.post(...)

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    try:
        answer = get_chat_response(messages)
    except ServerError:
        raise HTTPException(status_code=503, detail="Gemini is currently overloaded, please try again shortly.")
    return ChatResponse(response=answer)