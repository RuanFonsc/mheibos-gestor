# Workflow da série ENG

O plano normativo é `docs/ENG-SERIES-PLAN.md`. Ele lista ENG-0000 a ENG-0010 e impõe dependência sequencial; ENG-0000 ainda não existe na fotografia inicial. Não tratar dependência como satisfeita.

Usar `engineering/ENG-PROGRESS.json` como estado operacional. Produzir um documento por vez, definir responsabilidade exclusiva, referenciar RFCs, revisar duplicações, executar gates e só então marcar estado. `COMPLETED_WITH_GAPS` exige lacunas; `BLOCKED` exige razão/fontes. Nunca sobrescrever concluído sem revisão deliberada.

Terminar quando todos estiverem concluídos ou todos os restantes bloqueados. Emitir revisão cruzada e relatório de lacunas/conflitos.
