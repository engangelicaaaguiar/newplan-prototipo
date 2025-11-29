"""Routes for questionários."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Questionario

router = APIRouter()


@router.post("/")
async def create_questionario(vida_id: int, tipo: str, db: Session = Depends(get_db)):
    """Create a new questionnaire."""
    db_questionario = Questionario(vida_id=vida_id, tipo=tipo, status="pendente")
    db.add(db_questionario)
    db.commit()
    db.refresh(db_questionario)
    return db_questionario


@router.get("/{questionario_id}")
async def get_questionario(questionario_id: int, db: Session = Depends(get_db)):
    """Get questionnaire by ID."""
    questionario = db.query(Questionario).filter(Questionario.id == questionario_id).first()
    if not questionario:
        raise HTTPException(status_code=404, detail="Questionário não encontrado")
    return questionario


@router.put("/{questionario_id}/respostas")
async def update_respostas(questionario_id: int, respostas: dict, db: Session = Depends(get_db)):
    """Update questionnaire responses."""
    questionario = db.query(Questionario).filter(Questionario.id == questionario_id).first()
    if not questionario:
        raise HTTPException(status_code=404, detail="Questionário não encontrado")
    
    import json
    from datetime import datetime
    
    questionario.respostas = json.dumps(respostas)
    questionario.status = "respondido"
    questionario.respondido_em = datetime.utcnow()
    db.commit()
    db.refresh(questionario)
    return questionario
