<!-- Copilot instructions geradas automaticamente — por favor revise e ajuste -->
# Instruções rápidas para agentes de IA (Copilot)

Este arquivo contém o conhecimento essencial para um agente de programação ser imediatamente produtivo neste repositório.

**Resumo Rápido**
- **Propósito do repositório:** protótipo minimalista chamado `newplan-prototipo` (veja `README.md`).
- **Estado atual:** repositório muito enxuto — somente `README.md` no root. Antes de executar mudanças significativas, confirme com o mantenedor os objetivos e comandos de build/test.

**Onde Começar**
- **Ler:** abra `README.md` e procure instruções de execução. Atualmente o `README.md` é mínimo; trate-o como a fonte primária para contexto de alto nível.
- **Procurar artefatos típicos:** verifique a presença de `package.json`, `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `Makefile`, diretórios `src/`, `packages/`, `services/`, `infra/` e `tests/`.
  - Exemplos de comandos úteis: `git ls-files`, `rg "package.json|pyproject.toml|Dockerfile|docker-compose.yml|Makefile|src/|tests/" -S`.

**Arquitetura / Big Picture (o que procurar)**
- **Componentes maiores:** não há código aqui para inferir camadas; ao encontrar `src/` ou `services/`, determine fronteiras de serviço (APIs, jobs, workers).
- **Fluxos de dados:** procure por arquivos `*.proto`, `api/`, `routes/`, `handlers/` ou `controllers/` para mapear entrada → processamento → persistência.
- **Decisões estruturais:** rastreie arquivos `Dockerfile`, `k8s/`, `terraform/` ou `infra/` para entender deployment e por que certas bibliotecas/versões foram escolhidas.

**Workflows de desenvolvedor (como descobrir e executar)**
- **Instalação/Build:** se `package.json` existir, use `npm ci` ou `pnpm install`; se `pyproject.toml`, use `pip install -r requirements.txt` ou `pip install -e .`.
- **Testes:** procurar `pytest`, `jest`, `mocha` ou `go test`. Exemplos:
  - `npm test` ou `pnpm test`
  - `python -m pytest`
  - `go test ./...`
- **Container / infra:** se houver `docker-compose.yml`, iniciar com `docker compose up --build` para reproduzir ambiente local.
- **Depuração:** busque argumentos de execução em `launch.json` (`.vscode/`), `Makefile` ou scripts `package.json` para os comandos de run/debug.

**Padrões e convenções do projeto (o que o agente deve respeitar)**
- **Pequenos commits e PRs:** mantenha mudanças focadas e documente o propósito no título/descrição do PR.
- **Estrutura de código:** se existir `src/`, siga a mesma organização (não mover módulos sem validar). Se testes estiverem em `tests/` ou `__tests__`, adicione os seus lá.
- **Nomes de variáveis/arquivos:** seguir o estilo predominante (camelCase vs snake_case). Antes de formatar, verifique se há `prettier`, `black` ou `gofmt` configurados.

**Integrações e dependências externas (onde procurar sinais)**
- **Variáveis de ambiente:** procurar `.env`, `.env.example`, `config/` ou `settings/` para chaves de serviços externos.
- **Cloud / infra:** arquivos `aws/`, `gcp/`, `terraform/`, `pulumi/`, `k8s/` indicam integrações; trate credenciais como sensíveis — não as exiba.
- **APIs externas:** rastreie strings `https://` em arquivos de configuração e códigos para localizar dependências externas.

**Exemplos práticos (como agir aqui)**
- **Se o repositório só tem `README.md`:** 1) não adivinhe comandos de build; 2) abra uma issue ou PR que proponha um layout minimal (ex.: `src/`, `README` estendido, `tests/`); 3) peça ao mantenedor as instruções de execução.
- **Ao adicionar código:** inclua pelo menos um teste simples e um item no `README.md` descrevendo como executar o componente.

**Quando perguntar ao humano (sinais claros)**
- Se faltarem comandos para build/test/run.
- Se a mudança tocar infra (Docker, k8s, terraform) sem instruções de deploy.
- Se for necessário acessar segredos ou contas externas.

**Referências rápidas**
- Arquivo principal de contexto: `README.md` (root).
- Novo arquivo de instrução criado: `.github/copilot-instructions.md`.

Se algo aqui estiver impreciso, por favor atualize este arquivo ou responda com os detalhes de build/test/arquitetura para que eu refine as instruções.

*** Fim do arquivo ***
