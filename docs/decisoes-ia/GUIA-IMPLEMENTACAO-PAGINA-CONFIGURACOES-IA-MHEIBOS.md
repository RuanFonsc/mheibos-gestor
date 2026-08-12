# MHEIBOS GESTOR
# Guia de Implementação — Página de Configurações da IA

**Status:** Orientação técnica e de UX para implementação  
**Objetivo:** implementar configurações de IA sem permitir que preferências ultrapassem regras normativas, permissões ou barreiras de segurança.

---

# 1. Resultado esperado

A página deve permitir que usuários autorizados compreendam e configurem **somente as liberdades reais** do Mheibos.

Ela não deve ser uma lista de centenas de decisões internas.

Estrutura recomendada:

```text
Configurações
└── Inteligência Artificial
    ├── Empresa
    ├── Meu uso
    ├── Missões
    ├── Segurança e ações sensíveis
    └── Histórico de alterações
```

A aba `Empresa` aparece somente para quem possuir autoridade adequada.

A aba `Meu uso` contém preferências individuais.

A aba `Missões` lista somente Missões às quais o usuário possui acesso e, para editar autonomia, exige a autoridade aplicável à Missão.

---

# 2. Modelo de precedência

A resolução de política deve ser centralizada.

Nunca espalhar regras de precedência por componentes React, templates ou handlers.

Ordem conceitual:

```text
1. Regra normativa / decisão LOCKED
2. Permissão efetiva do usuário
3. Política/configuração da empresa
4. Configuração específica da Missão
5. Preferência do usuário
6. Adaptação contextual da IA
```

Uma camada inferior só pode **restringir ou escolher dentro do espaço permitido**, nunca ampliar autoridade.

Exemplo:

```text
financeiro_autonomo = proibido normativamente
empresa = "proativo"
missao = "autonomia ligada"
usuario = "modo inteligente"

resultado efetivo:
financeiro_autonomo = FALSE
```

---

# 3. Não usar simples cascata de valores para tudo

Empresa × Missão × Usuário não são uma hierarquia de override universal.

Existem três tipos diferentes de configuração:

## 3.1 Política organizacional
Ex.: sugestões organizacionais, política configurável de sensibilidade.

A empresa define o espaço permitido.

## 3.2 Autorização contextual de Missão
Ex.: autonomia da IA na Missão X.

Vale somente naquele objeto.

## 3.3 Preferência individual
Ex.: modo inteligente/apático, atalhos e adaptações visuais.

Não altera a política organizacional nem a Missão de terceiros.

Portanto, não implementar:

```python
effective = user_value or mission_value or company_value
```

Implementar um **Policy Resolver** que conheça o tipo semântico da configuração.

---

# 4. Modelo de dados recomendado

Evitar dezenas de colunas booleanas dispersas.

Usar catálogo tipado de definições + valores por escopo.

## 4.1 Definição

Exemplo conceitual:

```text
AISettingDefinition
- key
- title
- description
- category
- scope_allowed: COMPANY | USER | MISSION
- value_type
- default_value
- allowed_values
- configurability
- requires_permission
- requires_reauthentication
- requires_council
- audit_level
- reversible
- normative_reference
- version
```

## 4.2 Valores

```text
CompanyAISetting
- company_id
- definition_key
- value
- changed_by
- changed_at
- version

UserAISetting
- user_id
- definition_key
- value
- changed_by
- changed_at
- version

MissionAISetting
- mission_id
- definition_key
- value
- changed_by
- changed_at
- version
```

## 4.3 Histórico imutável

Toda alteração relevante gera evento/histórico:

```text
AISettingChanged
- setting_key
- scope
- scope_id
- old_value
- new_value
- actor
- authentication_context
- reason, quando exigida
- timestamp
- correlation_id
```

Nunca sobrescrever o histórico para “limpar” uma reversão.

---

# 5. Catálogo como código versionado

As definições das configurações devem ser controladas pelo programa, não criadas livremente pela empresa.

Exemplo:

```python
AI_SETTINGS = {
    "ai.proactivity": {
        "scope": "COMPANY",
        "type": "enum",
        "allowed": ["essential", "balanced", "proactive"],
        "default": "balanced",
        "configurability": "COMPANY",
    }
}
```

Benefícios:

- impede criação arbitrária de autoridade;
- permite versionamento;
- facilita testes;
- mantém referências normativas;
- permite migração;
- possibilita bloquear combinações inválidas.

---

# 6. Policy Resolver obrigatório

Toda leitura de comportamento da IA deve passar por um resolvedor central.

Interface e backend devem consultar algo equivalente a:

```text
resolve_ai_policy(
    action,
    user,
    company,
    mission=None,
    context=None
)
```

Saída sugerida:

```text
PolicyDecision
- allowed
- autonomous
- silent_execution
- requires_confirmation
- requires_reauthentication
- effective_setting
- source
- blocked_by
- audit_requirement
```

O resolvedor deve considerar:

1. regra LOCKED;
2. permissão;
3. ação sensível;
4. escopo;
5. política da empresa;
6. autorização de Missão;
7. preferência individual;
8. estado atual;
9. regras de confiança;
10. requisitos de auditoria.

---

# 7. Regra de autonomia por Missão

A autonomia é configurada **por Missão**, não globalmente.

Na página:

```text
Missões
└── Missão #123 — Campanha X
    ├── Autonomia da IA       [Ligada]
    ├── Escopo autorizado     [3 categorias]
    ├── Execução silenciosa   [Ligada]
    └── Intervenções          [Normais]
```

Ao ativar autonomia:

1. verificar autoridade do usuário sobre a Missão;
2. revalidar permissões;
3. mostrar resumo claro do que poderá acontecer;
4. listar apenas categorias realmente autonomizáveis;
5. deixar explícito o que **continua proibido**;
6. autenticar quando a política exigir;
7. registrar a mudança.

Nunca apresentar opção genérica:

> “Dar controle total à IA”.

Texto recomendado:

> “Permitir autonomia nas ações autorizadas desta Missão.”

---

# 8. Defaults

Defaults devem vir do catálogo versionado do Mheibos.

Princípios:

- segurança por padrão;
- comportamento útil sem exigir configuração inicial;
- nenhuma autorização crítica presumida;
- autonomia de Missão desligada por padrão até autorização;
- preferências individuais podem iniciar no padrão oficial;
- ausência de registro significa `usar padrão`, não `false` automaticamente.

Armazenar explicitamente a diferença entre:

```text
DEFAULT
ENABLED
DISABLED
```

quando semanticamente necessário.

---

# 9. UX das configurações

## 9.1 Evitar linguagem técnica

Não mostrar:
- IDs de decisão;
- nomes internos de policy;
- detalhes de modelo;
- prompts;
- thresholds irrelevantes ao usuário.

Mostrar:
- o que muda;
- onde muda;
- quem é afetado;
- o que não muda.

## 9.2 Cada controle deve explicar consequência

Exemplo:

**Modo inteligente**  
“Permite que o Mheibos adapte sua interface individualmente para facilitar seu trabalho. Não altera processos, permissões ou dados obrigatórios.”

## 9.3 Mostrar escopo visualmente

Usar badges/labels consistentes:

- `EMPRESA`
- `SÓ PARA MIM`
- `ESTA MISSÃO`

Não depender apenas de cor.

## 9.4 Separar preferência de segurança

Não misturar numa mesma lista:
- modo inteligente;
- ações sensíveis;
- desligamento geral da IA.

Ações de governança devem ter seção própria e maior peso visual.

---

# 10. Decisões amplas primeiro, específicas depois

Página inicial de IA deve mostrar poucas escolhas amplas.

Exemplo:

```text
Comportamento da IA
[ Iniciativa proativa       Equilibrada ]
[ Sugestões de melhoria     Ligado      ]
[ Relatórios automáticos    Ligado      ]

Minha experiência
[ Modo inteligente          Ligado      ]
[ Facilitações contextuais  Ligado      ]

Avançado >
```

A seção `Avançado` contém decisões específicas.

Não apresentar 30 controles de uma vez.

---

# 11. Configurações LOCKED

Decisões não configuráveis não devem aparecer como controles desabilitados em massa.

Quando relevante para compreensão, mostrar uma seção informativa:

**Proteções permanentes**
- A IA não pode tomar decisões financeiras.
- A IA não ultrapassa suas permissões.
- Auditoria obrigatória não pode ser desligada.

Sem toggles.

Quando o usuário tentar realizar uma alteração incompatível por outro fluxo, o backend deve retornar uma razão normativa clara.

---

# 12. Autenticação e reautenticação

Mudanças comuns de UX não precisam de senha adicional.

Exigir reautenticação quando a regra de segurança classificar a alteração como sensível.

Casos já definidos que merecem tratamento protegido incluem:

- desligamento geral da IA para usuário;
- alterações relevantes de política de segurança;
- outras mudanças classificadas como sensíveis.

Para desligamento da IA na empresa, aplicar o fluxo de governança coletiva já definido, não apenas uma senha simples.

A reautenticação deve confirmar o executor real e ser registrada.

---

# 13. Conselho de gerentes

Quando uma alteração exigir conselho:

1. não aplicar imediatamente;
2. criar solicitação pendente;
3. registrar proponente;
4. coletar as aprovações exigidas;
5. impedir aprovação duplicada pela mesma identidade;
6. revalidar permissões de cada aprovador;
7. aplicar somente após atingir o quórum;
8. registrar o evento final.

A interface deve mostrar:

```text
Alteração pendente
1 de 2 aprovações obtidas
```

e não fingir que a configuração já está ativa.

---

# 14. Auditoria proporcional

Classificar alterações:

## Baixa
Preferência visual individual.
- histórico leve;
- reversível;
- sem reautenticação.

## Média
Mudança de comportamento cognitivo organizacional.
- auditoria completa;
- permissão administrativa.

## Alta
Segurança, desligamento geral, autonomia relevante.
- auditoria reforçada;
- reautenticação;
- justificativa quando exigida;
- conselho quando aplicável.

---

# 15. Reversibilidade

Toda configuração configurável deve possuir estratégia de reversão.

A UI deve oferecer:

- `Restaurar padrão`;
- `Desfazer`, quando apropriado;
- histórico para alterações relevantes.

Reverter gera nova alteração auditável.

Não apagar o registro anterior.

Para rejeições da Interface Viva, permitir que o usuário posteriormente **repermita** a adaptação. A IA não pode repermitir por conta própria.

---

# 16. Validação no backend, nunca só na interface

Toda proteção deve existir no servidor/serviço central.

Nunca confiar em:

- toggle escondido;
- botão desabilitado;
- rota não exibida;
- estado React;
- validação apenas no Cliente.

Fluxo:

```text
UI solicita alteração
       ↓
API valida identidade
       ↓
API valida permissão
       ↓
Policy Resolver valida configurabilidade
       ↓
valida autenticação/conselho
       ↓
valida valor e escopo
       ↓
persiste
       ↓
gera evento
```

---

# 17. Impedir combinações inválidas

O sistema deve validar dependências.

Exemplos:

- `execução silenciosa na Missão = ligada` só pode existir se `autonomia da Missão = ligada`;
- escopo autônomo só pode conter ações marcadas como autonomizáveis;
- usuário não pode habilitar adaptação proibida pela política organizacional, quando houver restrição válida;
- desligar IA não pode desligar mecanismos determinísticos;
- uma configuração não pode habilitar decisão `LOCKED`.

A UI pode prevenir, mas o backend deve garantir.

---

# 18. Explicação da decisão efetiva

Para configurações com herança, a interface deve mostrar a origem do valor.

Exemplo:

```text
Sugestões proativas
Ativo
Origem: Política da empresa
```

Ou:

```text
Autonomia da IA
Desativada
Origem: Esta Missão
```

Quando bloqueada:

```text
Não configurável
Motivo: proteção obrigatória do Mheibos
```

Isso evita que o usuário pense que um toggle “não funciona”.

---

# 19. Cache e propagação

Configurações podem ser cacheadas para desempenho, mas mudanças relevantes devem invalidar o cache imediatamente.

Especial cuidado com:

- permissões;
- desligamento de IA;
- autonomia de Missão;
- política de segurança.

Uma ação iniciada antes da mudança deve ser revalidada no momento de persistir quando a regra exigir.

---

# 20. Offline

A página de configurações não deve permitir alterações de autoridade dependentes da Central durante o modo offline.

Especialmente:

- não ativar autonomia de Missão;
- não alterar política de segurança;
- não desligar/ligar governança organizacional;
- não ampliar permissões.

Preferências visuais puramente locais só poderão ser tratadas offline se a arquitetura oficial explicitamente permitir e houver sincronização segura posterior.

A IA conversacional continua suspensa offline.

---

# 21. Testes obrigatórios

Criar testes de matriz para cada configuração.

## 21.1 Precedência
- LOCKED vence empresa;
- empresa limita Missão;
- Missão não afeta outra Missão;
- usuário não amplia empresa;
- usuário só altera seu escopo.

## 21.2 Permissões
- usuário comum não edita Empresa;
- participante sem autoridade não ativa autonomia da Missão;
- administrador sem permissão específica não ultrapassa regra normativa.

## 21.3 Segurança
- reautenticação exigida quando aplicável;
- conselho exige quórum;
- auditoria criada;
- valor anterior preservado.

## 21.4 Financeiro
Testar explicitamente que nenhuma combinação de configurações produz decisão financeira autônoma.

## 21.5 Interface
Testar que modo inteligente não remove:
- campos obrigatórios;
- bloqueios;
- alertas críticos;
- permissões.

## 21.6 Conhecimento
Testar que nenhuma configuração promove ensinamento automaticamente a conhecimento oficial.

## 21.7 Missões
Testar:
- autonomia A não afeta B;
- desligar autonomia interrompe novas ações autônomas;
- ações já registradas permanecem no histórico.

---

# 22. Quality Gate da página

A implementação só deve ser considerada concluída quando:

- [ ] existem escopos Empresa, Usuário e Missão claramente separados;
- [ ] as 30 opções do catálogo estão mapeadas ou conscientemente agrupadas;
- [ ] decisões LOCKED não podem ser habilitadas por API;
- [ ] existe Policy Resolver central;
- [ ] permissões são revalidadas;
- [ ] ações sensíveis usam reautenticação;
- [ ] conselho é aplicado onde exigido;
- [ ] alterações relevantes são auditadas;
- [ ] reversões preservam histórico;
- [ ] existe `Restaurar padrão`;
- [ ] origem do valor efetivo pode ser explicada;
- [ ] autonomia é isolada por Missão;
- [ ] desligamento de IA não desliga proteções determinísticas;
- [ ] nenhuma configuração concede decisão financeira à IA;
- [ ] nenhuma configuração permite promoção autônoma de conhecimento oficial;
- [ ] nenhuma preferência visual altera processo ou permissão;
- [ ] testes cobrem precedência e combinações inválidas;
- [ ] modo offline não permite ampliação de autoridade.

---

# 23. Regra final

A página de Configurações deve ser construída como uma **interface sobre uma política central**, e não como a própria fonte da política.

> **A UI escolhe entre possibilidades autorizadas. O Policy Resolver determina o que é realmente permitido. As RFCs e regras normativas determinam os limites do Policy Resolver.**

Essa separação é obrigatória para impedir que um novo toggle, bug de interface ou valor de banco transforme uma preferência em autoridade.
