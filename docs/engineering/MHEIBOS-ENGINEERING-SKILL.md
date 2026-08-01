# Skill Mheibos Engineering

A Skill local `mheibos-engineering` governa mudanças técnicas e documentais contra a hierarquia oficial do Mheibos. Está em `.agents/skills/mheibos-engineering/` e é versionável com o repositório.

## Ativação

Invocar explicitamente com `$mheibos-engineering`. A ativação implícita ocorre em implementação, correção, refatoração, revisão, migração, modelos, banco, processos, eventos, segurança, offline, interface, IA, integrações, RFCs e ENG. Perguntas casuais sem mudança não devem ativá-la.

O arquivo `agents/openai.yaml` mantém invocação implícita habilitada. Se a Skill não aparecer, abrir o Codex na raiz, confirmar o caminho e frontmatter, executar o validador e reiniciar a sessão para recarregar o catálogo.

## Estrutura e scripts

`SKILL.md` contém o workflow; `references/` guarda hierarquia, roteamento de RFC, gates, terminologia, migração, série ENG, paradas e o AGENTS integral; `scripts/` oferece descoberta de fontes, validação da Skill/série e atualização segura do progresso.

```powershell
python .agents/skills/mheibos-engineering/scripts/discover_sources.py --root . --format text
python .agents/skills/mheibos-engineering/scripts/discover_sources.py --root . --format json
python .agents/skills/mheibos-engineering/scripts/validate_skill.py --root .
python .agents/skills/mheibos-engineering/scripts/validate_eng_series.py --root .
python .agents/skills/mheibos-engineering/scripts/update_eng_progress.py --root .
```

Atualizações de conclusão exigem `--validated`; estados aceitos: `PENDING`, `IN_PROGRESS`, `COMPLETED`, `COMPLETED_WITH_GAPS` e `BLOCKED`.

## Loop ENG e paradas

`produce-eng-series` lê `docs/ENG-SERIES-PLAN.md`, seleciona apenas o próximo documento permitido, revisa fontes/terminologia/duplicações, executa gates e atualiza progresso. O plano lista ENG-0000 a ENG-0010; a ausência atual do arquivo ENG-0000 é uma dependência real, não licença para inventá-lo ou avançar.

Parar por fonte ausente, conflito, risco de dados, impossibilidade de validação, escopo explosivo, repetição sem progresso ou decisão humana. Registrar a lacuna, sem criar arquitetura.

## Manutenção

Quando uma RFC mudar: atualizar somente referências afetadas, conferir gatilhos/invariantes, executar descoberta e ambos os validadores, repetir cenários comportamentais e revisar o diff. Não copiar toda RFC para a Skill; manter roteamento e regras operacionais concisas.
