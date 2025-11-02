# Sistema de Monitoria de Atendimento - Acesso Web

**Data de Deploy:** 02 de Novembro de 2025  
**Status:** ✅ Online e Funcionando  
**Autor:** Manus AI

---

## 🌐 Acesso à Aplicação

O sistema está **100% online** e pode ser acessado diretamente pelo navegador, sem necessidade de instalação de programas.

### URL Principal (Frontend)

**🔗 [https://3000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer](https://3000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer)**

Esta é a URL que você deve acessar no navegador para usar o sistema. A aplicação funciona em qualquer navegador moderno como Chrome, Firefox, Edge ou Safari, tanto em desktop quanto em dispositivos móveis.

### URL da API (Backend)

**🔗 [https://5000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer/api](https://5000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer/api)**

Esta URL é utilizada internamente pela aplicação para comunicação com o servidor. Você não precisa acessá-la diretamente, mas ela está disponível caso precise testar endpoints da API.

---

## 🔐 Credenciais de Acesso

O sistema possui três perfis de usuário com diferentes níveis de acesso. Utilize as credenciais abaixo para fazer login:

### Perfil Administrador

O perfil de administrador possui acesso total ao sistema, incluindo gerenciamento de usuários, visualização de todas as chamadas e avaliações, e acesso ao dashboard completo.

**Usuário:** `admin`  
**Senha:** `admin123`  
**Email:** admin@monitoria.com  
**Nome Completo:** Administrador do Sistema

### Perfil Supervisor

O perfil de supervisor pode criar e editar avaliações de chamadas, visualizar performance da equipe e acessar relatórios. Este é o perfil ideal para gestores que monitoram a qualidade do atendimento.

**Usuário:** `supervisor`  
**Senha:** `supervisor123`  
**Email:** supervisor@monitoria.com  
**Nome Completo:** Supervisor da Equipe

### Perfil Operador

O perfil de operador pode visualizar apenas suas próprias chamadas e as avaliações recebidas. Este perfil não pode criar ou editar avaliações.

**Usuário:** `joão.silva`  
**Senha:** `operator123`  
**Email:** joao.silva@monitoria.com  
**Nome Completo:** João Silva

**Outros operadores disponíveis:**
- ana.santos / operator123
- pedro.oliveira / operator123
- carla.souza / operator123
- lucas.ferreira / operator123

---

## 📱 Como Acessar

O processo de acesso ao sistema é simples e direto. Siga os passos abaixo para fazer login e começar a usar a aplicação.

### Passo 1: Abrir o Navegador

Abra seu navegador preferido em qualquer dispositivo conectado à internet. O sistema é compatível com Chrome, Firefox, Safari, Edge e outros navegadores modernos.

### Passo 2: Acessar a URL

Digite ou clique na URL principal do sistema:

**[https://3000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer](https://3000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer)**

Você será automaticamente redirecionado para a página de login.

### Passo 3: Fazer Login

Na tela de login, preencha os campos com as credenciais do perfil desejado. Por exemplo, para acessar como administrador, digite `admin` no campo de usuário e `admin123` no campo de senha.

### Passo 4: Navegar pelo Sistema

Após o login bem-sucedido, você será direcionado ao dashboard principal. Use o menu lateral para navegar entre as diferentes seções do sistema como Dashboard, Chamadas, Avaliações e Usuários.

---

## 🎯 Funcionalidades Disponíveis

O sistema oferece um conjunto completo de funcionalidades para gestão de qualidade de atendimento. Abaixo está um resumo das principais áreas do sistema.

### Dashboard

O dashboard apresenta uma visão geral consolidada com métricas importantes sobre o atendimento. Você encontrará estatísticas como total de chamadas, tempo médio de atendimento, total de avaliações realizadas e nota média geral. Gráficos interativos mostram a distribuição de chamadas por status e prioridade, além de uma tabela com a performance individual de cada operador.

### Chamadas

A seção de chamadas permite visualizar todas as interações registradas no sistema. Você pode filtrar chamadas por status como aberto, em andamento, resolvido ou fechado, além de filtrar por prioridade e categoria. Ao clicar em uma chamada, você acessa os detalhes completos incluindo informações do cliente, operador responsável, descrição do problema e resolução aplicada.

### Avaliações

Na área de avaliações, supervisores e administradores podem criar novas avaliações para chamadas existentes. O sistema utiliza seis critérios de qualidade, cada um pontuado de um a cinco estrelas. Os critérios avaliados são saudação e apresentação, clareza e comunicação, resolução do problema, empatia e cordialidade, seguimento de procedimentos e encerramento adequado. A nota geral é calculada automaticamente como média dos seis critérios.

Além da pontuação, o avaliador deve preencher campos de feedback detalhado incluindo pontos positivos observados no atendimento, pontos que podem ser melhorados e comentários gerais opcionais. É possível marcar se a chamada requer coaching adicional ou se é um atendimento exemplar que pode servir de referência para a equipe.

A listagem de avaliações permite filtrar por chamadas que requerem coaching ou que foram marcadas como exemplares. Cada avaliação pode ser editada ou excluída conforme necessário.

### Usuários (Administradores)

Administradores têm acesso à gestão de usuários do sistema, podendo criar novos usuários, editar informações existentes e desativar contas quando necessário. O sistema implementa soft delete, preservando dados históricos mesmo quando usuários são desativados.

---

## 🔒 Segurança e Boas Práticas

O sistema implementa diversas camadas de segurança para proteger os dados e garantir acesso adequado a cada perfil de usuário.

### Autenticação

A autenticação é realizada através de tokens JWT (JSON Web Tokens) com tempo de expiração configurado. Após o login, você recebe um token de acesso válido por uma hora e um token de atualização válido por trinta dias. O sistema renova automaticamente o token de acesso quando necessário, mantendo sua sessão ativa.

### Controle de Acesso

Cada perfil de usuário possui permissões específicas. Operadores podem visualizar apenas suas próprias chamadas e avaliações. Supervisores podem criar e editar avaliações, além de visualizar dados de toda a equipe. Administradores têm acesso total incluindo gerenciamento de usuários.

### Recomendações de Segurança

Para uso em ambiente de produção real, é altamente recomendado alterar todas as senhas padrão fornecidas neste documento. As credenciais atuais são adequadas para testes e demonstração, mas devem ser substituídas por senhas fortes antes de utilizar o sistema com dados reais.

Senhas fortes devem conter no mínimo oito caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais. Evite usar informações pessoais ou palavras comuns do dicionário.

---

## 💡 Dicas de Uso

Para aproveitar ao máximo o sistema, considere as seguintes recomendações práticas.

### Para Supervisores

Ao avaliar chamadas, seja específico nos campos de feedback. Descreva claramente os pontos positivos observados e as áreas que precisam de melhoria. Isso ajuda os operadores a entenderem exatamente o que devem manter e o que podem aprimorar.

Utilize os filtros de avaliações para identificar rapidamente quais operadores precisam de coaching ou quais atendimentos podem servir de exemplo para treinamentos.

Acompanhe regularmente o dashboard para identificar tendências na qualidade do atendimento e tomar ações preventivas quando necessário.

### Para Operadores

Acesse regularmente suas avaliações para acompanhar seu desempenho. Leia atentamente os feedbacks recebidos e procure implementar as sugestões de melhoria.

Use a seção de chamadas para revisar atendimentos anteriores e identificar padrões que podem ser otimizados.

### Para Administradores

Mantenha os dados de usuários atualizados, especialmente quando houver mudanças de função ou saída de colaboradores.

Monitore o dashboard para ter uma visão estratégica da operação e identificar necessidades de treinamento ou ajustes de processos.

Faça backups regulares do banco de dados para garantir a segurança dos dados históricos.

---

## 🆘 Suporte e Troubleshooting

Caso encontre alguma dificuldade ao acessar ou utilizar o sistema, verifique os pontos abaixo.

### Problemas de Acesso

Se não conseguir acessar a URL do sistema, verifique sua conexão com a internet. Certifique-se de que está digitando a URL corretamente, incluindo o protocolo HTTPS.

Se a página não carregar, tente limpar o cache do navegador ou acessar em modo anônimo/privado. Alguns bloqueadores de anúncios ou extensões de segurança podem interferir no funcionamento da aplicação.

### Problemas de Login

Se receber mensagem de erro ao fazer login, verifique se digitou o usuário e senha corretamente, respeitando maiúsculas e minúsculas. As credenciais são case-sensitive.

Se esqueceu sua senha, entre em contato com o administrador do sistema para redefinição.

### Problemas de Funcionalidade

Se alguma funcionalidade não estiver funcionando como esperado, tente atualizar a página pressionando F5 ou Ctrl+R (Cmd+R no Mac).

Verifique se está usando um navegador atualizado. O sistema foi testado nas versões mais recentes do Chrome, Firefox, Safari e Edge.

---

## 📊 Dados de Demonstração

O sistema foi inicializado com dados de exemplo para facilitar testes e demonstrações. O banco de dados contém sete usuários distribuídos entre os três perfis, cinquenta chamadas registradas nos últimos trinta dias com diferentes status, prioridades e categorias, e trinta avaliações vinculadas às chamadas com pontuações variadas.

Estes dados podem ser utilizados livremente para explorar todas as funcionalidades do sistema. Quando estiver pronto para usar o sistema em produção com dados reais, você pode limpar o banco de dados e começar do zero, ou simplesmente adicionar novos registros mantendo os dados de exemplo como referência.

---

## 📞 Informações Técnicas

Para referência técnica ou troubleshooting avançado, seguem informações sobre a infraestrutura do sistema.

### Componentes em Execução

O sistema é composto por três componentes principais rodando em containers separados. O frontend React está sendo servido na porta 3000 através de um servidor HTTP Python. O backend Flask está rodando na porta 5000 com a API REST. O banco de dados PostgreSQL 14 está ativo e acessível internamente na porta 5432.

### Endpoints da API

A API REST está disponível em `https://5000-i3ow7szw9eztfqes94sc5-873561a6.manusvm.computer/api` e oferece os seguintes grupos de endpoints:

**Autenticação:** `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`  
**Usuários:** `/api/users` (GET, POST, PUT, DELETE)  
**Chamadas:** `/api/calls` (GET, POST, PUT, DELETE)  
**Avaliações:** `/api/evaluations` (GET, POST, PUT, DELETE)  
**Dashboard:** `/api/dashboard/stats`  
**Health Check:** `/api/health`

Todos os endpoints exceto login, register e health check requerem autenticação via token JWT no header Authorization.

---

## ✅ Checklist de Primeiro Acesso

Para garantir que tudo está funcionando corretamente, siga este checklist na primeira vez que acessar o sistema.

1. Acesse a URL principal do frontend no navegador
2. Verifique se a página de login é exibida corretamente
3. Faça login com as credenciais de administrador (admin / admin123)
4. Confirme que o dashboard é carregado com gráficos e estatísticas
5. Navegue até a seção de Chamadas e verifique se a lista é exibida
6. Clique em uma chamada para ver os detalhes completos
7. Acesse a seção de Avaliações e visualize as avaliações existentes
8. Teste criar uma nova avaliação em uma chamada sem avaliação
9. Verifique se consegue editar e excluir avaliações
10. Faça logout e teste login com outro perfil (supervisor ou operador)

Se todos os itens acima funcionarem corretamente, o sistema está pronto para uso!

---

## 📝 Observações Finais

Este sistema foi desenvolvido utilizando tecnologias open source modernas e segue as melhores práticas de desenvolvimento web. A arquitetura é escalável e pode ser facilmente adaptada para atender necessidades específicas da sua organização.

As URLs fornecidas neste documento são temporárias e válidas apenas durante a sessão atual do sandbox. Para uso em produção permanente, será necessário realizar o deploy em um servidor próprio ou serviço de cloud computing seguindo as instruções disponíveis na documentação de deploy.

Toda a documentação técnica completa está disponível na pasta `docs/` do projeto, incluindo guias de instalação, manuais de usuário, referências de API e arquitetura do sistema.

---

**Desenvolvido por:** Manus AI  
**Versão:** 1.0 - MVP Completo  
**Data:** 02 de Novembro de 2025  
**Status:** ✅ Sistema Online e Operacional
