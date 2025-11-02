## Guia de Deploy - Sistema de Monitoria de Atendimento

Este guia oferece instruções detalhadas para fazer o deploy do sistema em diferentes provedores de nuvem. O método recomendado para todos os provedores é utilizando **Docker e Docker Compose**, pois garante um ambiente consistente e facilita a manutenção.

### Pré-requisitos Essenciais

Antes de começar, você precisará de:

1.  **Conta no Provedor de Nuvem:** Acesso a uma conta na DigitalOcean, Render, AWS, ou outro de sua preferência.
2.  **Domínio (Opcional):** Um nome de domínio registrado para acessar sua aplicação (ex: `monitoria.suaempresa.com`).
3.  **Acesso ao Terminal/SSH:** Permissão para se conectar ao seu servidor via SSH.
4.  **Arquivos do Projeto:** O pacote `monitoria-atendimento.zip` que contém todo o código e configurações.

---

### Opção 1: DigitalOcean (Recomendado para Custo-Benefício)

A DigitalOcean oferece Droplets (servidores virtuais) fáceis de configurar e com preço competitivo.

**Passos:**

1.  **Criar um Droplet:**
    *   Acesse sua conta na DigitalOcean e clique em "Create" > "Droplets".
    *   **Marketplace:** Procure por "Docker" e selecione a imagem pré-configurada. Isso já instala o Docker e o Docker Compose para você.
    *   **Plano:** Escolha um plano básico (ex: 1 CPU, 1GB RAM) para começar. O sistema é leve.
    *   **Região:** Escolha uma região próxima aos seus usuários (ex: São Paulo).
    *   **Autenticação:** Adicione sua chave SSH para acesso seguro.
    *   Clique em "Create Droplet".

2.  **Conectar ao Servidor:**
    *   Copie o endereço de IP do seu novo Droplet.
    *   Abra seu terminal e conecte-se via SSH:
        ```bash
        ssh root@SEU_IP_DO_DROPLET
        ```

3.  **Fazer Upload e Descompactar:**
    *   Copie o arquivo `monitoria-atendimento.zip` para o servidor:
        ```bash
        scp /caminho/local/monitoria-atendimento.zip root@SEU_IP_DO_DROPLET:/root/
        ```
    *   No servidor, instale o `unzip` e descompacte o arquivo:
        ```bash
        apt-get update && apt-get install -y unzip
        unzip monitoria-atendimento.zip
        cd monitoria-atendimento
        ```

4.  **Configurar e Iniciar:**
    *   Copie o arquivo de exemplo `.env.example` para `.env`:
        ```bash
        cp .env.example .env
        ```
    *   **Edite o arquivo `.env`** e altere as senhas e chaves secretas. Use o comando `nano .env`.
    *   Inicie a aplicação com Docker Compose:
        ```bash
        docker-compose up -d
        ```

5.  **Acessar o Sistema:**
    *   Acesse `http://SEU_IP_DO_DROPLET` no seu navegador.
    *   O sistema estará funcionando!

---

### Opção 2: Render.com (Plano Gratuito Disponível)

O Render é uma plataforma PaaS que facilita o deploy de aplicações web e bancos de dados.

**Passos:**

1.  **Criar um Banco de Dados PostgreSQL:**
    *   No dashboard do Render, clique em "New" > "PostgreSQL".
    *   Dê um nome ao seu banco de dados e escolha um plano (o plano gratuito é suficiente para começar).
    *   Após a criação, copie a **URL de Conexão Interna** (Internal Connection URL).

2.  **Criar um Web Service:**
    *   Clique em "New" > "Web Service".
    *   Conecte sua conta do GitHub e selecione o repositório do projeto (você precisará fazer o upload do projeto para o GitHub primeiro).
    *   **Configurações:**
        *   **Environment:** Docker
        *   **Root Directory:** Deixe em branco
        *   **DockerfilePath:** `./docker-compose.yml` (Render pode usar docker-compose diretamente)
    *   **Variáveis de Ambiente:**
        *   Adicione todas as variáveis do arquivo `.env.example`.
        *   Em `DATABASE_URL`, cole a URL de conexão interna do seu banco de dados PostgreSQL.

3.  **Deploy:**
    *   Clique em "Create Web Service".
    *   O Render irá buildar e fazer o deploy da sua aplicação automaticamente.

4.  **Acessar o Sistema:**
    *   O Render fornecerá uma URL pública (ex: `monitoria.onrender.com`).

---

### Opção 3: AWS (Amazon Web Services)

Para a AWS, a opção mais simples é usar o **EC2** para um servidor virtual.

**Passos:**

1.  **Lançar uma Instância EC2:**
    *   No console da AWS, vá para EC2 e clique em "Launch instances".
    *   **AMI:** Escolha uma AMI do Ubuntu Server (ex: 22.04 LTS).
    *   **Instance Type:** `t2.micro` ou `t3.micro` é suficiente para começar (geralmente elegível para o Free Tier).
    *   **Key Pair:** Crie ou selecione um par de chaves para acesso SSH.
    *   **Security Group:** Crie um novo grupo de segurança e adicione regras para permitir tráfego nas portas `80` (HTTP), `443` (HTTPS) e `22` (SSH).
    *   Clique em "Launch instance".

2.  **Instalar Docker e Docker Compose:**
    *   Conecte-se à sua instância EC2 via SSH.
    *   Siga o [guia oficial da Docker](https://docs.docker.com/engine/install/ubuntu/) para instalar o Docker.
    *   Instale o Docker Compose:
        ```bash
        sudo apt-get install docker-compose-plugin
        ```

3.  **Fazer Upload e Deploy:**
    *   Siga os mesmos passos 3 e 4 da seção da DigitalOcean para fazer o upload, descompactar, configurar o `.env` e iniciar com `docker-compose up -d`.

4.  **Acessar o Sistema:**
    *   Acesse `http://SEU_IP_PUBLICO_DA_EC2` no seu navegador.

---

### Configuração Pós-Deploy (Opcional, mas Recomendado)

Após o deploy, considere fazer o seguinte:

-   **Configurar um Domínio:** Aponte seu domínio para o IP do seu servidor.
-   **Habilitar HTTPS com Let's Encrypt:** Adicione um serviço de proxy reverso como o [Nginx Proxy Manager](https://nginxproxymanager.com/) ou configure o Caddy para obter SSL gratuito e renovação automática.
-   **Configurar Backups:** Crie um script para fazer backup periódico do volume do PostgreSQL.

Se precisar de ajuda com qualquer um desses passos, posso fornecer instruções mais detalhadas.
