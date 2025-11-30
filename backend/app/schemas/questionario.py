from typing import Dict, Optional

from pydantic import BaseModel


class QuestionarioCreate(BaseModel):
    tipo: str
    vida_id: int
    respostas: Optional[Dict] = None


class QuestionarioResponse(BaseModel):
    id: int
    vida_id: int
    tipo: str
    status: str
    respostas: Optional[Dict] = None
    criado_em: str
    respondido_em: Optional[str] = None

    class Config:
        from_attributes = True
