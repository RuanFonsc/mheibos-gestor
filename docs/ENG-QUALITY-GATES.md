# ENG-QUALITY-GATES.md
## Quality Gates Oficiais da Engenharia do Mheibos

**Status:** Normativo  
**Objetivo:** Definir os critérios obrigatórios que toda implementação, refatoração, migração ou documento ENG deve satisfazer antes de ser considerado concluído.

---

# Regra Geral

Nenhuma tarefa pode ser marcada como `COMPLETED` enquanto existir um *Quality Gate* obrigatório reprovado.

Os gates são cumulativos.

---

# GATE 01 — Fonte Normativa

Verificar:

- [ ] A RFC proprietária foi identificada.
- [ ] As RFCs relacionadas foram consultadas.
- [ ] O Inventário Oficial foi considerado.
- [ ] O Diagnóstico foi usado apenas como descrição do estado atual.
- [ ] Nenhuma regra foi inventada.

Reprovação automática:

- arquitetura criada sem fonte;
- decisão baseada apenas no código existente.

---

# GATE 02 — Arquitetura

Verificar:

- [ ] A solução respeita os princípios do Manifesto.
- [ ] Não contradiz nenhuma RFC.
- [ ] Não cria nova arquitetura.
- [ ] Preserva separação entre Domínio, Aplicação, Infraestrutura e Interface.
- [ ] Mantém Pedido, Processo, Fluxo, Etapa, Evento e Evidência como conceitos distintos.

---

# GATE 03 — Domínio

Verificar:

- [ ] Regras de negócio permanecem no domínio.
- [ ] Interface não contém autoridade de negócio.
- [ ] Casos de uso permanecem explícitos.
- [ ] Responsabilidades estão claramente definidas.

---

# GATE 04 — Dados

Verificar:

- [ ] Não há perda de dados.
- [ ] Migrações preservam histórico.
- [ ] Identidades permanecem estáveis.
- [ ] Compatibilidade temporária possui plano de remoção.

---

# GATE 05 — Eventos e Auditoria

Verificar:

- [ ] Eventos relevantes são produzidos.
- [ ] Auditoria registra autoria e contexto.
- [ ] Alterações críticas permanecem rastreáveis.
- [ ] Não existe exclusão silenciosa.

---

# GATE 06 — Segurança

Verificar:

- [ ] Permissões validadas fora da interface.
- [ ] A IA herda permissões do usuário.
- [ ] Operações sensíveis possuem proteção.
- [ ] Não há escalonamento indevido de privilégios.

---

# GATE 07 — Inteligência Artificial

Verificar:

- [ ] IA não é fonte da verdade.
- [ ] IA não substitui regras determinísticas.
- [ ] Sugestões exigem validação quando necessário.
- [ ] O sistema continua funcionando sem IA.

---

# GATE 08 — UX

Verificar:

- [ ] A alteração reduz carga cognitiva.
- [ ] O usuário não precisa decorar etapas.
- [ ] O fluxo acompanha a operação real.
- [ ] Não foram criadas barreiras artificiais entre módulos.

---

# GATE 09 — Código

Verificar:

- [ ] Não há duplicação desnecessária.
- [ ] O código é legível.
- [ ] Existem testes proporcionais ao risco.
- [ ] Não existem dependências circulares novas.

---

# GATE 10 — Testes

Verificar:

- [ ] Testes executados.
- [ ] Testes aprovados.
- [ ] Migrações verificadas.
- [ ] Casos de erro considerados.

---

# GATE 11 — Documentação

Verificar:

- [ ] Documentação atualizada.
- [ ] Arquivos ENG atualizados quando necessário.
- [ ] Mudanças rastreáveis.
- [ ] Relatório final produzido.

---

# GATE 12 — Revisão Final

Antes de concluir confirmar:

- [ ] Nenhuma RFC foi contrariada.
- [ ] Nenhum conceito foi confundido.
- [ ] Nenhuma lacuna foi escondida.
- [ ] Nenhuma decisão arquitetural foi tomada sem autorização.
- [ ] Todos os gates anteriores estão aprovados.

---

# Resultado

## COMPLETED

Todos os gates aprovados.

## COMPLETED_WITH_GAPS

Todos os gates críticos aprovados, mas existem lacunas documentadas que dependem de decisão humana.

## BLOCKED

Existe pelo menos um gate crítico reprovado ou uma decisão normativa ausente.

---

# Gates Críticos

Os seguintes gates nunca podem ser ignorados:

- GATE 01 — Fonte Normativa
- GATE 02 — Arquitetura
- GATE 03 — Domínio
- GATE 05 — Eventos e Auditoria
- GATE 06 — Segurança
- GATE 10 — Testes

Se qualquer um deles falhar, o trabalho deve permanecer bloqueado até correção ou decisão formal.