from fastapi import APIRouter, HTTPException
from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.gemini_services import GeminiService
router = APIRouter()
gemini_service = GeminiService()

@router.post("/aula", response_model=ChatResponse)
async def aula(request: ChatRequest):
    try:
        response = await gemini_service.generate_response(
            request.materia,
            request.pergunta
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))