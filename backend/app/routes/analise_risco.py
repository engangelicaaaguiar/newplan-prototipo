"""Routes for análise de risco."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnaliseRisco, Questionario

router = APIRouter()


@router.post("/{questionario_id}/calcular")
async def calcular_risco(questionario_id: int, db: Session = Depends(get_db)):
    """Calculate risk analysis for a questionnaire."""
    questionario = db.query(Questionario).filter(Questionario.id == questionario_id).first()
    if not questionario:
        raise HTTPException(status_code=404, detail="Questionário não encontrado")
    
    # TODO: Implement risk calculation logic
    score_psicossocial = 50.0  # Placeholder
    nivel_risco = "médio"  # Placeholder
    
    analise = AnaliseRisco(
        questionario_id=questionario_id,
        score_psicossocial=score_psicossocial,
        nivel_risco=nivel_risco,
        recomendacoes="{}",
    )
    db.add(analise)
    db.commit()
    db.refresh(analise)
    return analise


@router.get("/{questionario_id}")
async def get_analise_risco(questionario_id: int, db: Session = Depends(get_db)):
    """Get risk analysis for a questionnaire."""
    analise = (
        db.query(AnaliseRisco)
        .filter(AnaliseRisco.questionario_id == questionario_id)
        .first()
    )
    if not analise:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return analise



@router.get("/{questionario_id}/calcular")
async def consultar_status_analise(questionario_id: int, db: Session = Depends(get_db)):
    """Consult status/result of the risk analysis for a questionnaire.

    This complements the POST route which triggers calculation.
    """
    analise = (
        db.query(AnaliseRisco)
        .filter(AnaliseRisco.questionario_id == questionario_id)
        .first()
    )
    if not analise:
        raise HTTPException(status_code=404, detail="Análise ainda não disponível")
    return analise
