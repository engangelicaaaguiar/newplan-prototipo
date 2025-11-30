# Variáveis de Ambiente — Guia Rápido

## Frontend (Vercel)

Adicione na aba "Environment Variables" do projeto Vercel:

```
VITE_API_URL=https://saude-mental-nr1-backend.onrender.com/api
```

---

## Backend (Render)

Adicione na aba "Environment" do Web Service Render:

### 1. Banco de dados PostgreSQL

Se criou um PostgreSQL no Render, copie a "Internal Database URL":

```
DATABASE_URL=postgresql://user:password@dpg-xxxxx-a.your-region.databases.render.com:5432/dbname
```

Se usar um PostgreSQL externo (ex: AWS RDS), substitua pela URL correspondente.

### 2. Redis

Se criou um Redis no Render, copie a "Redis URL":

```
REDIS_URL=redis://default:password@redis-xxxxx.your-region.redis.render.com:6379
```

Se usar um Redis externo, substitua pela URL correspondente.

### 3. Chave secreta

Gere uma chave aleatória segura:

```bash
# No terminal local, execute:
openssl rand -hex 32
```

Copie o resultado e adicione:

```
SECRET_KEY=<seu-resultado-do-openssl>
```

Exemplo:
```
SECRET_KEY=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6
```

### 4. Python

Para garantir output em tempo real (útil para logs):

```
PYTHONUNBUFFERED=1
```

---

## ✅ Checklist

- [ ] Frontend: `VITE_API_URL` configurado no Vercel
- [ ] Backend: `DATABASE_URL` configurado no Render
- [ ] Backend: `REDIS_URL` configurado no Render
- [ ] Backend: `SECRET_KEY` configurado no Render
- [ ] Backend: `PYTHONUNBUFFERED=1` configurado no Render
- [ ] PostgreSQL criado no Render (ou URL externa adicionada)
- [ ] Redis criado no Render (ou URL externa adicionada)

---

## 🔗 URLs Após Deploy

Após o deploy bem-sucedido:

- **Frontend**: `https://<seu-projeto>.vercel.app`
- **Backend**: `https://<seu-projeto>.onrender.com`
- **Backend Health**: `https://<seu-projeto>.onrender.com/health`
- **Backend Docs**: `https://<seu-projeto>.onrender.com/docs`
