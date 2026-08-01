# ENG-0004 — Development Protocol

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** definir o ciclo obrigatório de uma mudança de software no Mheibos, da solicitação à entrega verificável.  
**Dependências:** ENG-0000 e ENG-0003.

---

## 1. Entrada e triagem

Registrar objetivo, comportamento esperado, pessoas e entidades afetadas, dados persistentes, riscos, compatibilidade e critérios de aceitação.

Classificar a solicitação como mudança direta segura, mudança que exige contexto ou mudança estratégica/arriscada. Ambiguidade de baixo risco pode receber hipótese explícita; ambiguidade que cria regra, risco de dados ou arquitetura deve parar.

## 2. Baseline

Antes de editar:

```powershell
git status --short --branch
git diff --stat
```

Preservar alterações preexistentes. Não limpar, sobrescrever ou reverter trabalho alheio.

Executar descoberta documental e registrar RFC proprietária, dependências, Inventário, Diagnóstico, código e testes afetados.

## 3. Análise normativa

Extrair:

- invariantes e proibições;
- permissões e ações sensíveis;
- estados e transições;
- eventos, evidências e auditoria;
- requisitos offline;
- requisitos de interface;
- limites da IA;
- critérios de conformidade da RFC.

Separar `DEVE_EXISTIR` de `EXISTE_HOJE`. Classificar a diferença.

## 4. Mapeamento técnico

Localizar apenas o necessário:

- models e migrations;
- services/use cases;
- views, forms e serializers;
- templates, JavaScript e Electron;
- tarefas e integrações;
- testes e fixtures;
- fontes concorrentes de verdade.

Usar busca por símbolos e chamadas antes de leitura ampla. Excluir `.venv`, `.local-tools`, builds e artefatos.

## 5. Plano de mudança

Definir:

1. fatia mínima coerente;
2. ordem domínio → aplicação → infraestrutura → interface;
3. contratos afetados;
4. estratégia de dados/migração;
5. eventos e auditoria;
6. autorização;
7. compatibilidade e remoção;
8. testes;
9. rollback;
10. documentação.

Mudança persistente sem plano de dados ou mudança sensível sem plano de autorização não pode começar.

## 6. Implementação

### Domínio

Modelar conceitos distintos e regras determinísticas. Não colocar autoridade em template, view, form ou JavaScript.

### Aplicação

Casos de uso coordenam intenção, autorização, domínio, persistência e eventos por contratos explícitos.

### Infraestrutura

Encapsular banco, filas, arquivos, Windows, WhatsApp e serviços externos. Falhas externas devem ser isoladas.

### Interface

Coletar intenção, apresentar estado, ações permitidas, erro e explicação. A interface não decide permissão final nem inventa estado.

### IA

Adicionar somente após fonte operacional confiável. Validar saída estruturada e permissões antes de qualquer efeito.

## 7. Dados e migrations

Toda migration deve:

- ser revisada antes de aplicar;
- preservar identidade e histórico;
- evitar destruição silenciosa;
- prever backfill idempotente;
- validar contagens e invariantes;
- considerar rollback ou compensação;
- separar implantação de remoção quando houver compatibilidade.

Executar:

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py migrate --plan
```

Aplicar `migrate` em ambiente apropriado somente quando autorizado pelo escopo.

## 8. Validação do projeto

Comandos reais atualmente disponíveis:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
npm run electron:gestor
npm run electron:producao
npm run build:backend
npm run dist:suite
```

`manage.py test` é o gate geral Django; testes focados devem precedê-lo quando o escopo permitir. Builds Electron/instaladores são gates condicionais e podem exigir tempo/ambiente adicional.

Os gates Python oficiais são executados por `tools/quality.ps1`: Ruff, mypy, `manage.py check` e `manage.py test`. O `package.json` não é a autoridade destes gates.

## 9. Matriz mínima de testes

Conforme o risco:

- regra de domínio;
- autorização permitida e negada;
- persistência e rollback;
- migration/backfill;
- evento e auditoria;
- idempotência/reprocessamento;
- online/offline;
- falha de IA/integração;
- interface e fluxo principal;
- regressão do comportamento preservado.

Teste legado que contradiz RFC deve ser classificado como correção normativa, não mantido cegamente.

## 10. Revisão

Revisar:

- diff completo e arquivos inesperados;
- duplicação e dependências circulares;
- segredos e dados sensíveis;
- concorrência e transações;
- N+1 e regressões proporcionais ao risco;
- acessibilidade e feedback;
- documentação;
- todos os Quality Gates.

## 11. Entrega

O relatório final registra resultado, fontes, classificação, arquivos, migrations, testes, gates, lacunas, rollback e ações manuais.

Commit e push exigem autorização específica. A conclusão técnica não implica publicação.

## 12. Falha e recuperação

Se teste falhar, corrigir ou registrar bloqueio. Não reduzir a suíte para ocultar falha. Se escopo crescer de forma explosiva, terminar uma fatia segura ou pedir decisão.

Após três repetições sem progresso na mesma causa, registrar bloqueio conforme o mecanismo de trabalho vigente.

## 13. Lacunas herdadas

As lacunas normativas do ENG-0000 permanecem. O antigo GAP-ENG-0004-001 foi encerrado com a adoção do Ruff para lint, mypy/django-stubs para verificação gradual de tipos e `tools/quality.ps1` como comando unificado. A ampliação progressiva da cobertura tipada deve acompanhar novas implementações, sem declarar o legado inteiro como previamente tipado.

## 14. Relatório de validação

| Gate | Resultado |
|---|---|
| Fonte Normativa | APROVADO COM LACUNAS |
| Arquitetura | APROVADO |
| Domínio | APROVADO |
| Dados | APROVADO |
| Eventos/Auditoria | APROVADO |
| Segurança | APROVADO |
| IA | APROVADO |
| UX | APROVADO |
| Código | APROVADO — fluxo e comandos reais |
| Testes | APROVADO COM GAP-ENG-0004-001 |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
