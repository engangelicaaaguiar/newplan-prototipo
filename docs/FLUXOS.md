# Fluxos Principais

## 1. Fluxo de Importação

```
┌─────────────────────────────────────────────────────────┐
│  Usuário sobe arquivo CSV/Excel via frontend            │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  POST /importacao/empresas                              │
│  POST /importacao/cargos                                │
│  POST /importacao/vidas                                 │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  Backend valida com Pydantic schemas                    │
│  SQLAlchemy insere em DB                                │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  Retorna IDs criados ao frontend                        │
│  Frontend exibe confirmação                             │
└─────────────────────────────────────────────────────────┘
```

### Decisões Chave
- Validação no Pydantic antes de persistência
- Transações DB para integridade (rollback se falhar)
- IDs retornados para rastreamento

---

## 2. Fluxo de Questionário

```
┌──────────────────────────────────────────────────────┐
│  Frontend: usuário clica em "Responder Questionário"  │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  POST /questionarios/?vida_id=X&tipo=ERGOS           │
│  Cria Questionario com status="pendente"             │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Frontend renderiza formulário (18-20 questões)      │
│  Usuário responde com escala 1-5                    │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  PUT /questionarios/X/respostas                      │
│  { "q1": 3, "q2": 4, ... }                          │
│  Atualiza status = "respondido"                      │
│  Registra respondido_em = now()                      │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Frontend exibe sucesso                              │
│  Pronto para análise de risco                        │
└──────────────────────────────────────────────────────┘
```

### Regras de Negócio
- Questionário pode ser respondido apenas uma vez (ou atualizado)
- Respostas armazenadas como JSON para flexibilidade
- Auditoria de timestamp de resposta

---

## 3. Fluxo de Análise de Risco

```
┌──────────────────────────────────────────────────────┐
│  Usuário clica em "Calcular Risco"                    │
│  POST /analise-risco/X/calcular                       │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Backend processa:                                    │
│  1. Valida questionário está respondido              │
│  2. Busca respostas em JSON                          │
│  3. Aplica tabelas Ergos                             │
│  4. Calcula score psicossocial (0-100)              │
│  5. Determina nível: baixo/médio/alto/crítico       │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Armazena AnaliseRisco em DB                         │
│  Gera recomendações personalizadas                    │
│  Retorna análise ao frontend                         │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Frontend exibe:                                      │
│  - Score psicossocial (gráfico)                      │
│  - Nível de risco (badge colorido)                   │
│  - Recomendações de ação                             │
│  - Opção para gerar documento                        │
└──────────────────────────────────────────────────────┘
```

### Cálculo de Score (Ergos)
Baseado em metodologia NR1:
- Peso para cada fator (carga mental 25%, ritmo 20%, etc)
- Média ponderada das respostas (1-5)
- Normalização para escala 0-100

**Tabela de Risco:**
| Faixa | Nível | Ação |
|-------|-------|------|
| 0-25 | Baixo | Monitoramento anual |
| 25-50 | Médio | Revisão semestral |
| 50-75 | Alto | Intervenção imediata |
| 75-100 | Crítico | Afastamento recomendado |

---

## 4. Fluxo de Geração de Documento (NR1/NR17)

```
┌──────────────────────────────────────────────────────┐
│  Usuário clica em "Gerar PDF"                         │
│  POST /documentos/X/pdf (analise_id=X)               │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Backend retorna 202 Accepted                         │
│  Enfileira Celery task async                          │
│  Frontend exibe spinner (polling ou WebSocket)       │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Celery Worker:                                       │
│  1. Busca dados: empresa, vida, questionario, análise│
│  2. ReportLab/python-docx renderiza template        │
│  3. Insere tabelas, gráficos, recomendações         │
│  4. Salva em storage (local ou S3)                   │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  GET /documentos/X/download                          │
│  Retorna PDF binário (ou link presigned se S3)      │
└────────┬─────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────┐
│  Frontend oferece download                            │
│  Usuário recebe laudo NR1 em PDF                     │
└──────────────────────────────────────────────────────┘
```

### Decisões Chave
- **Async com Celery**: PDFs podem levar segundos/minutos
- **Storage**: Local para dev, S3 em produção recomendado
- **Auditoria**: Registra quem gerou, quando e qual versão

---

## 5. Dashboard

```
┌─────────────────────────────────────────────────────┐
│                    HOME / DASHBOARD                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐  ┌────────────┐  ┌─────────────────┐ │
│  │Importação│  │Questionário│  │  Análise Risco  │ │
│  │          │  │            │  │                 │ │
│  │ Gerenciar│  │ Listar     │  │ Visualizar      │ │
│  │ empresas │  │ respondidos│  │ scores/níveis   │ │
│  │ e vidas  │  │ pendentes  │  │                 │ │
│  └──────────┘  └────────────┘  └─────────────────┘ │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  DOCUMENTOS                                  │   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │   │
│  │  │PDF-1 │  │PDF-2 │  │PDF-3 │  │+ Novo│    │   │
│  │  └──────┘  └──────┘  └──────┘  └──────┘    │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Acesso e Permissões** (futuro):
- Admin: acesso a todas empresas
- Gerenciador RH: acesso departamento específico
- Funcionário: acesso próprio questionário

---

## Sequência Completa: De Empresa até Laudo

```
1. HR IMPORTA DADOS
   └→ CSV com lista de empresas/cargos/funcionários
   └→ Sistema valida e armazena

2. FUNCIONÁRIO RESPONDE QUESTIONÁRIO
   └→ Acessa portal e preenche Ergos (18 questões)
   └→ Sistema registra respostas com timestamp

3. ANÁLISE AUTOMÁTICA
   └→ Sistema calcula score psicossocial (0-100)
   └→ Classifica risco (baixo/médio/alto/crítico)
   └→ Gera recomendações personalizadas

4. GERAÇÃO DE DOCUMENTO (NR1/NR17)
   └→ Backend enfileira task async
   └→ Celery renderiza PDF profissional
   └→ Usuário baixa laudo

5. AUDITORIA E CONFORMIDADE
   └→ Todos os passos registrados em DB
   └→ Rastreabilidade completa para auditoria
   └→ Conformidade com NR1 e NR17
```

Veja `SETUP.md` para começar a desenvolver.
