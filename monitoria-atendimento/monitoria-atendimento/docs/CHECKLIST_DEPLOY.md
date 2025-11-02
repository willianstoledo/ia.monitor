# Checklist de Deploy - Sistema de Monitoria de Atendimento

Use este checklist para garantir que todos os passos necessários foram executados antes de colocar o sistema em produção.

## Pré-Deploy

### Servidor
- [ ] Servidor Linux configurado e acessível via SSH
- [ ] Docker instalado (versão 20.10+)
- [ ] Docker Compose instalado (versão 2.5+)
- [ ] Git instalado
- [ ] Portas 80 (frontend) e 5000 (backend) liberadas no firewall
- [ ] Recursos adequados: mínimo 2GB RAM, 2 CPUs, 20GB disco

### Segurança
- [ ] Arquivo `.env` criado a partir do `.env.example`
- [ ] `SECRET_KEY` alterada para valor único e seguro
- [ ] `JWT_SECRET_KEY` alterada para valor único e seguro
- [ ] `POSTGRES_PASSWORD` alterada para senha forte
- [ ] Arquivo `.env` adicionado ao `.gitignore` (não versionar)
- [ ] Chaves SSH configuradas para acesso seguro ao servidor

### Configuração
- [ ] Variável `VITE_API_URL` configurada corretamente no `.env`
- [ ] Variáveis de ambiente do banco de dados verificadas
- [ ] Configurações de workers e timeout do Gunicorn ajustadas se necessário

## Durante o Deploy

### Build e Inicialização
- [ ] Repositório clonado no servidor
- [ ] Script `deploy.sh` com permissões de execução (`chmod +x`)
- [ ] Comando `./deploy.sh deploy` executado com sucesso
- [ ] Todos os containers iniciados (verificar com `docker-compose ps`)
- [ ] Logs verificados sem erros críticos (`docker-compose logs`)

### Banco de Dados
- [ ] Banco de dados criado automaticamente
- [ ] Tabelas criadas com sucesso
- [ ] Dados de exemplo populados (ou removidos se não desejado)
- [ ] Backup inicial criado (`./deploy.sh backup`)

### Aplicação
- [ ] Frontend acessível via navegador em `http://<IP_SERVIDOR>`
- [ ] Backend respondendo em `http://<IP_SERVIDOR>:5000/api/health`
- [ ] Login funcionando com credenciais de teste
- [ ] Dashboard carregando estatísticas corretamente
- [ ] Listagem de chamadas funcionando
- [ ] Filtros e paginação operacionais

## Pós-Deploy

### Testes Funcionais
- [ ] Login com diferentes perfis (admin, supervisor, operador)
- [ ] Criação de nova chamada
- [ ] Atualização de status de chamada
- [ ] Criação de avaliação (supervisor/admin)
- [ ] Visualização de dashboard com dados corretos
- [ ] Filtros de período funcionando
- [ ] Navegação entre páginas sem erros
- [ ] Responsividade testada em mobile

### Segurança e Acesso
- [ ] Senhas padrão alteradas para todas as contas
- [ ] Usuários de produção criados
- [ ] Permissões de usuários validadas
- [ ] Tokens JWT expirando corretamente
- [ ] CORS configurado adequadamente
- [ ] Headers de segurança do Nginx verificados

### Performance
- [ ] Tempo de resposta da API aceitável (< 500ms para queries simples)
- [ ] Frontend carregando rapidamente
- [ ] Imagens e assets otimizados
- [ ] Gzip habilitado no Nginx
- [ ] Cache de assets estáticos funcionando

### Monitoramento
- [ ] Logs sendo gerados corretamente
- [ ] Sistema de backup automático configurado (opcional)
- [ ] Alertas de erro configurados (opcional)
- [ ] Monitoramento de recursos do servidor (CPU, RAM, disco)

### Documentação
- [ ] README.md atualizado com URL de produção
- [ ] Guia do usuário compartilhado com a equipe
- [ ] Credenciais de admin documentadas em local seguro
- [ ] Procedimentos de backup e restore documentados

## Produção Real (Opcional mas Recomendado)

### Domínio e HTTPS
- [ ] Domínio registrado e DNS configurado
- [ ] Certificado SSL/TLS instalado (Let's Encrypt ou outro)
- [ ] Redirecionamento HTTP → HTTPS configurado
- [ ] HSTS habilitado

### Infraestrutura
- [ ] Proxy reverso configurado (Nginx, Traefik, etc.)
- [ ] Load balancer configurado (se aplicável)
- [ ] CDN configurado para assets estáticos (opcional)
- [ ] Backup automático agendado

### Compliance
- [ ] LGPD: Política de privacidade implementada
- [ ] Logs de acesso e auditoria configurados
- [ ] Retenção de dados definida
- [ ] Procedimento de exclusão de dados implementado

## Rollback

### Plano de Contingência
- [ ] Backup do banco de dados antes do deploy
- [ ] Versão anterior da aplicação documentada
- [ ] Procedimento de rollback testado
- [ ] Contatos de emergência documentados

---

**Data do Deploy:** _______________  
**Responsável:** _______________  
**Versão Implantada:** _______________  
**Observações:** _______________________________________________
