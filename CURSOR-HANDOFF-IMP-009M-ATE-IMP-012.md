# Handoff obrigatório para o Cursor — concluir IMP-009M até IMP-012

## Missão

Continuar a transformação do Mheibos Gestor legado na arquitetura oficial, sem reiniciar o trabalho e sem reinterpretar decisões já tomadas. Concluir, nesta ordem:

1. IMP-009M e a consolidação formal do IMP-009;
2. capacidades restantes do IMP-010;
3. IMP-011;
4. IMP-012, incluindo integralmente o Dashboard, Analytics e Simulação da RFC-0015;
5. auditoria cruzada, disponibilização local, commits atômicos e push.

Não avançar para IMP-013/IMP-014. IA é obrigatória no produto futuro, mas continua sendo a última fase. Nenhum fluxo normal pode parar por ausência de modelo, API ou credencial. Recursos analíticos anteriores à IA devem ter execução determinística/fallback operacional. Lacuna realmente intransponível deve ser registrada e apresentada ao usuário, sem arquitetura inventada.

## Repositório e ambiente autoritativos

- Repositório Git real: `C:\Users\Ruan\Documents\Codex\2026-08-01\entre-no-repositorio-mheibos-gestor-do\mheibos-gestor`
- Branch: `agent/engineering-baseline`
- Remoto: `https://github.com/RuanFonsc/mheibos-gestor.git`
- Dados manuais: `C:\Users\Ruan\Documents\Mheibos Gestor`
- Banco manual: `C:\Users\Ruan\Documents\Mheibos Gestor\manual-test-data\mheibos_manual.sqlite3`
- Pasta manual de artes: `C:\Users\Ruan\Documents\Mheibos Gestor\manual-test-data\artes-oficiais`
- Aplicação local: `http://127.0.0.1:8002`

Nunca inserir segredo, chave de API ou senha no Git, em relatório ou log. Não reutilizar qualquer chave Gemini que tenha aparecido em conversas anteriores.

## Leitura obrigatória antes de editar

Ler integralmente, nesta hierarquia:

1. `AGENTS.md`;
2. `.agents/skills/mheibos-engineering/SKILL.md` e todas as referências que ela exige;
3. `.agents/skills/mheibos-ui-engineering/SKILL.md` para qualquer alteração de interface;
4. `docs/Manifesto-Mheibos.md` e os 20 Princípios Fundamentais;
5. todas as RFCs oficiais existentes, com atenção especial a RFC-0003, 0007, 0008, 0009, 0010, 0011, 0012, 0014 e 0015;
6. `engineering/implementation/IMPLEMENTATION-DECISIONS.md`;
7. `engineering/implementation/IMPLEMENTATION-BACKLOG.md`;
8. `engineering/implementation/IMPLEMENTATION-PROGRESS.md`;
9. `engineering/implementation/IMPLEMENTATION-TEST-MATRIX.md`;
10. `docs/UI-STANDARDS-MHEIBOS.md` e `docs/VISUAL-QUALITY-GATE-MHEIBOS.md`.

Não usar os documentos `ChatGPT-RFC-*` como substitutos das RFCs oficiais. Eles são material histórico, salvo indicação explícita da hierarquia documental.

## Estado Git no momento deste handoff

O último commit remoto confirmado é:

- `2834b6b test(offline): validate two-instance synchronization`

O IMP-008 possui smoke real com duas bases SQLite e HTTP, 170 testes aprovados. Resta apenas o smoke humano do futuro instalador Windows; isso não bloqueia os IMPs seguintes.

Existem alterações **não commitadas** iniciando o IMP-009M. Não descartá-las e não usar reset/checkout destrutivo:

- `apps/arquivos/models.py`
- `apps/arquivos/services.py`
- `apps/arquivos/tests.py`
- `apps/arquivos/migrations/0008_transferencia_arte_provisoria.py`
- `apps/pedidos/views.py`
- `apps/pedidos/urls.py`
- `apps/pedidos/templates/pedidos/detail.html`

Já foi executado:

- migração `arquivos.0008_transferencia_arte_provisoria` no banco manual;
- 40 testes focados de `ArquivoOficialArteTests`: PASS;
- Ruff do escopo modificado: PASS;
- servidor local reiniciado e respondendo HTTP 200.

As alterações ainda não receberam suíte completa, revisão visual, relatório, documentação de progresso, commit ou push.

## IMP-009M — contrato obrigatório

Fonte principal: DEC-IMP-033 e RFC-0014.

Implementação iniciada:

- a criação tenta primeiro a pasta compartilhada oficial;
- indisponibilidade física real cria automaticamente arquivo vazio numa área local controlada pelo Mheibos;
- o mesmo nome oficial é preservado;
- o destino compartilhado pretendido é reservado no registro;
- o detalhe sinaliza `Copia provisoria local` e oferece `Transferir e validar agora`;
- a transferência usa cópia temporária, SHA-256, não sobrescreve colisões e preserva a cópia local até decisão humana;
- após validação, a pessoa escolhe `Mover para copias locais` ou `Remover copia local`;
- remoção antecipada só ocorre depois de provar a integridade do oficial;
- eventos auditáveis são gerados;
- falha causal deve reverter banco e arquivos físicos sem órfãos.

Antes de concluir o IMP-009M:

1. revisar profundamente a compensação entre filesystem e transação, especialmente falha no commit depois de copiar/mover/renomear;
2. garantir que somente a interface do Mheibos cria, transfere, vincula ou restaura uma arte oficial;
3. garantir que o nome do arquivo nunca muda;
4. garantir que arquivo externo semelhante nunca seja adotado automaticamente;
5. testar criação normal, fallback local, dupla indisponibilidade, colisão no destino, corrupção durante cópia, reenvio, permissão negada, auditoria falha, remoção, movimentação e retenção;
6. testar rotas HTTP e mensagens, não apenas os serviços;
7. verificar se a preferência empresarial `retencao_copias_locais_dias` precisa gerar Pendência/alerta determinístico nesta fatia; não criar scheduler fora da RFC proprietária;
8. validar no navegador real em 1366×768, 1440×900, 1536×864 e 1920×1080 a 100%, mais 1366×768 a 125%; executar detector de overflow e capturar estados normal, provisório, transferido, erro e permissão reduzida;
9. remover qualquer dado visual artificial depois das evidências;
10. gerar `engineering/implementation/IMP-009M-VISUAL-VALIDATION.md` e atualizar backlog, progresso e matriz de testes;
11. rodar todos os gates e só então fazer commit/push atômico.

Observação: um teste visual temporário falhou porque o Pedido #2 já estava com arte concluída. A configuração empresarial foi restaurada para `C:\Users\Ruan\Documents\Mheibos Gestor\manual-test-data\artes-oficiais`; confirmar isso antes de novos testes. Não existe registro provisório artificial pendente no banco manual até o momento do handoff.

## Consolidação do IMP-009

Revisar IMP-009A até IMP-009M contra RFC-0014 e DEC-IMP-032/033. Não declarar o IMP-009 integralmente `COMPLETED` se permanecerem lacunas normativas de:

- provedor/credenciais/política de backup;
- semântica do agrupamento/revisão anual;
- retenção automática que dependa de scheduler ainda não proprietário.

Nesses casos, registrar precisamente as fontes consultadas e `DECISAO_HUMANA_NECESSARIA`, sem bloquear IMP-010/011/012 quando a dependência não existir.

## IMP-010 — Missões e Teamwork

O backlog informa IMP-010 `IN_PROGRESS`; descobrir o que já existe antes de codificar. Preservar Processo, Fluxo, Etapa, Pendência e Missão como conceitos distintos. Completar as capacidades e gaps já definidos nos documentos de implementação e na RFC-0010, uma fatia vertical por vez, com:

- domínio e migrations explícitas;
- autorização e autoria;
- eventos/auditoria;
- idempotência e rollback;
- interface integrada, sem módulo duplicado;
- testes de serviço, integração, HTTP e visuais;
- documentação, commit atômico e push por fatia.

Não transformar Missão em um segundo Processo/Pendência e não inserir comportamento cognitivo obrigatório.

## IMP-011 — Conhecimento e Memória

Implementar conforme RFC-0011 depois de concluir o IMP-010:

- conhecimento persistido fora do modelo de IA;
- proveniência, autoria, contexto, validação e versionamento;
- distinção entre fato, hipótese, orientação, aprendizado, erro e solução emergente conforme fontes oficiais;
- autorização para promover/validar conhecimento;
- rastreabilidade até Missão/eventos/fontes;
- funcionamento integral com IA desligada;
- nenhuma ingestão silenciosa de segredo ou dado sensível;
- testes e interface conforme os gates.

## IMP-012 — Dashboard, Analytics e Simulação

Fonte proprietária: `docs/RFC-0015-Dashboard-Analytics-e-Simulacao.md` (confirmar o nome real descoberto no repositório).

Implementar integralmente a RFC-0015, não apenas trocar o visual do dashboard. Derivar uma matriz requisito → código → teste → evidência antes de começar. O dashboard deve refletir a fonte oficial de Processo/Etapa/Pendência/Missão/Conhecimento, não estados legados divergentes.

Exigências mínimas:

- dashboard individual e modular por usuário/função/permissão;
- indicadores explicáveis, com fonte, período, cálculo e contexto;
- análises determinísticas disponíveis sem IA;
- análises cognitivas opcionais, claramente identificadas, sem alterar estados e com fallback;
- simulações persistidas, comparáveis, autorizadas e auditáveis;
- simulação nunca altera a operação real silenciosamente;
- promoção explícita e autorizada de resultado de simulação para Missão quando a RFC permitir;
- estados vazio, parcial, erro, sem permissão, IA desligada e dados extremos;
- UI compacta, sem mosaico decorativo de cards, sem gigantismo e sem overflow;
- testes de cálculo, autorização, isolamento por usuário, auditoria, rollback, HTTP e visual;
- relatório visual completo e evidências nas cinco combinações oficiais.

Se a RFC-0015 depender de capacidade ainda ausente do IMP-010/011, implementar primeiro a dependência correta; não simular dados falsos no dashboard.

## Decisões de interface que devem continuar preservadas

- Vendas é redundante e deve permanecer removido/unificado.
- Produção é uma visão especializada por função do usuário ou Etapa do Pedido.
- Preparação de Arte e Assistência de Impressão são duas funções diferentes; ambas permanecem.
- O cartão do Pedido é compacto mesmo com muitas artes; detalhe mostra caminho e lista completa.
- Arte de referência não integra o ciclo da arte oficial e só muda pela edição do Pedido.
- Cadastro/manutenção de usuários fica somente na página Usuários.
- Perfil lista todas as preferências do usuário, configuráveis ou somente informativas.
- Perfil da Empresa lista todas as preferências empresariais, configuráveis ou informativas.
- Aparência lista apenas escolhas permitidas pelos padrões oficiais.
- IA desligada nunca esconde nem bloqueia funções normais.

## Gates e comandos finais

Para gates locais isolados:

```powershell
$env:MHEIBOS_DB_MODE='sqlite'
$env:SQLITE_DB_NAME=':memory:'
powershell -ExecutionPolicy Bypass -File tools\quality.ps1
```

Também executar:

- `python manage.py makemigrations --check --dry-run` no modo SQLite;
- scripts de auditoria visual exigidos pela Skill de UI;
- testes Node/Electron quando arquivos Electron forem tocados;
- smoke real proporcional ao risco;
- `git diff --check`;
- auditoria de segredos antes do commit.

Após cada fatia concluída:

1. atualizar documentação oficial de implementação;
2. aplicar migrations aditivas ao banco manual somente depois dos testes;
3. reiniciar com segurança somente o servidor identificado da porta 8002;
4. confirmar HTTP 200 e fluxo real;
5. criar commit atômico sem pedir autorização rotineira;
6. fazer push para `origin agent/engineering-baseline`;
7. confirmar worktree limpo e branch sincronizada.

Nunca usar `git reset --hard`, `git checkout --`, apagar dados manuais, matar processos amplos ou sobrescrever alterações existentes. Se a rede do GitHub falhar, preservar o commit e repetir o push.

## Critério de entrega ao Codex/usuário

Entregar um resumo factual contendo:

- commits e pushes;
- estados finais de IMP-009, IMP-010, IMP-011 e IMP-012;
- migrations aplicadas;
- quantidade e resultado dos testes;
- evidências visuais;
- URL disponível;
- lacunas normativas remanescentes e por que não bloqueiam ou bloqueiam;
- worktree e sincronização remota.

Não declarar conclusão a partir de testes estreitos. A conclusão deve ser provada requisito por requisito contra RFCs, decisões e quality gates.
