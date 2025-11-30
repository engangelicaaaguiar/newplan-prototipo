# Guia de Deploy — Vercel + Render

Este guia descreve como fazer deploy da aplicação em **Vercel** (frontend) e **Render** (backend).

## 📋 Pré-requisitos

- Conta GitHub (já possui)
- Conta Vercel (crie em https://vercel.com)
- Conta Render (crie em https://render.com)
- Variáveis de ambiente geradas (.env — veja seção abaixo)

---

## 🚀 Passo 1: Deploy do Frontend em Vercel

### 1.1 Conecte o repositório ao Vercel

1. Acesse https://vercel.com/new
2. Clique em "Import Git Repository"
3. Procure por `engangelicaaaguiar/newplan-prototipo` e selecione
4. Clique em "Import"

### 1.2 Configure o projeto Vercel

Na tela de configuração:

- **Project Name**: `newplan-prototipo` (ou seu nome preferido)
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (já preenchido automaticamente)
- **Output Directory**: `dist` (já preenchido automaticamente)

### 1.3 Variáveis de ambiente

Ainda na tela de configuração, clique em "Environment Variables" e adicione:

```
VITE_API_URL=https://<seu-backend-url>/api
```

⚠️ **Substitua `<seu-backend-url>`** pela URL do backend no Render (você obterá após criar o serviço no Render).

Por enquanto, pode deixar como `https://localhost:8000` (será atualizado depois).

### 1.4 Deploy

Clique em "Deploy" e aguarde (~3–5 minutos).

Após o deploy, você receberá um URL público como: `https://newplan-prototipo.vercel.app`

---

## 🔧 Passo 2: Deploy do Backend em Render

### 2.1 Conecte o repositório ao Render

1. Acesse https://render.com/dashboard
2. Clique em "New +" → "Web Service"
3. Procure por `engangelicaaaguiar/newplan-prototipo` e selecione
4. Clique em "Connect"

### 2.2 Configure o Web Service

Na tela de configuração:

- **Name**: `saude-mental-nr1-backend` (ou seu nome preferido)
- **Environment**: `Docker`
- **Region**: `São Paulo` (ou sua preferência)
- **Root Directory**: `backend`
- **Dockerfile Path**: `backend/Dockerfile` (padrão, deixe assim)

### 2.3 Variáveis de ambiente

Clique em "Advanced" → "Add Environment Variable" e adicione as seguintes:

```
DATABASE_URL=postgresql://user:password@postgres-render-url:5432/dbname
REDIS_URL=redis://redis-render-url:6379
SECRET_KEY=your-secret-key-here
PYTHONUNBUFFERED=1
```

⚠️ **Valores necessários:**
- Você pode usar **Render PostgreSQL** (managed) — veja próxima seção.
- Redis: use **Render Redis** (managed) ou um Redis externo.
- SECRET_KEY: gere uma chave segura (ex: `openssl rand -hex 32`).

### 2.4 Crie um PostgreSQL no Render (opcional, recomendado)

1. Acesse https://render.com/dashboard
2. Clique em "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `saude-mental-db`
   - **Database**: `saude_mental`
   - **User**: `dbuser`
   - **Region**: mesmo que o Web Service

Após criar, você receberá uma **Internal Database URL** (use em DATABASE_URL).

### 2.5 Deploy

Clique em "Deploy" e aguarde (~5–10 minutos, pois constrói a imagem Docker).

Após o deploy, você receberá um URL como: `https://saude-mental-nr1-backend.onrender.com`

---

## 🔗 Passo 3: Sincronize URLs (Frontend → Backend)

Após o backend ser implantado no Render:

1. Acesse o painel do Vercel
2. Abra as "Environment Variables" do projeto
3. Atualize `VITE_API_URL` com a URL do Render:
   ```
   VITE_API_URL=https://saude-mental-nr1-backend.onrender.com/api
   ```
4. Clique em "Save" e aguarde o redeploy automático do Vercel (~2–3 minutos)

---

## ✅ Validação

Após ambos os deploys:

1. Acesse a URL do frontend (Vercel):
   ```
   https://seu-frontend-url.vercel.app
   ```

2. Verifique se a aplicação carrega sem erros

3. Teste a integração com o backend:
   - Abra o console (F12)
   - Vá para a página de importação ou dashboard
   - Verifique se há requisições ao backend sem erros CORS

4. Teste o endpoint de health:
   ```bash
   curl https://saude-mental-nr1-backend.onrender.com/health
   ```
   Deve responder: `{"status":"ok","app":"Saúde Mental NR1"}`

---

## 🔧 Configurações Adicionais

### CORS no Backend

Se houver erro CORS, o backend já está configurado com `CORSMiddleware` em `backend/app/main.py`. Se precisar ajustar, edite o arquivo:

```python
allow_origins=["https://seu-frontend-url.vercel.app", "http://localhost:3000"]
```

### Logs e Debugging

- **Vercel**: Vá para "Deployments" e clique em cada build para ver logs
- **Render**: Vá para "Logs" na página do serviço

---

## 🚨 Troubleshooting

### Frontend não conecta ao backend

- Verifique a variável `VITE_API_URL` no Vercel
- Confirme que o backend está rodando (teste `/health`)
- Verifique CORS no backend

### Backend falha ao iniciar

- Verifique a variável `DATABASE_URL` (conexão ao Postgres)
- Verifique a variável `REDIS_URL` (conexão ao Redis)
- Veja os logs no Render para erros específicos

### Redeploy manual no Render

Se precisar redeployar sem fazer push:

1. Acesse https://render.com/dashboard
2. Clique no Web Service
3. Clique em "Manual Deploy" → "Clear build cache & deploy"

---

## 📞 Contato / Suporte

Para erros específicos, consulte:
- Documentação Vercel: https://vercel.com/docs
- Documentação Render: https://render.com/docs
- API Backend: `https://seu-backend/docs` (FastAPI Swagger)
