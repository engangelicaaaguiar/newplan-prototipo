"""Pydantic validation schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class EmpresaBase(BaseModel):
    """Base schema for Empresa."""

    razao_social: str
    cnpj: str
    endereco: Optional[str] = None


class EmpresaCreate(EmpresaBase):
    """Schema for creating Empresa."""

    pass


class EmpresaResponse(EmpresaBase):
    """Schema for Empresa response."""

    id: int
    criado_em: datetime

    class Config:
        """Config."""

        from_attributes = True


class VidaBase(BaseModel):
    """Base schema for Vida."""

    nome: str
    cpf: str
    email: EmailStr


class VidaCreate(VidaBase):
    """Schema for creating Vida."""

    empresa_id: int
    cargo_id: Optional[int] = None


class VidaResponse(VidaBase):
    """Schema for Vida response."""

    id: int
    empresa_id: int
    criado_em: datetime

    class Config:
        """Config."""

        from_attributes = True


class QuestionarioBase(BaseModel):
    """Base schema for Questionario."""

    tipo: str
    status: str = "pendente"


class QuestionarioResponse(QuestionarioBase):
    """Schema for Questionario response."""

    id: int
    vida_id: int
    criado_em: datetime
    respondido_em: Optional[datetime] = None

    class Config:
        """Config."""

        from_attributes = True


class AnaliseRiscoResponse(BaseModel):
    """Schema for AnaliseRisco response."""

    id: int
    questionario_id: int
    score_psicossocial: float
    nivel_risco: str
    criado_em: datetime

    class Config:
        """Config."""

        from_attributes = True
