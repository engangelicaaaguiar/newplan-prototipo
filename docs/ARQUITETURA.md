# Arquitetura

## Visão Geral

O Saúde Mental NR1 é uma plataforma de análise psicossocial com automação de questionários Ergos, consolidação de dados e geração de documentos NR1/NR17.

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                 │
│  - Dashboard | Importação | Questionários | Análise      │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────────┐
│                   FastAPI Backend                        │
│  - Rotas API | Serviços | Models SQLAlchemy            │
│  - Celery para tasks assíncronos                        │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
   ┌────▼──┐ ┌───▼──┐ ┌───▼────┐
   │  DB   │ │Redis │ │Storage │
   │  PgSQL│ │Cache │ │(PDFs)  │
   └───────┘ └──────┘ └────────┘
```

## Stack Técnico

### Backend
- **FastAPI**: Framework web assíncrono, validação automática com Pydantic
- **SQLAlchemy**: ORM para persistência de dados
- **PostgreSQL**: Banco de dados relacional
- **Celery**: Fila de tarefas para processamento assíncrono (geração de PDFs, envios)
- **Redis**: Cache e broker de mensagens

### Frontend
- **React 18**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Estilização utilitária
- **Zustand**: State management
- **Vite**: Build tool moderno

### Infraestrutura
- **Docker**: Containerização
- **Docker Compose**: Orquestração local
- **GitHub Actions**: CI/CD

## Estrutura de Pastas

```
backend/
├── app/
│   ├── models/          → SQLAlchemy models (Empresa, Vida, Questionario, etc)
│   ├── schemas/         → Pydantic schemas para validação
│   ├── routes/          → Endpoints da API (/api/v1/...)
│   ├── services/        → Lógica de negócio isolada
│   ├── tasks/           → Celery tasks assíncronos
│   ├── utils/           → Utilidades (tabelas Ergos, validadores)
│   ├── main.py          → Factory e app FastAPI
│   ├── config.py        → Settings/configurações
│   └── database.py      → Configuração SQLAlchemy
├── tests/               → Testes unitários/integração
└── requirements.txt

frontend/
├── src/
│   ├── components/      → React components reutilizáveis
│   ├── pages/           → Página root/layout
│   ├── services/        → Cliente HTTP (axios)
│   ├── store/           → Zustand stores (estado global)
│   ├── App.tsx          → Router principal
│   └── main.tsx         → Entry point
├── public/              → Arquivos estáticos
├── package.json
├── vite.config.ts
└── tsconfig.json

.github/
└── workflows/
    ├── tests.yml        → Testes automatizados (backend + frontend)
    ├── lint.yml         → Verificação de código (black, flake8, eslint)
    └── deploy.yml       → Build e deploy de imagens Docker
```

## Fluxos de Dados Principais

### 1. Importação de Dados
```
CSV/Excel → Backend /api/v1/importacao/empresas
          → SQLAlchemy models (Empresa, Cargo, Vida)
          → Banco de dados
```

### 2. Respondimento de Questionário
```
Frontend /questionarios/:id
       → Backend /api/v1/questionarios/:id/respostas
       → Armazena respostas em JSON
       → Marca como "respondido"
```

### 3. Análise de Risco
```
Backend /api/v1/analise-risco/:questionario_id/calcular
      → Processa respostas com tabelas Ergos
      → Calcula score psicossocial
      → Determina nível de risco (baixo/médio/alto/crítico)
      → Armazena análise
```

### 4. Geração de Documento (NR1/NR17)
```
Backend /api/v1/documentos/:analise_id/pdf
      → Celery task (assíncrono)
      → ReportLab/python-docx gera PDF
      → Armazena em storage
      → Retorna link de download
```

## Padrões de Código

### Backend
- **Dependency Injection**: FastAPI Depends() para injetar DB session
- **Async/Await**: Handlers e serviços assíncronos
- **Type Hints**: Todas as funções tipadas com Python 3.9+
- **Schemas Duplos**: Pydantic (entrada/saída) + SQLAlchemy (DB)

### Frontend
- **Functional Components**: React Hooks (useState, useEffect, etc)
- **Custom Hooks**: Para lógica compartilhada
- **Zustand Stores**: Estado global simples e reativo

## Decisões Arquiteturais

1. **Separação Backend/Frontend**: Facilita deploy independente e permite múltiplos clientes
2. **Celery para PDFs**: Não bloqueia API enquanto gera documentos pesados
3. **PostgreSQL + SQLAlchemy**: ACID compliance para dados sensíveis de saúde
4. **Zustand**: State manager simples vs Redux (menos boilerplate para prototipo)
5. **Docker Compose**: Simples para dev local; escalável para k8s depois

## Segurança

- JWT para autenticação (esquema em desenvolvimento)
- Validação de entrada com Pydantic
- CORS configurável por ambiente
- Secrets em `.env` (não em repo)
- HTTPS recomendado em produção

Veja `SETUP.md` para ambiente de desenvolvimento e `API.md` para endpoints.
