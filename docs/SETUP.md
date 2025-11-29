# Setup - Desenvolvimento Local

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker e Docker Compose
- Git

## Backend Setup

### 1. Ambiente Virtual

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Dependências

```bash
pip install -r requirements.txt
```

### 3. Banco de Dados

Inicie PostgreSQL e Redis com Docker Compose:

```bash
# Do root do projeto
docker-compose up -d
```

Ou manualmente:

```bash
# Terminal 1: PostgreSQL
docker run -d --name postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=saude_mental -p 5432:5432 postgres:15

# Terminal 2: Redis
docker run -d --name redis -p 6379:6379 redis:7
```

### 4. Variáveis de Ambiente

Crie `.env` no diretório `backend/`:

```env
DATABASE_URL=postgresql://postgres:password@localhost/saude_mental
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
SECRET_KEY=your-secret-key-dev-only
DEBUG=True
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### 5. Rodar Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs (Swagger UI)

## Frontend Setup

### 1. Dependências

```bash
cd frontend
npm install
```

### 2. Variáveis de Ambiente

Crie `.env` (frontend root):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Rodar Frontend

```bash
npm run dev
```

Acesse: http://localhost:5173

## Com Docker Compose

Do root do projeto:

```bash
docker-compose up --build
```

Isso inicia:
- Backend (8000)
- Frontend (5173)
- PostgreSQL (5432)
- Redis (6379)

## Testes

### Backend

```bash
cd backend
pytest tests/ -v
# ou com coverage
pytest tests/ --cov=app
```

### Frontend

```bash
cd frontend
npm run lint
npm run type-check
```

## Comandos Úteis

### Migrations (quando models mudam)

```bash
# Criar alembic config (primeira vez)
cd backend
alembic init migrations
```

Veja `ARQUITETURA.md` para visão geral do projeto.
