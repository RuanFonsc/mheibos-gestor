# ENG-SERIES-PLAN.md
# Plano Oficial da Série ENG (Engineering)

**Projeto:** Mheibos  
**Status:** Planejamento Oficial  
**Objetivo:** Definir o escopo, a ordem de produção, as dependências e os critérios de conclusão da série ENG.

---

# 1. Missão da Série ENG

A série ENG transforma a arquitetura definida pelos RFCs em um processo oficial de engenharia de software.

Os documentos ENG:

- não criam arquitetura;
- não substituem RFCs;
- não alteram regras de negócio;
- definem como o projeto deve ser desenvolvido, validado, testado e evoluído.

---

# 2. Ordem Oficial de Produção

| Ordem | Documento | Objetivo | Dependências |
|-------:|-----------|----------|--------------|
| 0000 | Programa de Engenharia e Governança | Base normativa da série | Manifesto, RFCs |
| 0001 | Manifesto de Engenharia | Filosofia oficial de engenharia | ENG-0000 |
| 0002 | AGENTS.md | Constituição operacional dos agentes | ENG-0000/0001 |
| 0003 | Skill Oficial do Codex | Workflow reutilizável do Codex | ENG-0000/0002 |
| 0004 | Development Protocol | Processo obrigatório de desenvolvimento | ENG-0000/0003 |
| 0005 | Architecture Guide | Guia de interpretação dos RFCs | RFCs + Inventário |
| 0006 | Implementation Guide | Ordem recomendada de implementação | RFCs + Diagnóstico |
| 0007 | Migration Strategy | Migração do Gestor atual | Diagnóstico + RFCs |
| 0008 | Architectural Checklist | Checklist obrigatório de revisão | Todos anteriores |
| 0009 | Code Review Guide | Revisão técnica oficial | ENG-0004/0008 |
| 0010 | Glossário Oficial | Terminologia oficial do projeto | Todos os RFCs |

---

# 3. Dependências

## Base normativa

- Manifesto
- RFC-0001
- Todas as RFCs aprovadas
- Inventário Oficial
- Diagnóstico da implementação atual

## Base de engenharia

Cada ENG depende dos anteriores.

Nenhum documento pode contradizer um documento anterior sem decisão formal.

---

# 4. Critério de Conclusão

Cada documento somente será considerado concluído quando:

- possuir responsabilidade exclusiva;
- não duplicar outro ENG;
- referenciar as RFCs relevantes;
- passar pelos quality gates;
- possuir revisão cruzada;
- possuir rastreabilidade documental.

---

# 5. Loop Oficial

Para cada documento:

1. Descobrir fontes.
2. Identificar RFCs.
3. Extrair decisões.
4. Produzir estrutura.
5. Escrever primeira versão.
6. Revisar contra RFCs.
7. Revisar terminologia.
8. Revisar duplicações.
9. Executar quality gates.
10. Atualizar ENG-PROGRESS.
11. Avançar para o próximo.

---

# 6. Estados

- PENDING
- IN_PROGRESS
- COMPLETED
- COMPLETED_WITH_GAPS
- BLOCKED

---

# 7. Critérios de Bloqueio

O documento deverá ser interrompido quando houver:

- conflito entre RFCs;
- ausência de decisão normativa;
- risco de criar arquitetura nova;
- dependência de documento ainda inexistente.

---

# 8. Resultado Esperado

Ao final da série ENG, qualquer engenheiro ou agente de IA deverá ser capaz de:

- compreender a arquitetura do Mheibos;
- localizar rapidamente a documentação correta;
- implementar funcionalidades respeitando os RFCs;
- revisar código com critérios uniformes;
- migrar o sistema legado com segurança;
- produzir documentação consistente;
- evoluir o projeto preservando sua coerência arquitetural.