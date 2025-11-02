# Arquivos de Deploy - Referência Rápida

Este documento descreve todos os arquivos relacionados ao deploy em produção do Sistema de Monitoria de Atendimento.

## Arquivos Docker

### `/docker-compose.yml`
Arquivo principal de orquestração que define todos os serviços da aplicação. Este arquivo coordena três containers: banco de dados PostgreSQL, backend Flask e frontend React/Nginx. A configuração inclui healthchecks, volumes persistentes para dados do PostgreSQL, e uma rede interna para comunicação entre os serviços.

**Serviços definidos:**
- `database`: PostgreSQL 14 com volume persistente
- `backend`: API Flask com Gunicorn (4 workers)
- `frontend`: Aplicação React servida pelo Nginx

### `/backend/Dockerfile`
Dockerfile multi-estágio para construção da imagem do backend. Utiliza Python 3.11 slim como base, instala dependências do sistema necessárias para PostgreSQL, e configura o Gunicorn como servidor WSGI de produção. A imagem final executa com um usuário não-root para maior segurança.

### `/frontend/Dockerfile`
Dockerfile multi-estágio para construção da imagem do frontend. O primeiro estágio compila a aplicação React usando Node.js 22 e pnpm, gerando os assets otimizados. O segundo estágio usa Nginx Alpine para servir os arquivos estáticos buildados, resultando em uma imagem final extremamente leve (cerca de 25MB).

### `/frontend/nginx.conf`
Configuração customizada do Nginx para o frontend. Define regras de cache para assets estáticos, compressão Gzip para melhor performance, proxy reverso para redirecionar chamadas `/api` para o backend, e headers de segurança (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection). A configuração também implementa o padrão SPA (Single Page Application), garantindo que todas as rotas retornem o `index.html`.

## Scripts de Automação

### `/deploy.sh`
Script Bash completo para gerenciamento do ciclo de vida da aplicação. Oferece comandos para deploy, build, start, stop, restart, visualização de logs, inicialização do banco de dados, backup e restore. O script inclui verificações de pré-requisitos, mensagens coloridas para melhor UX, e confirmações para operações destrutivas.

**Principais comandos:**
- `./deploy.sh deploy`: Deploy completo automatizado
- `./deploy.sh backup`: Cria backup do banco de dados
- `./deploy.sh restore <arquivo>`: Restaura backup
- `./deploy.sh logs [serviço]`: Visualiza logs em tempo real

### `/Makefile`
Atalhos simplificados para os comandos do `deploy.sh`. Permite executar operações comuns com comandos curtos como `make deploy`, `make logs-backend`, `make backup`. Ideal para desenvolvedores familiarizados com Make.

## Variáveis de Ambiente

### `/.env.example`
Template de configuração com todas as variáveis de ambiente necessárias. Inclui comentários explicativos para cada variável e avisos sobre a importância de alterar valores padrão em produção. Este arquivo deve ser versionado no Git.

**Variáveis críticas:**
- `SECRET_KEY`: Chave secreta do Flask
- `JWT_SECRET_KEY`: Chave para assinatura de tokens JWT
- `POSTGRES_PASSWORD`: Senha do banco de dados
- `VITE_API_URL`: URL da API para o frontend

### `/.env`
Arquivo de configuração real com valores de produção. **Nunca deve ser versionado no Git** (incluído no `.gitignore`). Deve ser criado a partir do `.env.example` e customizado para cada ambiente.

### `/backend/.env` e `/backend/.env.example`
Configurações específicas do backend. Mantidas para compatibilidade com execução local sem Docker.

### `/frontend/.env` e `/frontend/.env.production`
Configurações específicas do frontend. O arquivo `.env.production` é usado durante o build do Docker para definir a URL da API.

## Arquivos de Configuração

### `/backend/.dockerignore`
Define quais arquivos devem ser excluídos ao construir a imagem Docker do backend. Inclui cache Python (`__pycache__`, `*.pyc`), ambientes virtuais, logs e arquivos de desenvolvimento.

### `/frontend/.dockerignore`
Define exclusões para o build do frontend. Exclui `node_modules`, `dist`, logs e arquivos de configuração local.

### `/.gitignore`
Lista de arquivos que não devem ser versionados no Git. Inclui arquivos `.env`, caches, builds, logs, backups e diretórios de dependências.

## Documentação

### `/docs/DEPLOY.md`
Guia completo de deploy em produção. Cobre instalação de pré-requisitos (Docker, Docker Compose), configuração de ambiente, processo de deploy, gerenciamento da aplicação, backup/restore e configuração de domínio com HTTPS.

### `/docs/GUIA_USUARIO.md`
Manual do usuário final explicando como usar o sistema. Descreve perfis de acesso (operador, supervisor, administrador), funcionalidades principais (dashboard, gestão de chamadas, avaliações) e dicas de uso.

### `/docs/CHECKLIST_DEPLOY.md`
Checklist detalhado para validação de deploy. Organizado em seções: pré-deploy, durante o deploy, pós-deploy e produção real. Garante que nenhum passo crítico seja esquecido.

## Fluxo de Deploy Recomendado

O processo completo de deploy segue este fluxo:

1. **Preparação:** Clonar repositório, copiar `.env.example` para `.env` e configurar variáveis
2. **Validação:** Verificar pré-requisitos com checklist
3. **Execução:** Rodar `./deploy.sh deploy` ou `make deploy`
4. **Verificação:** Testar acesso ao frontend e backend
5. **Backup:** Criar backup inicial com `./deploy.sh backup`
6. **Documentação:** Registrar versão e configurações implantadas

## Manutenção

Para manutenção contínua, os seguintes arquivos são essenciais:

- **Logs:** Acessar via `./deploy.sh logs` ou `docker-compose logs`
- **Backups:** Criados em `./backups/` com timestamp
- **Atualizações:** Usar `git pull` + `./deploy.sh build` + `./deploy.sh restart`

Todos os arquivos foram projetados para serem autoexplicativos e incluem comentários detalhados quando necessário.
