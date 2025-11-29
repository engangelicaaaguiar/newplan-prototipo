"""SQLAlchemy models for the application."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Empresa(Base):
    """Enterprise/company model."""

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(255), unique=True, index=True)
    cnpj = Column(String(20), unique=True, index=True)
    endereco = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow)

    cargos = relationship("Cargo", back_populates="empresa")
    vidas = relationship("Vida", back_populates="empresa")


class Cargo(Base):
    """Job position model."""

    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    descricao = Column(String(255))
    departamento = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa = relationship("Empresa", back_populates="cargos")
    vidas = relationship("Vida", back_populates="cargo")


class Vida(Base):
    """Employee/life model."""

    __tablename__ = "vidas"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    cargo_id = Column(Integer, ForeignKey("cargos.id"))
    nome = Column(String(255), index=True)
    cpf = Column(String(20), unique=True, index=True)
    email = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa = relationship("Empresa", back_populates="vidas")
    cargo = relationship("Cargo", back_populates="vidas")
    questionarios = relationship("Questionario", back_populates="vida")


class Questionario(Base):
    """Questionnaire model (Ergos/NR1)."""

    __tablename__ = "questionarios"

    id = Column(Integer, primary_key=True, index=True)
    vida_id = Column(Integer, ForeignKey("vidas.id"), nullable=False)
    tipo = Column(String(50))  # e.g., "ERGOS", "NR17"
    status = Column(String(50), default="pendente")  # pendente, respondido, analisado
    respostas = Column(Text)  # JSON string with answers
    criado_em = Column(DateTime, default=datetime.utcnow)
    respondido_em = Column(DateTime, nullable=True)

    vida = relationship("Vida", back_populates="questionarios")
    analises = relationship("AnaliseRisco", back_populates="questionario")


class AnaliseRisco(Base):
    """Risk analysis model."""

    __tablename__ = "analises_risco"

    id = Column(Integer, primary_key=True, index=True)
    questionario_id = Column(Integer, ForeignKey("questionarios.id"), nullable=False)
    score_psicossocial = Column(Float)
    nivel_risco = Column(String(50))  # baixo, medio, alto, critico
    recomendacoes = Column(Text)  # Recommendations in JSON
    criado_em = Column(DateTime, default=datetime.utcnow)

    questionario = relationship("Questionario", back_populates="analises")
