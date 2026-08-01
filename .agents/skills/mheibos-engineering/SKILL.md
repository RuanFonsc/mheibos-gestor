---
name: mheibos-engineering
description: >
  Governa desenvolvimento, arquitetura, migração, revisão e documentação do Mheibos.
  Use ao implementar, corrigir, refatorar ou planejar código, modelos, banco, processos,
  eventos, segurança, offline, interface, IA, integrações, RFCs, documentos ENG ou a
  migração do Gestor legado. Não use para perguntas casuais sem mudança técnica ou documental.
---

# Mheibos Engineering

Subordinar mudanças às fontes oficiais. Não usar código atual, IA ou conveniência como autoridade normativa.

## Executar o workflow obrigatório

1. Executar `scripts/discover_sources.py --root <raiz>` e ler `references/RFC-ROUTING.md`.
2. Identificar a RFC proprietária, dependências e decisões do Inventário. Separar arquitetura futura de implementação atual.
3. Extrair invariantes, proibições, permissões, estados, eventos, evidências, auditoria e riscos.
4. Mapear somente o código, testes e documentos afetados.
5. Classificar como `preservar`, `adaptar`, `refatorar`, `reprojetar`, `substituir`, `adicionar`, `descontinuar`, `compatibilidade temporária`, `correção normativa` ou `decisão pendente`.
6. Produzir plano antes de editar. Se faltar decisão, ler `references/STOP-CONDITIONS.md` e bloquear somente a parte afetada.
7. Implementar em fatias: domínio e autorização determinística; persistência; eventos/auditoria; contratos; interface.
8. Validar segurança e dados. Ler `references/ENGINEERING-GATES.md` antes dos testes e gates descobertos.
9. Atualizar documentação sem alterar RFC silenciosamente.
10. Relatar fontes, classificação, arquivos, testes, resultados, lacunas, conflitos e trabalho manual.

Nunca inventar regra de produto. Distinguir hipótese, decisão pendente e fato normativo.

## Aplicar invariantes críticos

- Pedido não substitui Processo; um status único não representa toda a operação.
- Interface não contém autoridade de negócio.
- IA não é fonte da verdade e não substitui validação ou autorização determinística.
- Cliente comercial não é Cliente Mheibos.
- Não correlacionar automaticamente mensagens de fornecedor terceirizado; exigir registro humano explícito.
- Manter a aplicação principal integrada; clientes móveis ou especializados usam contratos da mesma Central.
- Gerar eventos e auditoria para mudanças relevantes; não apagar histórico silenciosamente.
- Dar a toda compatibilidade temporária responsável, limite e plano de remoção.
- RFC prevalece sobre código, testes e comentários atuais.

Ler `references/TERMINOLOGY.md` ao trabalhar com entidades. Ler `references/MIGRATION-RULES.md` para legado, esquema, backfill ou compatibilidade.

## Executar `produce-eng-series`

Ler `references/ENG-SERIES-PLAN.md` e `docs/ENG-SERIES-PLAN.md`. Não presumir que o ENG-0000 exista: o plano o lista como primeiro documento esperado.

1. Descobrir fontes; carregar plano e `engineering/ENG-PROGRESS.json` (criar via script quando ausente).
2. Selecionar somente o próximo ENG pendente com dependências satisfeitas.
3. Definir responsabilidade exclusiva; produzir; revisar contra RFCs, terminologia e duplicações.
4. Executar gates e `scripts/validate_eng_series.py`.
5. Atualizar progresso com `scripts/update_eng_progress.py`; nunca concluir automaticamente.
6. Repetir até todos estarem concluídos ou os restantes formalmente bloqueados.
7. Fazer revisão cruzada final e registrar lacunas/conflitos. Nunca inventar arquitetura.

## Ler referências sob demanda

- `references/SOURCE-HIERARCHY.md`: quando fontes divergirem.
- `references/RFC-ROUTING.md`: em toda descoberta e escolha de RFC.
- `references/ENGINEERING-GATES.md`: antes da validação.
- `references/TERMINOLOGY.md`: para entidades, estados ou nomes.
- `references/MIGRATION-RULES.md`: em legado, dados ou compatibilidade.
- `references/ENG-SERIES-PLAN.md`: ao criar ou revisar ENG.
- `references/STOP-CONDITIONS.md`: diante de lacuna, conflito ou risco.
- `references/AGENTS-FULL.md`: para regras históricas detalhadas.

## Encerrar com evidências

Executar comandos aplicáveis, inspecionar o diff e declarar o que não pôde ser validado. Parar por ausência de fonte, conflito normativo, risco de dados, impossibilidade de validação, escopo explosivo, repetição sem progresso ou decisão humana. Registrar `DECISAO_HUMANA_NECESSARIA`; não improvisar conclusão.

