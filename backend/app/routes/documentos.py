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



@router.get("/{analise_id}/pdf/status")
async def status_pdf(analise_id: int, db: Session = Depends(get_db)):
    """Return a simple status for PDF generation.

    This is a lightweight endpoint that can be extended to return progress
    or hook into a background task store (Redis, DB) in the future.
    """
    analise = db.query(AnaliseRisco).filter(AnaliseRisco.id == analise_id).first()
    if not analise:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    # Placeholder: in a real system we'd consult a task queue or storage
    return {"analise_id": analise_id, "status": "queued"}


@router.get("/{analise_id}/download")
async def download_pdf(analise_id: int, db: Session = Depends(get_db)):
    """Download generated PDF."""
    # TODO: Implement PDF download
    return {"message": "PDF download not yet implemented"}
