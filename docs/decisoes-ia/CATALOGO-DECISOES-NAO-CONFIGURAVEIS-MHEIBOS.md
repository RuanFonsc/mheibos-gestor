# MHEIBOS GESTOR
# Catálogo de Decisões Não Configuráveis

**Status:** Proposta consolidada para implementação  
**Objetivo:** registrar barreiras que não podem ser flexibilizadas pela empresa, gerente, administrador, usuário, Missão ou pela própria IA através da página de configurações.

---

# 1. Regra central

> **Configuração não pode virar mecanismo para desativar a finalidade protetiva do Mheibos.**

As decisões abaixo não devem possuir toggle, slider, checkbox ou exceção administrativa comum.

Quando uma regra só puder ser alterada por revisão normativa, a interface deve informar isso em vez de oferecer controle.

---

# 2. Autoridade e permissões

## NC-01 — IA nunca ultrapassa as permissões do usuário
A IA herda os limites do usuário autenticado e não possui privilégios próprios.

## NC-02 — Interface não concede permissão
Visibilidade de botão, tela, atalho ou sugestão não cria autoridade para executar a ação.

## NC-03 — Permissão deve ser revalidada na persistência
Ter iniciado uma ação com permissão não garante que ela possa ser salva após perda da autorização.

## NC-04 — IA não revela dados fora do escopo
A IA não pode mostrar, resumir, inferir para exposição ou pré-carregar conteúdo que o usuário não poderia consultar normalmente.

## NC-05 — Ação sensível exige as proteções obrigatórias
Quando a ação for normativamente sensível, reautenticação, identidade e auditoria não podem ser desligadas por preferência.

---

# 3. Segurança e governança

## NC-06 — IA não amplia a própria autoridade
Nenhuma confiança, aprendizado, urgência ou benefício permite à IA conceder a si mesma novas funções.

## NC-07 — Configuração inferior não viola regra superior
Usuário, Missão e empresa operam apenas dentro do espaço permitido pelas regras normativas.

## NC-08 — Políticas fundamentais não são editadas nas Configurações
Mudanças de princípios, políticas obrigatórias e regras fundamentais exigem revisão dos documentos oficiais e implementação correspondente.

## NC-09 — Proteções permanentes não podem ser removidas
Uma política configurável de segurança nunca pode eliminar proteções classificadas como permanentes.

## NC-10 — IA não altera silenciosamente documentos normativos
RFCs, princípios e demais documentos oficiais não são autoconfiguráveis pela IA.

---

# 4. Auditoria, eventos e integridade histórica

## NC-11 — Eventos e evidências obrigatórios não podem ser desligados
Operações que exigem evidência/auditoria continuam registradas independentemente de preferência.

## NC-12 — Auditoria não pode ser reescrita silenciosamente
Nem administrador nem IA podem editar o passado para produzir uma narrativa diferente.

## NC-13 — Reversão não apaga o histórico
Desfazer uma decisão deve gerar novo estado/evento apropriado, não apagar que a decisão anterior existiu.

## NC-14 — Hipótese não substitui fato
A IA não pode transformar inferência em estado operacional oficial sem a transição/validação apropriada.

---

# 5. Processos e operação

## NC-15 — Etapas obrigatórias não podem ser desativadas por configuração
A configuração não pode conceder ao usuário liberdade geral para pular processos que o Mheibos exige.

## NC-16 — Bloqueios determinísticos obrigatórios permanecem soberanos
Confiança da IA não remove bloqueio criado por regra oficial.

## NC-17 — Coleta obrigatória de dados não é preferência
Campos e evidências necessários ao processo, produção, segurança ou integridade não podem ser desligados para “agilizar”.

## NC-18 — Usuário comum não ganha poder de ignorar críticos
As regras já definidas para situações críticas e encaminhamento permanecem obrigatórias.

## NC-19 — IA não transforma conveniência em exceção operacional
Uma prática frequente ou aparentemente eficiente não pode contornar procedimento obrigatório.

---

# 6. Financeiro e comercial

## NC-20 — IA não toma decisão financeira
A IA pode analisar, simular, recomendar e aprender, mas a decisão financeira é humana.

Isso inclui, entre outros:
- movimentar dinheiro;
- aprovar/cancelar/estornar pagamento;
- conceder desconto;
- alterar preço;
- comprar;
- contratar;
- investir;
- assumir compromisso financeiro.

## NC-21 — IA não negocia preço nem prazo
Mesmo em atendimento autônomo, preço e prazo seguem as condições autorizadas. Excepcionalidades exigem humano.

## NC-22 — Simulação não autoriza execução
Resultado financeiro favorável, alta confiança ou reversibilidade não convertem recomendação em decisão.

---

# 7. Atendimento e comunicação externa

## NC-23 — IA nunca responde clientes sem autorização explícita do modo autônomo
A capacidade de atendimento autônomo depende da liberação específica já definida, com autenticação gerencial.

## NC-24 — IA não aprende deliberadamente práticas ruins
Erros, omissões, atalhos humanos e violações de processo podem ser evidências de aprendizado, mas não viram comportamento desejável automaticamente.

## NC-25 — Excepcionalidade comercial relevante vai para humano
Quando o atendimento autônomo encontrar situação fora das condições autorizadas, não cria sua própria exceção.

---

# 8. Conhecimento, memória e aprendizado

## NC-26 — IA não promove conhecimento oficial autonomamente
Observação, padrão, hipótese, ensinamento ou recomendação exigem validação humana autorizada para virar conhecimento oficial destinado a terceiros.

## NC-27 — Persistência não equivale a verdade
Memória longa não pode transformar automaticamente um conteúdo em regra oficial.

## NC-28 — Fonte oficial prevalece segundo autoridade e vigência
Similaridade semântica, repetição ou memória antiga não superam fonte normativa válida.

## NC-29 — Aprendizado não transfere autoridade
Aprender com gerente, financeiro, líder ou especialista não concede à IA os poderes dessa pessoa.

---

# 9. Interface Viva

## NC-30 — Personalização não altera regra de negócio
Adaptação visual não pode remover etapas, permissões, dados obrigatórios, segurança ou processos.

## NC-31 — Interface Viva não executa experimentação arbitrária
A IA não altera a interface apenas para testar hipóteses ou coletar evidência.

## NC-32 — Interface não pode oscilar indefinidamente
Adaptações devem possuir critérios de parada e estabilidade.

## NC-33 — Informação crítica não pode depender só de efeito visual
Falha de destaque, cor ou animação não pode apagar a comunicação essencial.

## NC-34 — Falha da IA não inutiliza a aplicação normal
O sistema determinístico deve continuar operável quando a IA estiver indisponível.

---

# 10. Missões e Teamwork

## NC-35 — Autonomia de Missão não é global
Autorizar autonomia na Missão A não autoriza a Missão B.

## NC-36 — Autonomia de Missão não remove barreiras superiores
Permissões, segurança, financeiro, processos e demais invariantes continuam valendo.

## NC-37 — IA não transfere tarefa atribuída sem consentimento/autoridade aplicável
A autonomia cognitiva não permite redistribuição arbitrária de responsabilidade.

## NC-38 — Missão não substitui processos oficiais
Missão organiza objetivos; não reescreve Pedido, Processo, Etapa ou Pendência.

---

# 11. Offline e sincronização

## NC-39 — Offline é regime emergencial
Não deve existir configuração para transformar o offline em modo normal preferencial de operação.

## NC-40 — IA conversacional permanece suspensa offline
O modelo local não se torna substituto conversacional por configuração.

## NC-41 — IA local não amplia função durante queda da Central
Ela executa somente papéis pequenos, estruturais e previamente designados.

## NC-42 — Sincronização não reescreve silenciosamente a história
Mudança do contexto global não autoriza recalcular retroativamente o que ocorreu legitimamente offline.

---

# 12. Arquivos e produção

## NC-43 — Regras obrigatórias de integridade de arquivos permanecem
Nome, vínculo, rastreabilidade e demais invariantes definidas para arquivos não podem ser desligadas por preferência.

## NC-44 — IA não substitui análise humana de arte quando essa capacidade não foi prevista
Alertar sobre ausência do arquivo correto não autoriza a IA a declarar qualidade técnica/visual que ela não verificou pelo mecanismo apropriado.

---

# 13. Confiança e intervenção

## NC-45 — Confiança não cria autoridade
95%+ pode mudar o tratamento cognitivo previsto, mas nunca supera uma proibição normativa.

## NC-46 — Alertas preventivos cognitivos de possível erro exigem o limiar definido
A página de configurações não deve permitir reduzir o limiar obrigatório estabelecido para esse tipo de intervenção.

## NC-47 — Interrupção proativa exige relevância temporal além de alta confiança
Não pode existir configuração “interromper sempre”.

---

# 14. Administração técnica

## NC-48 — Diagnóstico não autoriza autorreprogramação
A IA pode diagnosticar e propor correções, mas não reescrever autonomamente código, arquitetura ou regras fundamentais em produção.

## NC-49 — Manutenção autônoma só existe para classes previamente autorizadas
A IA não pode decidir no momento que uma ação técnica é segura e, com isso, autorizar-se.

## NC-50 — Configuração não transforma ação proibida em ação silenciosa
“Execução silenciosa” só pode existir para ação que já possua autorização válida.

---

# 15. Regra para implementação

Cada decisão interna deve possuir metadados equivalentes a:

```text
configurability = LOCKED | COMPANY | USER | MISSION
authority_source = RFC / policy / catalog
can_be_disabled = true | false
requires_reauth = true | false
audit_level = ...
```

Para todos os itens deste documento:

```text
configurability = LOCKED
```

A interface pode explicar a regra, mas não deve apresentar um controle que sugira que ela é negociável.
