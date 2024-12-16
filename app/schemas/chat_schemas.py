from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    materia: str
    pergunta: str
    
class ChatResponse(BaseModel):
    materia: str
    resposta: str
    links: list[str] = Field(default_factory=list)
    informacoes_uteis: list[str] = Field(default_factory=list)

