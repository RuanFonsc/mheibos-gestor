# ENG-0003 — Skill Oficial do Codex

**Status:** COMPLETED_WITH_GAPS  
**Versão:** 1.0  
**Data:** 01/08/2026  
**Responsabilidade exclusiva:** especificar como a Skill `mheibos-engineering` torna executável a governança do Mheibos no Codex.  
**Dependências:** ENG-0000 e ENG-0002.  
**Implementação:** `.agents/skills/mheibos-engineering/`.

---

## 1. Finalidade

A Skill transforma hierarquia, invariantes, gates e estados de parada em um workflow reutilizável. Ela não é fonte de regras de produto; roteia o agente às fontes proprietárias e impede que contexto resumido substitua documentação normativa.

## 2. Descoberta e ativação

A instalação é local ao repositório e versionada em `.agents/skills/mheibos-engineering/`.

Ativação explícita:

```text
Use $mheibos-engineering para planejar e validar esta alteração contra as RFCs.
```

Ativação implícita ocorre em implementação, correção, refatoração, revisão, migração, modelos, banco, processos, eventos, segurança, offline, interface, IA, integrações, RFCs e ENG.

Perguntas casuais sem mudança técnica ou documental ficam fora do escopo.

## 3. Contrato operacional

Ao ativar, a Skill obriga:

1. descobrir fontes;
2. identificar RFC proprietária;
3. separar norma e implementação;
4. extrair invariantes;
5. mapear escopo atual;
6. classificar a mudança;
7. planejar antes de editar;
8. implementar domínio antes da interface;
9. validar autorização, eventos e auditoria;
10. executar testes e gates;
11. atualizar documentação;
12. produzir relatório verificável.

## 4. Progressive disclosure

`SKILL.md` mantém somente o procedimento essencial. Detalhes são carregados sob demanda:

| Referência | Momento de leitura |
|---|---|
| SOURCE-HIERARCHY | fontes divergentes |
| RFC-ROUTING | descoberta e RFC proprietária |
| ENGINEERING-GATES | antes da validação |
| TERMINOLOGY | entidades, estados e nomes |
| MIGRATION-RULES | legado, dados e compatibilidade |
| ENG-SERIES-PLAN | produção/revisão de ENG |
| STOP-CONDITIONS | lacuna, conflito ou risco |
| AGENTS-FULL | regra histórica detalhada não coberta |

Referências permanecem a um nível de profundidade e não substituem a leitura da RFC aplicável.

## 5. Scripts determinísticos

### discover_sources.py

Localiza fontes por nomes tolerantes a versões e espaços, classifica tipos, identifica duplicatas e produz texto ou JSON. É somente leitura e ignora artefatos internos da própria Skill.

### validate_skill.py

Valida frontmatter, nome, descrição, caminhos, referências, scripts, estrutura local, tamanho e duplicação evidente com AGENTS.

### validate_eng_series.py

Verifica numeração, títulos, referências, progresso, duplicações de responsabilidade, decisões pendentes e documentos vazios.

### update_eng_progress.py

Inicializa e atualiza `engineering/ENG-PROGRESS.json` de forma atômica, preserva histórico e aceita somente estados oficiais. Recusa conclusão sem `--validated`.

Todos usam biblioteca padrão e não dependem de internet.

## 6. Workflow de mudanças

Entrada mínima:

- solicitação;
- raiz do repositório;
- fontes descobertas;
- estado Git.

Saída mínima:

- fontes consultadas;
- RFC proprietária;
- classificação;
- plano;
- alterações;
- testes/gates;
- gaps/conflitos;
- relatório final.

Se a tarefa for parcialmente bloqueada, continuar apenas partes independentes e seguras.

## 7. Workflow produce-eng-series

1. carregar plano e progresso;
2. selecionar o menor ENG pendente permitido;
3. impedir segundo documento em progresso;
4. definir responsabilidade exclusiva;
5. produzir e revisar;
6. executar gates;
7. atualizar progresso com validação explícita;
8. avançar somente após conclusão ou bloqueio formal;
9. realizar revisão cruzada final.

O loop termina com todos concluídos ou os restantes formalmente bloqueados.

## 8. Regras comportamentais verificáveis

- Pedido: rejeitar transição operacional modelada somente como novo status; exigir Processo/Etapa.
- Fornecedor terceirizado: rejeitar correlação automática de mensagens; propor registro humano.
- IA e permissão: rejeitar decisão do modelo; exigir autorização determinística.
- Regra permanente sem fonte: registrar `DECISAO_HUMANA_NECESSARIA`.
- Série ENG: produzir somente o próximo documento, validar e persistir progresso.

## 9. Segurança da automação

A Skill não deve:

- modificar RFC automaticamente;
- concluir progresso por geração textual;
- executar ação destrutiva sem alvo confirmado;
- assumir comandos inexistentes;
- instalar-se globalmente;
- desabilitar outras Skills;
- esconder teste não executado.

## 10. Manutenção

Quando RFC mudar:

1. descobrir a versão real;
2. revisar roteamento e invariantes afetados;
3. evitar copiar integralmente a RFC;
4. atualizar referências procedurais;
5. validar Skill e série;
6. repetir cenários;
7. revisar diff;
8. atualizar ENG dependente quando necessário.

## 11. Diagnóstico de carregamento

Se não aparecer:

- abrir Codex na raiz Git;
- confirmar `.agents/skills/mheibos-engineering/SKILL.md`;
- validar frontmatter UTF-8;
- executar `validate_skill.py`;
- conferir `agents/openai.yaml`;
- reiniciar sessão para recarregar catálogo;
- testar invocação explícita.

## 12. Lacunas herdadas

A Skill roteia, mas não resolve RFC-0015/0016 ausentes, drafts pendentes ou o elaboração normativa pendente da RFC-0012. Temas afetados devem parar.

## 13. Relatório de validação

| Gate | Resultado |
|---|---|
| Fonte Normativa | APROVADO COM LACUNAS |
| Arquitetura | APROVADO |
| Domínio | APROVADO |
| Dados | NÃO APLICÁVEL |
| Eventos/Auditoria | APROVADO — progresso rastreável |
| Segurança | APROVADO |
| IA | APROVADO |
| UX | APROVADO |
| Código | APROVADO — scripts invocáveis |
| Testes | APROVADO — validadores e cenários definidos |
| Documentação | APROVADO |
| Revisão Final | APROVADO COM LACUNAS |

**Resultado:** `COMPLETED_WITH_GAPS`.
