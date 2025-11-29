"""Routes para geração de documentos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnaliseRisco, Questionario

router = APIRouter()


@router.post("/{analise_id}/pdf")
async def gerar_pdf(analise_id: int, db: Session = Depends(get_db)):
    """Generate PDF document for risk analysis (NR1/NR17)."""
    analise = db.query(AnaliseRisco).filter(AnaliseRisco.id == analise_id).first()
    if not analise:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    
    # TODO: Implement PDF generation using reportlab/python-docx
    return {
        "message": "PDF generation queued",
        "analise_id": analise_id,
        "task_id": "generated-pdf-task-id",
    }


@router.get("/{analise_id}/download")
async def download_pdf(analise_id: int, db: Session = Depends(get_db)):
    """Download generated PDF."""
    # TODO: Implement PDF download
    return {"message": "PDF download not yet implemented"}
