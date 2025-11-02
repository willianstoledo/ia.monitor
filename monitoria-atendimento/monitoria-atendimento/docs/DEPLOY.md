# Guia de Deploy - Sistema de Monitoria de Atendimento

Este guia detalha o processo de deploy da aplicação em um ambiente de produção utilizando Docker e Docker Compose. A arquitetura foi projetada para ser agnóstica ao provedor de nuvem, podendo ser executada em qualquer servidor Linux com Docker instalado.

## 1. Pré-requisitos

Antes de começar, garanta que o servidor de produção atenda aos seguintes requisitos:

- **Sistema Operacional:** Qualquer distribuição Linux moderna (Ubuntu 20.04+, CentOS 7+, etc.).
- **Docker:** Versão 20.10+.
- **Docker Compose:** Versão 2.5+ (plugin do Docker) ou `docker-compose` 1.29+.
- **Git:** Para clonar o repositório.
- **Acesso ao servidor:** Acesso SSH com permissões de superusuário (sudo).

### Instalação do Docker e Docker Compose

Se o Docker não estiver instalado, siga o guia oficial para sua distribuição. Para Ubuntu:

```bash
# Remover versões antigas
sudo apt-get remove docker docker-engine docker.io containerd runc

# Instalar dependências
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Adicionar chave GPG oficial do Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Adicionar repositório do Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine e Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Adicionar usuário ao grupo docker (para executar sem sudo)
sudo usermod -aG docker $USER

# Aplicar as alterações (pode ser necessário reiniciar a sessão)
newgrp docker
```

## 2. Configuração do Ambiente

### Passo 1: Clonar o Repositório

Conecte-se ao seu servidor via SSH e clone o repositório do projeto:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd monitoria-atendimento
```

### Passo 2: Configurar Variáveis de Ambiente

O arquivo `.env.example` contém o template para as variáveis de ambiente. Copie-o para `.env` e edite-o com suas configurações de produção.

```bash
cp .env.example .env
nano .env
```

**É crucial alterar as seguintes variáveis:**

- `SECRET_KEY`: Gere uma chave segura com `python3 -c "import secrets; print(secrets.token_hex(32))"`.
- `JWT_SECRET_KEY`: Gere outra chave segura com o mesmo comando.
- `POSTGRES_PASSWORD`: Defina uma senha forte para o banco de dados.
- `VITE_API_URL`: Se o frontend e o backend estiverem no mesmo servidor, mantenha `/api`. Se estiverem em domínios diferentes, altere para a URL completa da API (ex: `https://api.seudominio.com`).

## 3. Deploy da Aplicação

O script `deploy.sh` e o `Makefile` foram criados para automatizar o processo de deploy.

### Opção A: Usando o Script `deploy.sh` (Recomendado)

O script `deploy.sh` oferece um controle granular sobre o ciclo de vida da aplicação.

**Para realizar o deploy completo pela primeira vez:**

```bash
./deploy.sh deploy
```

Este comando irá:
1. Verificar se o Docker está instalado.
2. Verificar se o arquivo `.env` existe.
3. Construir as imagens Docker do backend e frontend (`--no-cache` para garantir a versão mais recente).
4. Iniciar todos os serviços em background (`-d`).
5. Aguardar o banco de dados ficar pronto.
6. Executar o script `init_db.py` para popular o banco com dados de exemplo (opcional, pode ser removido do script se não desejar).
7. Mostrar o status dos containers.

### Opção B: Usando `Makefile` (Simplificado)

O `Makefile` fornece atalhos para os comandos do `deploy.sh`.

**Para realizar o deploy completo:**

```bash
make deploy
```

## 4. Gerenciamento da Aplicação

Após o deploy, você pode gerenciar a aplicação com os seguintes comandos:

| Comando `make`        | Comando `deploy.sh`          | Descrição                                                 |
|-----------------------|------------------------------|-----------------------------------------------------------|
| `make start`          | `./deploy.sh start`          | Inicia os containers.                                     |
| `make stop`           | `./deploy.sh stop`           | Para os containers.                                       |
| `make restart`        | `./deploy.sh restart`        | Reinicia os containers.                                   |
| `make status`         | `./deploy.sh status`         | Mostra o status atual dos containers.                     |
| `make logs`           | `./deploy.sh logs`           | Exibe os logs de todos os serviços em tempo real.         |
| `make logs-backend`   | `./deploy.sh logs backend`   | Exibe os logs apenas do backend.                          |
| `make build`          | `./deploy.sh build`          | Força a reconstrução das imagens Docker.                  |
| `make init-db`        | `./deploy.sh init-db`        | Popula o banco de dados com dados de exemplo.             |
| `make backup`         | `./deploy.sh backup`         | Cria um backup do banco de dados na pasta `./backups`.    |
| `make clean`          | `./deploy.sh clean`          | **CUIDADO:** Para tudo e remove containers, imagens e volumes. |

## 5. Acesso à Aplicação

Após o deploy, a aplicação estará acessível:

- **Frontend:** `http://<IP_DO_SEU_SERVIDOR>`
- **Backend API:** `http://<IP_DO_SEU_SERVIDOR>:5000`

O Nginx dentro do container do frontend já está configurado para redirecionar as chamadas de `/api` para o serviço de backend, então a aplicação deve funcionar diretamente acessando a URL principal.

## 6. Atualizando a Aplicação

Para atualizar a aplicação com uma nova versão do código:

1. **Puxe as alterações do Git:**
   ```bash
   git pull origin main
   ```

2. **Reconstrua as imagens e reinicie os serviços:**
   ```bash
   make build
   make start
   ```
   Ou, de forma mais direta:
   ```bash
   docker-compose up -d --build
   ```

## 7. Backup e Restore

### Criando um Backup

O script automatiza a criação de backups do banco de dados.

```bash
make backup
```

Um arquivo `.sql` será salvo na pasta `./backups`.

### Restaurando um Backup

**ATENÇÃO:** Este processo sobrescreve os dados atuais do banco.

```bash
./deploy.sh restore ./backups/<NOME_DO_ARQUIVO_DE_BACKUP>.sql
```

## 8. Configuração de Domínio e HTTPS (Produção Real)

Para um ambiente de produção real, é altamente recomendado configurar um domínio e HTTPS.

1. **Apontar DNS:** Configure um registro `A` no seu provedor de DNS para apontar seu domínio (ex: `monitoria.suaempresa.com`) para o IP do seu servidor.

2. **Configurar Nginx com Certbot (Let's Encrypt):** A maneira mais fácil é usar um container Nginx separado como proxy reverso que gerencia os certificados SSL.

   - Você pode adaptar o `docker-compose.yml` para incluir um serviço de Nginx Proxy Manager ou configurar o Certbot manualmente no servidor host para gerenciar os certificados para o container do frontend.

Este guia fornece a base para um deploy robusto e gerenciável. Adapte as configurações de rede e segurança conforme as políticas da sua organização.
