# Checkpoint IMP-011 — Conhecimento e memória

**Data:** 10/08/2026  
**Estado:** `COMPLETED_WITH_GAPS`  
**Fonte normativa:** RFC-0011, Inventário Oficial INV-073 a INV-084, RFC-0006 e RFC-0007  
**IA:** desligada; nenhuma capacidade deste checkpoint depende de modelo ou provedor externo.

## Capacidade entregue

- Base de conhecimento persistente fora do modelo, com camadas, fonte, autoria, vigência, estado e versão.
- Registro de ensinamento inicia como `PENDENTE`; aprovação exige identidade administrativa e gera evento auditável.
- Busca determinística retorna somente conhecimento aprovado e vigente.
- Memória operacional curta/longa fica vinculada ao operador, aceita expiração, atualiza por chave sem duplicação e é isolada por identidade.
- Recuperação de contexto reúne conhecimento aprovado, memória vigente e contexto atual em uma composição transversal determinística.
- Interface `/aprendizado/conhecimento/` permite registrar e aprovar conteúdo sem depender de IA.

## Quality Gates

| Gate | Resultado | Evidência |
|---|---|---|
| Fonte normativa | `PASS_WITH_GAP` | RFC-0011 e inventário comparados; escopo de governança ampla permanece explícito abaixo. |
| Arquitetura | `PASS` | conhecimento e memória são persistentes, substituíveis e independentes do modelo. |
| Domínio | `PASS_WITH_GAP` | camadas, estados, vigência, memória curta/longa e contexto transversal implementados. |
| Eventos e auditoria | `PASS` | registro, aprovação e gravação/atualização de memória produzem eventos transacionais. |
| Segurança | `PASS_WITH_GAP` | identidade ativa é obrigatória; escopos institucionais finos e retenção completa ficam para governança posterior. |
| Migração | `PASS` | `0002_conhecimento` e `0003_memoriaoperacional`; `makemigrations --check` sem alterações. |
| Testes | `PASS` | 9 testes de `apps.aprendizado`; Django check aprovado; Ruff sem cache aprovado; mypy do escopo aprovado. |
| Interface | `PASS_WITH_GAP` | curadoria web funcional; visualização de memória/contexto e integração no Dashboard pertencem ao IMP-012. |
| IA indisponível | `PASS` | serviços e testes executam integralmente com IA desligada. |

## Lacunas não bloqueantes

1. Conhecimento institucional ainda usa o escopo único da instalação; a RFC-0016 deverá definir governança, proveniência detalhada, revisão e escopos finos antes de qualquer exposição entre instalações.
2. Memória de relacionamento, memória de missão e contexto de conversa ainda serão ligados às entidades próprias quando os contratos de Dashboard/Analytics e governança forem implementados.
3. A avaliação preliminar por IA permanece futura e opcional; nenhum conteúdo é promovido automaticamente.
4. Retenção, arquivamento e revisão temporal ampla ainda exigem política normativa específica.

Essas lacunas não impedem o uso determinístico da base nem o início do IMP-012. Elas não devem ser preenchidas por inferência silenciosa.

## Evidências executadas

```text
manage.py check                                      PASS
manage.py makemigrations --check --dry-run          PASS
manage.py test apps.aprendizado --noinput            9 PASS
ruff check --no-cache (escopo IMP-011)              PASS
mypy (escopo IMP-011)                               PASS
```

## Commit da fatia

Será registrado no commit atômico que contém o modelo, a migração, os serviços, os testes e este checkpoint.
