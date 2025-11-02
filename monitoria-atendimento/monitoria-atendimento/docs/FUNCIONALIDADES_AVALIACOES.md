# Funcionalidades de Avaliações - Documentação Técnica

**Data:** 02 de Novembro de 2025  
**Versão:** 1.0  
**Autor:** Manus AI

## Visão Geral

Este documento detalha a implementação completa do sistema de avaliações de chamadas, incluindo componentes, páginas, rotas e fluxos de usuário. O sistema permite que supervisores e administradores avaliem a qualidade dos atendimentos realizados pelos operadores.

## Componentes Implementados

### 1. EvaluationForm (Componente)

**Localização:** `/frontend/src/components/EvaluationForm.jsx`

**Descrição:** Formulário completo para criação e edição de avaliações de chamadas.

**Funcionalidades:**

- **Sistema de Avaliação por Estrelas:** Componente interativo com 6 critérios de avaliação (1-5 estrelas cada)
  - Saudação e Apresentação
  - Clareza e Comunicação
  - Resolução do Problema
  - Empatia e Cordialidade
  - Seguimento de Procedimentos
  - Encerramento Adequado

- **Cálculo Automático:** Nota geral calculada em tempo real como média dos 6 critérios

- **Validações:**
  - Todos os critérios devem ser pontuados
  - Pontos positivos obrigatórios
  - Pontos de melhoria obrigatórios
  - Feedback visual de erros com ícones e mensagens

- **Campos de Feedback:**
  - Pontos Positivos (textarea, obrigatório)
  - Pontos de Melhoria (textarea, obrigatório)
  - Comentários Gerais (textarea, opcional)

- **Classificações Adicionais:**
  - Checkbox "Requer Coaching"
  - Checkbox "Atendimento Exemplar"

- **Estados:**
  - Loading durante submissão
  - Feedback visual de hover nas estrelas
  - Desabilita botões durante submissão

**Props:**
- `callId`: ID da chamada sendo avaliada
- `existingEvaluation`: Dados de avaliação existente (para edição)
- `onSave`: Callback para salvar avaliação
- `onCancel`: Callback para cancelar operação

### 2. Evaluations (Página)

**Localização:** `/frontend/src/pages/Evaluations.jsx`

**Descrição:** Página de listagem e gerenciamento de todas as avaliações.

**Funcionalidades:**

- **Listagem Completa:**
  - Cards com informações resumidas de cada avaliação
  - Nota geral destacada com cores baseadas na pontuação
  - Protocolo da chamada vinculada
  - Nome do operador avaliado
  - Data e hora da avaliação
  - Badges para "Exemplar" e "Requer Coaching"
  - Resumo dos 6 critérios com estrelas

- **Filtros Avançados:**
  - Busca por texto (protocolo, operador)
  - Filtro "Requer Coaching" (Sim/Não/Todos)
  - Filtro "Exemplar" (Sim/Não/Todos)

- **Paginação:**
  - 10 avaliações por página
  - Navegação anterior/próxima
  - Contador de total de registros

- **Ações:**
  - Ver detalhes (redireciona para página da chamada)
  - Editar avaliação
  - Excluir avaliação (com confirmação)

- **Estados:**
  - Loading com spinner
  - Empty state quando não há avaliações
  - Tratamento de erros

**Cores da Nota Geral:**
- Verde: ≥ 4.5
- Azul: ≥ 3.5
- Amarelo: ≥ 2.5
- Vermelho: < 2.5

### 3. CallDetail (Página)

**Localização:** `/frontend/src/pages/CallDetail.jsx`

**Descrição:** Página de detalhes completos de uma chamada com suas avaliações.

**Funcionalidades:**

- **Informações da Chamada:**
  - Protocolo único
  - Status e prioridade (badges coloridos)
  - Cliente e telefone
  - Operador responsável
  - Categoria do atendimento
  - Data de criação e duração
  - Assunto, descrição e resolução

- **Formulário de Avaliação:**
  - Botão "Nova Avaliação" (apenas para supervisores/admins)
  - Formulário inline integrado
  - Modo criação ou edição
  - Cancelamento retorna ao estado anterior

- **Visualização de Avaliações:**
  - Lista de todas as avaliações da chamada
  - Nota geral destacada
  - Nome do avaliador e data
  - Badges de classificação
  - Detalhamento dos 6 critérios
  - Feedback completo (pontos positivos, melhorias, comentários)
  - Botão "Editar" para supervisores/admins

- **Controle de Acesso:**
  - Apenas supervisores e administradores podem criar/editar avaliações
  - Operadores podem visualizar suas avaliações

- **Navegação:**
  - Botão "Voltar" para lista de chamadas
  - Breadcrumb visual

## Rotas Implementadas

### Frontend (React Router)

```javascript
// Listagem de avaliações
/evaluations

// Detalhes da chamada (com avaliações)
/calls/:id
```

### Backend (API)

As seguintes rotas da API são utilizadas:

```
GET    /api/evaluations          # Listar avaliações com filtros
GET    /api/evaluations/:id      # Obter avaliação específica
POST   /api/evaluations          # Criar nova avaliação
PUT    /api/evaluations/:id      # Atualizar avaliação
DELETE /api/evaluations/:id      # Excluir avaliação
GET    /api/calls/:id             # Obter chamada com avaliações
```

## Fluxos de Usuário

### Fluxo 1: Criar Nova Avaliação

1. Supervisor acessa página de chamadas (`/calls`)
2. Clica no protocolo de uma chamada
3. Sistema exibe detalhes da chamada (`/calls/:id`)
4. Supervisor clica em "Nova Avaliação"
5. Formulário de avaliação é exibido inline
6. Supervisor preenche os 6 critérios (estrelas)
7. Preenche pontos positivos e de melhoria
8. Opcionalmente marca checkboxes de classificação
9. Clica em "Salvar Avaliação"
10. Sistema valida campos obrigatórios
11. Se válido, envia para API (`POST /api/evaluations`)
12. Formulário fecha e avaliação aparece na lista
13. Chamada é atualizada com a nova avaliação

### Fluxo 2: Editar Avaliação Existente

1. Supervisor acessa detalhes da chamada ou lista de avaliações
2. Clica em "Editar" na avaliação desejada
3. Formulário é aberto com dados preenchidos
4. Supervisor altera os campos necessários
5. Clica em "Salvar Avaliação"
6. Sistema valida e envia para API (`PUT /api/evaluations/:id`)
7. Avaliação é atualizada na visualização

### Fluxo 3: Visualizar Avaliações

1. Usuário acessa `/evaluations`
2. Sistema carrega lista de avaliações
3. Usuário pode filtrar por coaching ou exemplar
4. Usuário pode buscar por texto
5. Clica em "Ver" para ir aos detalhes da chamada
6. Ou clica em "Editar" para modificar (se tiver permissão)

### Fluxo 4: Excluir Avaliação

1. Supervisor acessa lista de avaliações
2. Clica em "Excluir" na avaliação desejada
3. Sistema exibe confirmação
4. Supervisor confirma exclusão
5. Sistema envia para API (`DELETE /api/evaluations/:id`)
6. Avaliação é removida da lista

## Validações Implementadas

### Frontend

- **Critérios de Avaliação:** Todos os 6 critérios devem ter pontuação (1-5)
- **Pontos Positivos:** Campo obrigatório, não pode estar vazio
- **Pontos de Melhoria:** Campo obrigatório, não pode estar vazio
- **Feedback Visual:** Ícones de alerta e mensagens de erro em vermelho
- **Desabilitação de Botões:** Durante submissão para evitar duplicação

### Backend (API)

- **Autenticação:** Token JWT válido obrigatório
- **Autorização:** Apenas supervisores e admins podem criar/editar
- **Validação de Dados:** Scores entre 1-5, campos obrigatórios
- **Validação de Relacionamento:** call_id deve existir

## Integração com API

### Exemplo de Payload - Criar Avaliação

```json
{
  "call_id": 123,
  "greeting_score": 5,
  "communication_score": 4,
  "problem_resolution_score": 5,
  "empathy_score": 4,
  "procedure_compliance_score": 5,
  "closing_score": 4,
  "positive_points": "Atendimento cordial e eficiente",
  "improvement_points": "Poderia ter oferecido mais opções ao cliente",
  "general_comments": "Bom atendimento no geral",
  "requires_coaching": false,
  "is_exemplary": true
}
```

### Exemplo de Resposta - Avaliação Criada

```json
{
  "id": 456,
  "call_id": 123,
  "evaluator_id": 2,
  "overall_score": 4.5,
  "greeting_score": 5,
  "communication_score": 4,
  "problem_resolution_score": 5,
  "empathy_score": 4,
  "procedure_compliance_score": 5,
  "closing_score": 4,
  "positive_points": "Atendimento cordial e eficiente",
  "improvement_points": "Poderia ter oferecido mais opções ao cliente",
  "general_comments": "Bom atendimento no geral",
  "requires_coaching": false,
  "is_exemplary": true,
  "created_at": "2025-11-02T10:30:00",
  "updated_at": "2025-11-02T10:30:00",
  "evaluator": {
    "id": 2,
    "full_name": "Supervisor Silva"
  },
  "call": {
    "id": 123,
    "protocol": "CALL-2025-001",
    "operator": {
      "id": 5,
      "full_name": "João Silva"
    }
  }
}
```

## Melhorias Futuras Sugeridas

1. **Notificações:** Enviar notificação ao operador quando receber avaliação
2. **Histórico:** Rastrear edições de avaliações (quem editou, quando)
3. **Anexos:** Permitir upload de evidências (prints, gravações)
4. **Comentários:** Sistema de comentários/respostas nas avaliações
5. **Relatórios:** Exportar avaliações em PDF ou Excel
6. **Gráficos:** Visualização de evolução das notas ao longo do tempo
7. **Metas:** Definir metas de pontuação por operador/equipe
8. **Assinatura Digital:** Confirmação de leitura pelo operador

## Testes Recomendados

### Testes Funcionais

- [ ] Criar avaliação com todos os campos válidos
- [ ] Tentar criar avaliação sem preencher critérios (deve mostrar erro)
- [ ] Tentar criar avaliação sem pontos positivos (deve mostrar erro)
- [ ] Editar avaliação existente
- [ ] Excluir avaliação com confirmação
- [ ] Cancelar criação de avaliação
- [ ] Filtrar avaliações por "Requer Coaching"
- [ ] Filtrar avaliações por "Exemplar"
- [ ] Buscar avaliação por protocolo
- [ ] Navegar entre páginas de avaliações
- [ ] Verificar cálculo automático da nota geral
- [ ] Verificar cores da nota geral baseadas na pontuação

### Testes de Permissão

- [ ] Operador não deve ver botão "Nova Avaliação"
- [ ] Operador não deve ver botão "Editar" em avaliações
- [ ] Supervisor deve poder criar e editar avaliações
- [ ] Admin deve poder criar e editar avaliações
- [ ] Usuário não autenticado deve ser redirecionado para login

### Testes de UI/UX

- [ ] Hover nas estrelas deve mostrar preview da pontuação
- [ ] Formulário deve ser responsivo em mobile
- [ ] Loading spinner deve aparecer durante submissão
- [ ] Mensagens de erro devem ser claras e visíveis
- [ ] Badges devem ter cores apropriadas
- [ ] Paginação deve funcionar corretamente

## Conclusão

O sistema de avaliações está completamente implementado e integrado com o backend. Todas as funcionalidades principais estão operacionais, incluindo criação, edição, listagem, filtros e exclusão de avaliações. A interface é intuitiva, responsiva e fornece feedback visual adequado ao usuário.
