# MHEIBOS INTELLIGENT OPERATING SYSTEM

# D11 — Administração, Configuração e Saúde do Sistema
## Inventário de Decisões Cognitivas Candidatas ao Catálogo de Decisões Autônomas

**Status:** Proposta consolidada para revisão e aprovação humana  
**Domínio:** D11 — Administração, Configuração e Saúde do Sistema  
**Natureza:** Inventário de decisões candidatas; não altera nem substitui as RFCs oficiais  
**Base principal:** Manifesto e Princípios Fundamentais; RFCs oficiais de arquitetura, segurança, auditoria, operação offline, Interface Viva, missões, aprendizado e modelo operacional; decisões D01–D10 já consolidadas.

---

# 1. Objetivo

Este documento propõe as decisões do **D11 — Administração, Configuração e Saúde do Sistema**, encerrando a etapa de levantamento dos domínios cognitivos necessária antes da consolidação das configurações de IA do Mheibos.

O D11 trata da atuação da IA sobre:

- diagnóstico de saúde do sistema;
- identificação de problemas técnicos e operacionais;
- investigação de causa provável;
- recomendação de correções;
- manutenção;
- configurações;
- permissões administrativas;
- alterações de comportamento;
- governança das configurações;
- integridade das regras obrigatórias.

O princípio central é:

> **A IA pode compreender, diagnosticar, explicar e propor melhorias para o próprio Mheibos, mas não pode usar essa capacidade para alterar sua própria autoridade, remover proteções ou reescrever as regras fundamentais do sistema.**

---

# 2. Princípios transversais

## 2.1 Configuração não é autoridade normativa

Uma configuração existe apenas dentro do espaço de liberdade previamente autorizado pelo Mheibos.

Nenhuma configuração de:

- empresa;
- usuário;
- missão;
- IA;
- interface;
- operação;

poderá contrariar uma regra superior.

A existência de uma opção configurável não transforma uma regra obrigatória em preferência.

> **O usuário pode configurar liberdade onde o Mheibos permite liberdade; não pode configurar o direito de errar onde o Mheibos exige proteção.**

---

## 2.2 A IA não altera a própria autoridade

A IA não poderá:

- ampliar suas permissões;
- reduzir requisitos de confirmação;
- remover autenticações;
- modificar limiares obrigatórios de segurança;
- tornar configurável algo que é obrigatório;
- conceder a si mesma novas funções;
- alterar regras de governança;
- modificar a hierarquia normativa;
- reinterpretar uma proibição como autorização.

Isso permanece proibido independentemente de:

- confiança;
- benefício previsto;
- reversibilidade;
- urgência;
- aprendizado acumulado;
- solicitação de usuário sem autoridade suficiente.

---

## 2.3 Configurações obedecem escopo

O Mheibos poderá possuir configurações em diferentes escopos, conforme as decisões já estabelecidas:

```text
REGRAS OBRIGATÓRIAS DO MHEIBOS
             ↓
CONFIGURAÇÕES DA EMPRESA
             ↓
CONFIGURAÇÕES POR MISSÃO
             ↓
CONFIGURAÇÕES DO USUÁRIO
```

Essa representação indica escopos de configuração e não autoriza uma camada inferior a violar uma superior.

Algumas opções poderão existir apenas em um desses níveis.

Exemplo já estabelecido:

> **Autonomia relacionada a uma missão é configurada por missão, e não como autorização geral para todas as missões.**

---

# 3. D11-01 — Diagnóstico autônomo de saúde do sistema

A IA poderá analisar sinais técnicos e operacionais disponíveis para identificar possíveis problemas de saúde do Mheibos.

Poderá considerar, conforme arquitetura e permissões:

- falhas registradas;
- erros recorrentes;
- eventos;
- filas;
- sincronização;
- tempos de resposta;
- falhas de integração;
- comportamentos anormais;
- degradações;
- inconsistências;
- resultados de verificações técnicas;
- sinais de problemas operacionais relacionados ao sistema.

A IA poderá:

- detectar anomalias;
- correlacionar sintomas;
- priorizar investigação;
- explicar impacto;
- sugerir verificações;
- recomendar correções.

Quando houver mecanismo determinístico capaz de identificar objetivamente a falha, esse mecanismo continuará sendo preferencial.

> **A IA complementa a observabilidade; não substitui verificações técnicas determinísticas.**

---

# 4. D11-02 — Investigação cognitiva de causa raiz

Quando existir um problema técnico ou operacional no próprio Mheibos, a IA poderá investigar autonomamente suas possíveis causas.

Deverá distinguir:

- sintoma;
- fato observado;
- correlação;
- hipótese;
- causa confirmada;
- confiança.

Poderá relacionar múltiplos eventos e componentes para formular hipóteses de causa raiz.

Quando houver mais de uma explicação plausível, deverá apresentar alternativas compatíveis com as regras gerais de confiança já estabelecidas.

A IA não poderá modificar registros históricos para fazer a hipótese “encaixar”.

> **Diagnosticar não significa reescrever evidências.**

---

# 5. D11-03 — Proposição de correções e melhorias

A IA poderá sugerir correções ou melhorias quando identificar:

- falha;
- risco;
- degradação;
- gargalo;
- inconsistência;
- problema de experiência;
- deficiência operacional;
- oportunidade de simplificação;
- oportunidade de prevenção.

A sugestão poderá incluir:

- problema observado;
- evidências;
- causa provável;
- impacto;
- alternativa recomendada;
- benefício esperado;
- riscos;
- reversibilidade;
- dependências.

Quando a correção pertencer a outro domínio, a execução continuará sujeita às regras daquele domínio.

Exemplos:

- melhoria financeira continua sem decisão financeira autônoma;
- mudança de interface obedece ao D09;
- mudança de processo não pode violar processo obrigatório;
- mudança offline não pode ser executada autonomamente apenas por sugestão da IA;
- alteração de conhecimento oficial exige governança do D10/RFC-0011.

> **A capacidade de propor uma melhoria não concede autoridade para implementá-la.**

---

# 6. D11-04 — Execução autônoma apenas de manutenção técnica previamente autorizada

A IA poderá executar autonomamente ações de manutenção somente quando **o próprio Mheibos tiver definido previamente aquela classe de ação como segura, autorizada e automatizável**.

A autorização deverá ser estrutural, e não inventada pela IA no momento da falha.

Podem existir ações técnicas pequenas, determinísticas, reversíveis e previamente aprovadas para automação.

A IA não poderá concluir:

> “Isto parece seguro, então vou me autorizar a fazer.”

Ações fora do catálogo técnico autorizado deverão permanecer como:

- recomendação;
- solicitação de confirmação;
- encaminhamento ao responsável;
- intervenção técnica humana;

conforme o caso.

A execução automática não poderá alterar:

- regras obrigatórias;
- autoridade;
- permissões;
- segurança;
- evidências;
- auditoria;
- políticas fundamentais.

> **Autonomia técnica existe porque foi previamente autorizada pelo Mheibos, não porque a IA acredita que a ação é segura.**

---

# 7. D11-05 — Configurações amplas e específicas sem explosão de opções

A página de configurações não deverá expor individualmente toda microdecisão cognitiva catalogada.

O Mheibos deverá trabalhar com dois níveis de configuração:

## Decisões amplas

Controles compreensíveis que representam comportamentos gerais permitidos, por exemplo:

- grau de iniciativa da IA;
- intervenções de interface permitidas;
- sugestões proativas;
- autonomia autorizada por missão;
- tipos de notificações cognitivas configuráveis;
- preferências de apresentação.

## Decisões específicas

Exceções ou controles de maior relevância que mereçam configuração própria por possuírem impacto claramente compreensível para o usuário.

O objetivo é evitar uma página com dezenas ou centenas de micropermissões técnicas.

> **O catálogo interno pode ser detalhado; a interface de configuração deve ser humana e administrável.**

As configurações amplas nunca poderão englobar silenciosamente uma autoridade que seja proibida ou que exija autorização específica.

---

# 8. D11-06 — Separação entre configurações da empresa, missão e usuário

Cada configuração deverá possuir escopo explícito.

## Empresa

Configurações que afetam comportamento organizacional permitido e que podem ser definidas pela autoridade administrativa correspondente.

## Missão

Configurações aplicáveis apenas à missão específica.

A autorização de autonomia em uma missão:

- vale apenas para aquela missão;
- não se propaga automaticamente para outras;
- não remove barreiras superiores;
- não altera permissões;
- não elimina restrições de segurança.

## Usuário

Configurações relacionadas principalmente à experiência individual e às liberdades que podem variar sem comprometer:

- processo;
- produção;
- coleta obrigatória de dados;
- segurança;
- auditoria;
- integridade operacional.

Especialmente alterações de Interface Viva poderão possuir caráter individual quando previsto.

> **Personalização individual pode mudar a experiência; não pode mudar as obrigações fundamentais do Mheibos.**

---

# 9. D11-07 — Configurações não podem desativar proteções fundamentais

Determinadas decisões deverão ser classificadas como **não configuráveis**.

Nenhum usuário, gerente, administrador ou configuração da empresa poderá desligá-las quando constituírem regra obrigatória do Mheibos.

Entre as categorias protegidas estão, conforme as decisões e RFCs aplicáveis:

- segurança;
- integridade;
- permissões;
- auditoria obrigatória;
- evidências;
- processos obrigatórios;
- bloqueios fundamentais;
- coleta de dados obrigatórios;
- regras de produção obrigatórias;
- limites absolutos de autoridade da IA;
- proibição de decisão financeira autônoma;
- proibição de promoção autônoma a conhecimento oficial;
- restrições de arquivos;
- preservação histórica;
- regras fundamentais de sincronização;
- outras proteções normativas.

Também não poderá existir configuração que permita à IA ou ao usuário escolher ignorar permanentemente erros que o Mheibos foi projetado para impedir.

> **Configuração não pode virar mecanismo de desativação da finalidade protetiva do Mheibos.**

---

# 10. D11-08 — Mudança de regras obrigatórias somente pela governança normativa

Políticas obrigatórias e regras fundamentais do Mheibos não serão editáveis pela página comum de configurações.

Alterá-las exige revisão dos documentos oficiais e mudança deliberada da implementação correspondente.

Conforme decisão de governança já estabelecida, alterações desse nível não podem ser feitas:

- pela IA;
- por usuário comum;
- por gerente;
- por administrador da empresa;
- por configuração local.

Mudanças nas políticas fundamentais dependem da autoridade normativa superior já definida para o projeto.

A empresa poderá precisar encaminhar a necessidade ao suporte/criador quando a mudança ultrapassar sua autoridade configurável.

> **Configuração altera comportamento permitido; governança normativa altera o que é permitido. São mecanismos diferentes.**

---

# 11. Desligamento e redução da IA

As regras já estabelecidas para desligamento da IA permanecem válidas e não são redefinidas pelo D11.

Em particular:

- desligamento geral da IA para um usuário exige a autoridade/autenticação administrativa já definida;
- desligamento geral para toda a empresa exige a governança coletiva anteriormente estabelecida;
- determinadas funções obrigatórias não podem ser desativadas;
- desligar a interface conversacional ou determinadas funções configuráveis não remove mecanismos determinísticos obrigatórios do Mheibos.

A configuração não deverá induzir o usuário a acreditar que “desligar a IA” significa desligar segurança, processos ou validações estruturais.

---

# 12. Auditoria de alterações de configuração

Mudanças relevantes de configuração deverão ser auditáveis de acordo com seu impacto.

O registro poderá incluir, conforme aplicável:

- configuração alterada;
- valor anterior;
- valor novo;
- escopo;
- usuário responsável;
- autoridade utilizada;
- data/hora;
- autenticação adicional quando exigida;
- missão relacionada, quando aplicável.

A IA não poderá apagar ou ocultar esse histórico para simplificar a experiência.

Configurações puramente visuais e de baixo impacto poderão possuir tratamento proporcional, desde que isso seja compatível com as regras oficiais.

---

# 13. Reversibilidade das configurações

Quando uma configuração for legitimamente configurável, deverá existir caminho claro para:

- consultar o estado atual;
- compreender seu efeito;
- restaurar padrão;
- desfazer alteração quando permitido.

Reversibilidade não significa ausência de auditoria.

Uma configuração pode ser reversível e ainda assim preservar o histórico de que foi alterada.

A página deverá diferenciar:

- **restaurar padrão**;
- **desfazer alteração**;
- **desligar uma função configurável**;
- **tentar alterar uma regra não configurável**.

A última opção não deverá ser oferecida como controle comum.

---

# 14. Diagnóstico não autoriza autorreprogramação

A capacidade da IA de diagnosticar problemas no próprio Mheibos não deverá ser interpretada como autorização para autorreprogramação irrestrita.

A IA poderá:

- produzir diagnóstico;
- formular proposta;
- indicar componente provável;
- gerar orientação técnica;
- colaborar com ferramentas de desenvolvimento quando explicitamente autorizado em contexto apropriado.

Mas o Mheibos em produção não deverá permitir que a IA simplesmente altere seu próprio código, regras fundamentais ou documentos normativos como consequência automática de um diagnóstico.

> **Autoconhecimento operacional não equivale a soberania sobre a própria arquitetura.**

---

# 15. Relação com o futuro Catálogo de Configurações

O D11 estabelece a base para separar posteriormente as decisões do catálogo em três grupos:

```text
CATÁLOGO DE DECISÕES
        │
        ├── configuráveis pela empresa
        │
        ├── configuráveis por missão
        │
        ├── configuráveis pelo usuário
        │
        └── não configuráveis
```

A interface pública não deverá necessariamente espelhar cada item interno individualmente.

Decisões relacionadas poderão ser agrupadas em controles amplos, desde que:

- o efeito seja compreensível;
- nenhuma autoridade proibida seja incluída;
- exceções críticas permaneçam explícitas;
- o escopo seja claro;
- permissões sejam respeitadas.

---

# 16. Regra de precedência

Quando houver conflito entre:

1. preferência do usuário;
2. configuração de missão;
3. configuração da empresa;
4. regra obrigatória;
5. documento normativo superior;

a preferência/configuração inferior nunca poderá invalidar a obrigação superior.

De forma conceitual:

```text
DOCUMENTO / REGRA OBRIGATÓRIA
              ↓
       limites absolutos
              ↓
CONFIGURAÇÃO DA EMPRESA
              ↓
CONFIGURAÇÃO DA MISSÃO
              ↓
CONFIGURAÇÃO DO USUÁRIO
              ↓
ADAPTAÇÃO COGNITIVA DA IA
```

A camada inferior opera apenas dentro do espaço permitido pelas superiores.

---

# 17. Estado deste documento

O D11 é apresentado para **revisão e aprovação humana**, contendo oito decisões propostas:

1. **D11-01** — Diagnóstico autônomo de saúde do sistema;
2. **D11-02** — Investigação cognitiva de causa raiz;
3. **D11-03** — Proposição de correções e melhorias;
4. **D11-04** — Execução autônoma apenas de manutenção técnica previamente autorizada;
5. **D11-05** — Configurações amplas e específicas sem explosão de opções;
6. **D11-06** — Separação entre configurações da empresa, missão e usuário;
7. **D11-07** — Configurações não podem desativar proteções fundamentais;
8. **D11-08** — Mudança de regras obrigatórias somente pela governança normativa.

O domínio estabelece a seguinte fronteira:

> **A IA pode diagnosticar e melhorar sua capacidade de compreender o sistema, mas não pode usar essa compreensão para ampliar sua própria autoridade.**

E, para a futura página de configurações:

> **Nem tudo que a IA sabe fazer precisa virar uma opção; nem tudo que o usuário gostaria de desligar pode ser configurável.**

Após aprovação do D11, o inventário D01–D11 estará suficientemente consolidado para produzir:

1. catálogo enxuto de decisões configuráveis, agrupadas em decisões amplas e específicas;
2. catálogo de decisões não configuráveis;
3. orientação de implementação da página de configurações do Mheibos Gestor.
