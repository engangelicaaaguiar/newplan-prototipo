# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticação

Todos os endpoints (exceto `/health`) requerem JWT token no header:

```
Authorization: Bearer <token>
```

## Endpoints

### Health Check

```http
GET /health
```

Resposta:
```json
{
  "status": "ok",
  "app": "Saúde Mental NR1"
}
```

---

## Importação

### Criar Empresa

```http
POST /importacao/empresas
Content-Type: application/json

{
  "razao_social": "Empresa XYZ Ltda",
  "cnpj": "12.345.678/0001-90",
  "endereco": "Rua das Flores, 123 - São Paulo, SP"
}
```

Resposta (201):
```json
{
  "id": 1,
  "razao_social": "Empresa XYZ Ltda",
  "cnpj": "12.345.678/0001-90",
  "endereco": "Rua das Flores, 123 - São Paulo, SP",
  "criado_em": "2024-01-10T10:30:00"
}
```

### Obter Empresa

```http
GET /importacao/empresas/1
```

Resposta (200):
```json
{
  "id": 1,
  "razao_social": "Empresa XYZ Ltda",
  "cnpj": "12.345.678/0001-90",
  "endereco": "...",
  "criado_em": "2024-01-10T10:30:00"
}
```

### Criar Vida (Funcionário)

```http
POST /importacao/vidas
Content-Type: application/json

{
  "empresa_id": 1,
  "cargo_id": 1,
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "email": "joao@example.com"
}
```

Resposta (201):
```json
{
  "id": 1,
  "empresa_id": 1,
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "email": "joao@example.com",
  "criado_em": "2024-01-10T10:35:00"
}
```

---

## Questionários

### Criar Questionário

```http
POST /questionarios/?vida_id=1&tipo=ERGOS
```

Resposta (201):
```json
{
  "id": 1,
  "vida_id": 1,
  "tipo": "ERGOS",
  "status": "pendente",
  "criado_em": "2024-01-10T10:40:00",
  "respondido_em": null
}
```

### Obter Questionário

```http
GET /questionarios/1
```

Resposta (200):
```json
{
  "id": 1,
  "vida_id": 1,
  "tipo": "ERGOS",
  "status": "pendente",
  "criado_em": "2024-01-10T10:40:00",
  "respondido_em": null
}
```

### Atualizar Respostas

```http
PUT /questionarios/1/respostas
Content-Type: application/json

{
  "q1": 3,
  "q2": 4,
  "q3": 2,
  "q4": 5,
  "q5": 3
}
```

Resposta (200):
```json
{
  "id": 1,
  "vida_id": 1,
  "tipo": "ERGOS",
  "status": "respondido",
  "criado_em": "2024-01-10T10:40:00",
  "respondido_em": "2024-01-10T11:00:00"
}
```

---

## Análise de Risco

### Calcular Risco

```http
POST /analise-risco/1/calcular
```

Resposta (201):
```json
{
  "id": 1,
  "questionario_id": 1,
  "score_psicossocial": 62.5,
  "nivel_risco": "alto",
  "criado_em": "2024-01-10T11:05:00"
}
```

### Obter Análise

```http
GET /analise-risco/1
```

Resposta (200):
```json
{
  "id": 1,
  "questionario_id": 1,
  "score_psicossocial": 62.5,
  "nivel_risco": "alto",
  "criado_em": "2024-01-10T11:05:00"
}
```

---

## Documentos

### Gerar PDF (NR1/NR17)

```http
POST /documentos/1/pdf
```

Resposta (202 Accepted):
```json
{
  "message": "PDF generation queued",
  "analise_id": 1,
  "task_id": "abc-def-ghi-jkl"
}
```

### Baixar PDF

```http
GET /documentos/1/download
```

Resposta (200): Arquivo PDF binário

---

## Códigos de Status

- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `202 Accepted`: Processamento iniciado (async)
- `400 Bad Request`: Validação falhou
- `401 Unauthorized`: Falta autenticação
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro no servidor

## Erros

Formato padrão:

```json
{
  "detail": "Descrição do erro"
}
```

---

Para mais detalhes sobre modelos, veja `ARQUITETURA.md`.
