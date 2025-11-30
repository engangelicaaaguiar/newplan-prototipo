"""Routes for questionários.

This module was updated to accept a request body for creation (improves DX)
while keeping backward-compatibility with query params.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

import json

from app.database import get_db
from app.models import Questionario
from app.schemas.questionario import QuestionarioCreate

router = APIRouter()


@router.post("/")
async def create_questionario(
    payload: Optional[QuestionarioCreate] = Body(None),
    vida_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Create a new questionnaire.

    Supports two usage patterns for backward compatibility:
    - Query params: `?tipo=NR1&vida_id=123` (existing clients)
    - Body payload: `{ "tipo": "NR1", "vida_id": 123, "respostas": {...} }` (preferred)
    """

    # Determine source of fields (body preferred)
    if payload:
        tipo_val = payload.tipo
        vida_id_val = payload.vida_id
        respostas = payload.respostas
    else:
        tipo_val = tipo
        vida_id_val = vida_id
        respostas = None

    if not tipo_val or not vida_id_val:
        raise HTTPException(
            status_code=422,
            detail=(
                "Missing 'tipo' or 'vida_id'. Provide them in the request body or as query params."
            ),
        )

    db_questionario = Questionario(vida_id=vida_id_val, tipo=tipo_val, status="pendente")
    if respostas is not None:
        db_questionario.respostas = json.dumps(respostas)

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
async def update_respostas(questionario_id: int, respostas: dict = Body(...), db: Session = Depends(get_db)):
    """Update questionnaire responses."""
    questionario = db.query(Questionario).filter(Questionario.id == questionario_id).first()
    if not questionario:
        raise HTTPException(status_code=404, detail="Questionário não encontrado")

    questionario.respostas = json.dumps(respostas)
    questionario.status = "respondido"
    questionario.respondido_em = datetime.utcnow()
    db.commit()
    db.refresh(questionario)
    return questionario
