"""Routes for importação de dados."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Empresa, Vida, Cargo
from app.schemas.empresa import EmpresaCreate, EmpresaResponse, VidaCreate, VidaResponse

router = APIRouter()


@router.post("/empresas", response_model=EmpresaResponse)
async def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    """Create a new enterprise."""
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
async def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    """Get enterprise by ID."""
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa


@router.post("/vidas", response_model=VidaResponse)
async def create_vida(vida: VidaCreate, db: Session = Depends(get_db)):
    """Create a new vida (employee record)."""
    db_vida = Vida(**vida.dict())
    db.add(db_vida)
    db.commit()
    db.refresh(db_vida)
    return db_vida


@router.get("/vidas/{vida_id}", response_model=VidaResponse)
async def get_vida(vida_id: int, db: Session = Depends(get_db)):
    """Get vida by ID."""
    vida = db.query(Vida).filter(Vida.id == vida_id).first()
    if not vida:
        raise HTTPException(status_code=404, detail="Vida não encontrada")
    return vida
