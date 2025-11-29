"""FastAPI application factory and configuration."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import importacao, questionarios, analise_risco, documentos

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    yield
    # Shutdown
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Portal Saúde Mental NR1 - API de análise psicossocial",
        lifespan=lifespan,
    )

    # CORS Configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(importacao.router, prefix="/api/v1/importacao", tags=["Importação"])
    app.include_router(questionarios.router, prefix="/api/v1/questionarios", tags=["Questionários"])
    app.include_router(analise_risco.router, prefix="/api/v1/analise-risco", tags=["Análise de Risco"])
    app.include_router(documentos.router, prefix="/api/v1/documentos", tags=["Documentos"])

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok", "app": settings.APP_NAME}

    return app


# Create application instance
app = create_app()
