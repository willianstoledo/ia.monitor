# Documentação - Sistema de Monitoria de Atendimento

Bem-vindo à documentação completa do Sistema de Monitoria de Atendimento. Esta pasta contém todos os guias, manuais e referências necessários para instalar, configurar, usar e manter o sistema.

## 📚 Índice de Documentos

### Para Começar

**[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)**  
Visão geral completa do projeto, incluindo arquitetura, funcionalidades, stack tecnológica e próximos passos. Recomendado como primeira leitura para entender o escopo e capacidades do sistema.

### Deploy e Infraestrutura

**[DEPLOY.md](DEPLOY.md)**  
Guia completo de deploy em produção. Cobre instalação de pré-requisitos (Docker, Docker Compose), configuração de ambiente, processo de deploy, gerenciamento da aplicação, backup/restore e configuração de domínio com HTTPS. **Essencial para administradores de sistema.**

**[CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md)**  
Checklist detalhado para validação de deploy. Organizado em seções: pré-deploy, durante o deploy, pós-deploy e produção real. Use este documento para garantir que nenhum passo crítico seja esquecido durante a implantação.

**[ARQUIVOS_DEPLOY.md](ARQUIVOS_DEPLOY.md)**  
Referência completa de todos os arquivos relacionados ao deploy (Dockerfiles, docker-compose.yml, scripts, configurações). Explica a função de cada arquivo e como eles se relacionam.

### Para Usuários

**[GUIA_USUARIO.md](GUIA_USUARIO.md)**  
Manual do usuário final explicando como usar o sistema. Descreve perfis de acesso (operador, supervisor, administrador), funcionalidades principais (dashboard, gestão de chamadas, avaliações) e dicas de uso. **Compartilhe este documento com sua equipe.**

### Desenvolvimento

**[PROGRESSO_SESSAO.md](PROGRESSO_SESSAO.md)**  
Histórico detalhado do desenvolvimento inicial do sistema. Documenta decisões técnicas, desafios encontrados, soluções aplicadas e próximos passos recomendados. Útil para desenvolvedores que darão continuidade ao projeto.

### Referências

**[ESTRUTURA_FINAL.txt](ESTRUTURA_FINAL.txt)**  
Árvore de diretórios e arquivos do projeto completo. Use como referência rápida para localizar componentes específicos.

**[ESTRUTURA_PROJETO.txt](ESTRUTURA_PROJETO.txt)**  
Estrutura inicial do projeto (versão de desenvolvimento).

## 🚀 Início Rápido

Se você quer fazer o deploy imediatamente, siga esta sequência:

1. Leia o **RESUMO_EXECUTIVO.md** para entender o sistema
2. Siga o **DEPLOY.md** passo a passo
3. Use o **CHECKLIST_DEPLOY.md** para validar a instalação
4. Compartilhe o **GUIA_USUARIO.md** com sua equipe

## 📋 Documentos por Público

### Você é Administrador de Sistema?
- Comece com: **DEPLOY.md**
- Valide com: **CHECKLIST_DEPLOY.md**
- Referência: **ARQUIVOS_DEPLOY.md**

### Você é Usuário Final?
- Leia: **GUIA_USUARIO.md**

### Você é Desenvolvedor?
- Visão geral: **RESUMO_EXECUTIVO.md**
- Histórico: **PROGRESSO_SESSAO.md**
- Estrutura: **ESTRUTURA_FINAL.txt**

### Você é Gestor/Tomador de Decisão?
- Leia: **RESUMO_EXECUTIVO.md**

## 🔗 Links Úteis

- **README Principal:** `../README.md`
- **Script de Deploy:** `../deploy.sh`
- **Docker Compose:** `../docker-compose.yml`

## 📞 Suporte

Para dúvidas ou problemas não cobertos nesta documentação, consulte o administrador do sistema ou a equipe de TI da sua organização.

---

**Última Atualização:** 02 de Novembro de 2025  
**Versão da Documentação:** 1.0
