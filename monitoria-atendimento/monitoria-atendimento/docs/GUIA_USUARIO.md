# Guia do Usuário - Sistema de Monitoria de Atendimento

Este guia foi criado para ajudar os usuários finais a utilizarem o Sistema de Monitoria de Atendimento de forma eficiente.

## Acesso ao Sistema

O sistema é 100% web e pode ser acessado através de qualquer navegador moderno (Chrome, Firefox, Edge, Safari) sem necessidade de instalação de programas.

**URL de Acesso:** `http://<endereço-do-servidor>` (fornecido pelo administrador)

## Credenciais Padrão (Ambiente de Demonstração)

Se o sistema foi instalado com dados de exemplo, as seguintes credenciais estão disponíveis:

| Perfil       | Usuário           | Senha        |
|--------------|-------------------|--------------|
| Administrador| admin             | admin123     |
| Supervisor   | supervisor        | supervisor123|
| Operador     | joão.silva        | operator123  |
| Operador     | ana.santos        | operator123  |
| Operador     | pedro.oliveira    | operator123  |

**IMPORTANTE:** Em ambiente de produção, o administrador deve alterar todas as senhas padrão imediatamente.

## Perfis de Usuário

O sistema possui três níveis de acesso:

### 1. Operador
Operadores são os atendentes que realizam as chamadas com os clientes.

**Permissões:**
- Visualizar suas próprias chamadas
- Registrar novas chamadas
- Atualizar status de suas chamadas
- Visualizar suas avaliações recebidas
- Acessar dashboard com suas estatísticas pessoais

### 2. Supervisor
Supervisores são responsáveis por monitorar e avaliar o desempenho dos operadores.

**Permissões:**
- Todas as permissões de operador
- Visualizar chamadas de todos os operadores
- Criar e editar avaliações de qualquer chamada
- Visualizar dashboard com estatísticas de toda a equipe
- Acessar relatórios de performance

### 3. Administrador
Administradores têm controle total sobre o sistema.

**Permissões:**
- Todas as permissões de supervisor
- Gerenciar usuários (criar, editar, desativar)
- Alterar perfis e permissões
- Acesso a todas as configurações do sistema

## Funcionalidades Principais

### Dashboard

O dashboard é a página inicial após o login e apresenta uma visão geral das métricas mais importantes:

- **Total de Chamadas:** Número total de atendimentos no período selecionado
- **Tempo Médio:** Duração média dos atendimentos
- **Total de Avaliações:** Quantidade de avaliações realizadas
- **Nota Média:** Pontuação média das avaliações

**Gráficos Disponíveis:**
- Distribuição de chamadas por status (aberto, em andamento, resolvido, fechado)
- Distribuição de chamadas por prioridade (baixa, média, alta, urgente)
- Tabela de performance dos operadores (apenas para supervisores e admins)

**Filtro de Período:**
Use o seletor no canto superior direito para visualizar dados dos últimos 7, 30 ou 90 dias.

### Gestão de Chamadas

A página de **Chamadas** permite visualizar, filtrar e gerenciar todos os atendimentos.

**Filtros Disponíveis:**
- **Status:** Filtre por aberto, em andamento, resolvido ou fechado
- **Prioridade:** Filtre por baixa, média, alta ou urgente
- **Categoria:** Filtre por tipo de atendimento (suporte, vendas, reclamação, dúvida, cancelamento)

**Informações Exibidas:**
- Protocolo único da chamada
- Nome do cliente
- Assunto
- Operador responsável
- Status atual
- Prioridade
- Data de criação

**Ações:**
- Clique no protocolo para ver detalhes completos da chamada
- Use o botão "Nova Chamada" para registrar um novo atendimento

### Sistema de Avaliação

Supervisores e administradores podem avaliar as chamadas com base em seis critérios:

1. **Saudação e Apresentação** (1-5 pontos)
2. **Clareza e Comunicação** (1-5 pontos)
3. **Resolução do Problema** (1-5 pontos)
4. **Empatia e Cordialidade** (1-5 pontos)
5. **Seguimento de Procedimentos** (1-5 pontos)
6. **Encerramento Adequado** (1-5 pontos)

A **nota geral** é calculada automaticamente como a média dos seis critérios.

**Campos Adicionais:**
- **Pontos Positivos:** Destaque os aspectos bem executados
- **Pontos de Melhoria:** Indique áreas que precisam de atenção
- **Comentários Gerais:** Observações adicionais sobre o atendimento
- **Requer Coaching:** Marque se o operador precisa de treinamento adicional
- **Exemplar:** Marque se o atendimento foi excepcional e pode servir de exemplo

## Navegação

O menu lateral (sidebar) permite acesso rápido às principais seções:

- **Dashboard:** Visão geral e estatísticas
- **Chamadas:** Listagem e gestão de atendimentos
- **Avaliações:** Visualização e criação de avaliações
- **Usuários:** Gerenciamento de usuários (apenas admins)

No canto inferior do menu, você encontra:
- Seu nome e perfil
- Botão de **Sair** para encerrar a sessão

## Dicas de Uso

1. **Mantenha o protocolo:** Sempre anote o protocolo da chamada para referência futura
2. **Atualize o status:** Mantenha o status das chamadas atualizado para facilitar o acompanhamento
3. **Revise as avaliações:** Operadores devem revisar regularmente suas avaliações para identificar oportunidades de melhoria
4. **Use os filtros:** Os filtros facilitam encontrar chamadas específicas rapidamente
5. **Período de análise:** Ajuste o período no dashboard para análises mais precisas

## Suporte

Em caso de dúvidas ou problemas técnicos, entre em contato com o administrador do sistema ou com o departamento de TI da sua organização.
