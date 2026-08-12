# MHEIBOS GESTOR
# Catálogo de Configurações da IA

**Status:** Proposta consolidada para implementação  
**Escopos:** Empresa, Usuário e Missão  
**Objetivo:** expor um conjunto administrável de escolhas sem transformar cada microdecisão cognitiva em uma configuração.

---

## 1. Princípios

1. Configuração não cria autoridade nova.
2. Toda configuração opera dentro de permissões, regras determinísticas, auditoria e princípios fundamentais.
3. Uma configuração inferior nunca pode flexibilizar uma regra superior.
4. Configurações de usuário tratam principalmente experiência individual.
5. Configurações de missão valem somente para a missão correspondente.
6. Configurações da empresa definem políticas configuráveis da organização.
7. O catálogo interno pode ser detalhado; a página pública deve permanecer simples.
8. O estado `Padrão do Mheibos` deve existir sempre que aplicável.
9. O usuário deve conseguir entender o efeito antes de alterar uma opção.
10. Ausência de uma opção nesta lista não significa que a função possa ser livremente configurada.

---

# 2. Decisões amplas

Estas opções agrupam comportamentos relacionados. Devem aparecer primeiro na interface.

## Empresa

### CFG-A01 — Iniciativa proativa da IA
**Tipo:** escolha  
**Opções sugeridas:** Essencial / Equilibrada / Proativa  
Controla com que frequência a IA apresenta sugestões não obrigatórias. Não reduz alertas, bloqueios ou comunicações obrigatórias.

### CFG-A02 — Assistência preventiva operacional
**Tipo:** liga/desliga  
Permite assistência cognitiva preventiva configurável antes de problemas, respeitando os limiares obrigatórios de confiança e as regras determinísticas.

### CFG-A03 — Sugestões de melhoria organizacional
**Tipo:** liga/desliga  
Permite sugestões proativas sobre eficiência, gargalos, tendências, treinamento, interface, processos e saúde operacional, sem autorizar sua execução.

### CFG-A04 — Análises cognitivas em segundo plano
**Tipo:** liga/desliga  
Permite análises não urgentes e não obrigatórias em segundo plano. Mecanismos obrigatórios de segurança, auditoria e processo permanecem ativos.

### CFG-A05 — Política configurável de ações sensíveis
**Tipo:** entrada para subconfiguração administrativa  
Permite ao administrador configurar categorias adicionais de sensibilidade, perfis, justificativa, alcance e vigência dentro dos limites normativos.

### CFG-A06 — Relatórios e resumos automáticos
**Tipo:** liga/desliga  
Permite geração automática de resumos e relatórios cognitivos não obrigatórios quando houver dados e permissões adequados.

### CFG-A07 — Sugestões de planos de ação
**Tipo:** liga/desliga  
Permite que a IA consolide problemas relacionados e proponha planos de ação. Não cria automaticamente Missão nem altera responsabilidades.

### CFG-A08 — Sugestões de treinamento e melhoria
**Tipo:** liga/desliga  
Permite recomendações de treinamento e melhoria diante de padrões recorrentes. Não autoriza rotular capacidade pessoal.

### CFG-A09 — Análises estratégicas e simulações sob demanda
**Tipo:** liga/desliga para perfis elegíveis  
Permite que usuários autorizados solicitem análises e simulações complexas. Não concede decisão financeira ou administrativa à IA.

### CFG-A10 — Recomendações de saúde do sistema
**Tipo:** liga/desliga  
Permite que diagnósticos cognitivos não críticos do próprio Mheibos gerem recomendações administrativas.

## Usuário

### CFG-A11 — Modo inteligente da interface
**Tipo:** escolha  
**Opções:** Inteligente / Apático  
No modo Inteligente, a Interface Viva pode aplicar adaptações individuais permitidas. No modo Apático, mantém a apresentação padrão e evita adaptações comportamentais opcionais.

### CFG-A12 — Facilitações contextuais
**Tipo:** liga/desliga  
Permite botões flutuantes, atalhos e acessos diretos individuais criados legitimamente pela Interface Viva.

### CFG-A13 — Ajuda contextual pelo painel lateral
**Tipo:** liga/desliga  
Permite que a IA faça perguntas leves sobre o objetivo do usuário e ofereça ajuda contextual no painel lateral.

### CFG-A14 — Sugestões não urgentes no painel lateral
**Tipo:** liga/desliga  
Controla sugestões cognitivas opcionais que podem esperar. Não afeta comunicações obrigatórias.

### CFG-A15 — Resumos pessoais automáticos
**Tipo:** liga/desliga  
Permite resumos pessoais autorizados de trabalho, metas, progresso e contexto acessível ao usuário.

### CFG-A16 — Visualização adaptada por comportamento
**Tipo:** liga/desliga  
Permite reorganizações visuais individuais autorizadas. Deve coexistir com `Visualização padrão`.

## Missão

### CFG-A17 — Autonomia da IA nesta Missão
**Tipo:** liga/desliga  
Autoriza a IA a agir autonomamente **somente dentro da Missão específica** e apenas nas ações que já são autonomizáveis. Não amplia permissões nem remove barreiras de segurança.

### CFG-A18 — Organização autônoma do workspace da Missão
**Tipo:** liga/desliga  
Permite organização contextual, apresentação, agrupamento e manutenção das estruturas autorizadas da Missão.

### CFG-A19 — Sugestões proativas da Missão
**Tipo:** liga/desliga  
Permite sugestões sobre progresso, dependências, ajuda, riscos e próximos passos dentro da Missão.

### CFG-A20 — Resumos automáticos da Missão
**Tipo:** liga/desliga  
Permite gerar e atualizar resumos cognitivos do contexto da Missão sem substituir histórico, eventos ou notas oficiais.

---

# 3. Decisões específicas

Estas opções merecem controle próprio porque possuem efeito claramente compreensível ou exigem autoridade específica.

## Empresa

### CFG-E01 — Limiar de assistência progressiva por recorrência
**Tipo:** número/faixa permitida  
Define o limiar configurável para iniciar assistência progressiva em erros recorrentes. O padrão documental é a terceira ocorrência, salvo regras mais críticas.

### CFG-E02 — Categorias adicionais de ação sensível
**Tipo:** lista administrativa  
Permite incluir ou retirar categorias configuráveis da política de sensibilidade, sem remover ações permanentemente sensíveis.

### CFG-E03 — Exigir justificativa em ações sensíveis adicionais
**Tipo:** liga/desliga por categoria  
Configura justificativa adicional nas categorias em que a política de segurança permite escolha.

### CFG-E04 — Perfis autorizados para categorias sensíveis configuráveis
**Tipo:** matriz de perfis  
Define quais perfis podem executar categorias configuráveis de ações sensíveis. Não concede acesso fora das permissões fundamentais.

### CFG-E05 — Vigência de política configurável de segurança
**Tipo:** período  
Permite que políticas configuráveis tenham início/fim definidos e auditados.

### CFG-E06 — Desligamento geral da IA para a empresa
**Tipo:** ação protegida  
Não é um toggle comum. Exige o fluxo de governança já definido, incluindo conselho de gerentes quando aplicável. Não desliga regras determinísticas e proteções obrigatórias.

## Usuário

### CFG-U01 — Desligamento geral da IA para este usuário
**Tipo:** ação protegida  
Exige autenticação administrativa conforme decisão já estabelecida. Não desativa mecanismos determinísticos obrigatórios.

### CFG-U02 — Restaurar visualização padrão
**Tipo:** ação  
Remove adaptações individuais permitidas e retorna ao estado visual padrão, sem alterar regras de negócio.

### CFG-U03 — Repermitir adaptação anteriormente recusada
**Tipo:** lista de preferências rejeitadas  
Permite ao próprio usuário desfazer uma rejeição persistente anterior. A IA não pode reabrir essa possibilidade sozinha.

### CFG-U04 — Preferência de programa para abrir arquivos de arte
**Tipo:** seletor  
Salva a aplicação preferida do usuário para abrir arquivos quando essa liberdade estiver prevista. Não altera regras de nome, vínculo ou integridade dos arquivos.

## Missão

### CFG-M01 — Escopo de autonomia autorizado nesta Missão
**Tipo:** conjunto limitado de categorias  
Só aparece quando `Autonomia da IA nesta Missão` estiver ativa. Exibe exclusivamente categorias que o catálogo interno classificar como autonomizáveis.

### CFG-M02 — Execução silenciosa de ações já autorizadas na Missão
**Tipo:** liga/desliga  
Permite execução silenciosa somente para ações que já tenham autorização autônoma válida. Não transforma sugestão em autorização.

### CFG-M03 — Intervenções proativas da IA nesta Missão
**Tipo:** escolha  
**Opções sugeridas:** Essenciais / Normais / Ampliadas  
Ajusta intervenções opcionais da Missão sem reduzir alertas obrigatórios ou regras de segurança.

### CFG-M04 — Encerrar autonomia desta Missão
**Tipo:** ação  
Revoga a autorização de autonomia daquela Missão sem afetar outras Missões. Deve ser auditável e não apagar ações já realizadas.

---

# 4. Quantidade e regra de exposição

O catálogo público contém **30 escolhas**:

- 20 decisões amplas;
- 10 decisões específicas;
- distribuídas entre Empresa, Usuário e Missão.

A implementação não deverá aumentar esse número apenas para espelhar microdecisões internas. Novas opções só devem ser adicionadas quando houver necessidade operacional clara e compreensível.

---

# 5. Regra de segurança

Toda opção deste catálogo deverá passar por uma função central de resolução de política antes de ser aplicada.

Conceitualmente:

```text
regra normativa
      ↓
permissão
      ↓
política da empresa
      ↓
configuração da missão
      ↓
preferência do usuário
      ↓
decisão efetiva permitida
```

Se uma camada superior proibir algo, nenhuma configuração inferior poderá habilitá-lo.
