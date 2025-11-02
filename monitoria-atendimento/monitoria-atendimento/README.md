# Sistema de Monitoria de Atendimento

[![Status](https://img.shields.io/badge/status-MVP%20Completo-success)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Sistema web completo para monitoramento, avaliação e feedback de qualidade de atendimento ao cliente. Desenvolvido com stack open source (Python/Flask + React + PostgreSQL) e totalmente preparado para deploy em produção via Docker.

## 🎯 Visão Geral

Este sistema permite que supervisores avaliem chamadas de atendimento com base em critérios objetivos, fornecendo feedback estruturado aos operadores e métricas de performance em tempo real. A solução é **100% web** - usuários acessam via navegador sem necessidade de instalação.

### Principais Funcionalidades

- ✅ **Autenticação JWT** com controle de acesso por perfis (Admin, Supervisor, Operador)
- ✅ **Gestão de Chamadas** com protocolo único, categorização e priorização
- ✅ **Sistema de Avaliação** com 6 critérios de pontuação (1-5)
- ✅ **Dashboard Interativo** com gráficos e estatísticas em tempo real
- ✅ **Filtros Avançados** por status, prioridade, categoria e período
- ✅ **Interface Responsiva** que funciona em desktop, tablet e mobile
- ✅ **Deploy Automatizado** com Docker Compose e scripts de gerenciamento

## 🏗️ Arquitetura

### Stack Tecnológica

**Backend:**
- Python 3.11 + Flask
- SQLAlchemy ORM
- PostgreSQL 14
- Flask-JWT-Extended
- Gunicorn (produção)

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- React Router
- Axios + React Query
- Recharts (gráficos)

**Infraestrutura:**
- Docker + Docker Compose
- Nginx (proxy reverso)
- Shell scripts (automação)

### Estrutura do Projeto

```
monitoria-atendimento/
├── backend/              # API Flask
│   ├── app/
│   │   ├── models/       # Modelos SQLAlchemy
│   │   └── routes/       # Endpoints da API
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # Aplicação React
│   ├── src/
│   │   ├── components/   # Componentes reutilizáveis
│   │   ├── pages/        # Páginas da aplicação
│   │   └── context/      # Contexto de autenticação
│   ├── Dockerfile
│   └── nginx.conf
├── docs/                 # Documentação completa
├── docker-compose.yml    # Orquestração de containers
├── deploy.sh             # Script de deploy automatizado
├── Makefile              # Atalhos de comandos
└── .env.example          # Template de configuração
```

## 🚀 Deploy em Produção

### Pré-requisitos

- Servidor Linux (Ubuntu 20.04+, CentOS 7+, etc.)
- Docker 20.10+
- Docker Compose 2.5+

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd monitoria-atendimento

# 2. Configure as variáveis de ambiente
cp .env.example .env
nano .env  # Altere SECRET_KEY, JWT_SECRET_KEY e POSTGRES_PASSWORD

# 3. Execute o deploy
chmod +x deploy.sh
./deploy.sh deploy

# Ou use o Makefile
make deploy
```

**Pronto!** A aplicação estará disponível em `http://<IP_DO_SERVIDOR>`

### Comandos de Gerenciamento

| Comando              | Descrição                              |
|----------------------|----------------------------------------|
| `make start`         | Iniciar serviços                       |
| `make stop`          | Parar serviços                         |
| `make restart`       | Reiniciar serviços                     |
| `make logs`          | Ver logs em tempo real                 |
| `make logs-backend`  | Ver logs do backend                    |
| `make backup`        | Criar backup do banco de dados         |
| `make status`        | Ver status dos containers              |

Para mais detalhes, consulte a [documentação completa de deploy](docs/DEPLOY.md).

## 👥 Credenciais de Demonstração

Se o sistema foi instalado com dados de exemplo:

| Perfil        | Usuário    | Senha        |
|---------------|------------|--------------|
| Administrador | admin      | admin123     |
| Supervisor    | supervisor | supervisor123|
| Operador      | joão.silva | operator123  |

**⚠️ IMPORTANTE:** Altere todas as senhas padrão em ambiente de produção!

## 📚 Documentação

A documentação completa está organizada na pasta `docs/`:

- **[RESUMO_EXECUTIVO.md](docs/RESUMO_EXECUTIVO.md)** - Visão geral do projeto
- **[DEPLOY.md](docs/DEPLOY.md)** - Guia completo de deploy
- **[GUIA_USUARIO.md](docs/GUIA_USUARIO.md)** - Manual do usuário
- **[CHECKLIST_DEPLOY.md](docs/CHECKLIST_DEPLOY.md)** - Checklist de validação
- **[ARQUIVOS_DEPLOY.md](docs/ARQUIVOS_DEPLOY.md)** - Referência de arquivos

Acesse o [índice completo da documentação](docs/README.md).

## 🔧 Desenvolvimento Local

Para executar o projeto em modo de desenvolvimento (sem Docker):

### Backend

```bash
cd backend

# Instalar dependências
pip3 install -r requirements.txt

# Configurar banco de dados PostgreSQL
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE monitoria_atendimento;"

# Inicializar banco com dados de exemplo
python3 init_db.py

# Iniciar servidor
python3 app.py
```

Backend rodando em `http://localhost:5000`

### Frontend

```bash
cd frontend

# Instalar dependências
pnpm install

# Iniciar servidor de desenvolvimento
pnpm dev
```

Frontend rodando em `http://localhost:5173`

## 🔐 Segurança

- Autenticação JWT com refresh tokens
- Senhas hasheadas com bcrypt
- Usuário não-root nos containers
- Headers de segurança no Nginx
- CORS configurado adequadamente
- Variáveis sensíveis em `.env` (não versionado)

## 📊 Métricas e Performance

- **Build otimizado** com code splitting e minificação
- **Gzip habilitado** para compressão de assets
- **Cache agressivo** para arquivos estáticos
- **Múltiplos workers** Gunicorn para processamento paralelo
- **Healthchecks** para garantir disponibilidade dos serviços

## 🛠️ Tecnologias Utilizadas

### Backend
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)

### Frontend
![React](https://img.shields.io/badge/React-18-blue?logo=react)
![Vite](https://img.shields.io/badge/Vite-5-purple?logo=vite)
![Tailwind](https://img.shields.io/badge/Tailwind-3-blue?logo=tailwindcss)

### DevOps
![Docker](https://img.shields.io/badge/Docker-24-blue?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-1.25-green?logo=nginx)

## 📈 Próximos Passos

Melhorias planejadas para versões futuras:

- [ ] Página de criação/edição de avaliações
- [ ] Formulário de nova chamada
- [ ] Sistema de notificações
- [ ] Relatórios em PDF
- [ ] Upload de gravações
- [ ] Exportação de dados (Excel/CSV)
- [ ] Dashboard em tempo real (WebSockets)
- [ ] Aplicativo mobile

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido por **Manus AI**

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a [documentação completa](docs/README.md)
- Abra uma issue no repositório
- Entre em contato com o administrador do sistema

---

**Versão:** 1.0 - MVP Completo  
**Última Atualização:** 02 de Novembro de 2025
