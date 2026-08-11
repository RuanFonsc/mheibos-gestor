# Guia de Retomada da Implementação do Mheibos Gestor

**Atualizado em:** 11/08/2026  
**Repositório canônico:** `C:\Users\Ruan\Documents\Codex\2026-08-01\entre-no-repositorio-mheibos-gestor-do\mheibos-gestor`  
**Branch:** `agent/engineering-baseline`  
**Último commit publicado:** `4e29716 feat(configuracoes): reorganizar preferencias e estados oficiais`

## Objetivo do programa

Concluir a transformação do Mheibos Gestor legado para a arquitetura oficial definida pelas RFCs e ENGs, preservando funcionamento com IA desligada, rastreabilidade, autorização humana e compatibilidade operacional. A IA cognitiva entra somente na última fase; não se deve bloquear fluxo determinístico por ausência de modelo.

## Estado ao retomar

- IMP-009A–M: `COMPLETED`, incluindo criação oficial vazia, estrutura Ano/Mês/Dia, monitoramento, conclusão humana, restauração crítica, transferência gerencial e criação provisória local.
- IMP-010: `COMPLETED_WITH_GAPS`, Missões e Teamwork persistentes.
- IMP-011: `COMPLETED_WITH_GAPS`, conhecimento, memória e contexto determinísticos sem IA.
- IMP-012: `COMPLETED_WITH_GAPS`, Dashboard, Analytics, evidências, comparação factual e simulações determinísticas.
- Configurações: `COMPLETED_WITH_GAPS`; matriz oficial em `docs/CONFIGURACOES-MATRIZ-OFICIAL.md` e navegação implementada em `apps/catalogo/templates/catalogo/configuracoes.html`.
- IMP-013: `PENDING`; RFC-0016 é Draft 0.1 e falta o documento aprovado **Modelo de Decisões Autônomas da IA**.
- IMP-014: `PENDING`; IA cognitiva final, somente depois da governança aprovada.

## O que foi implementado na última fatia

- Áreas separadas de Configurações: Perfil, Aparência, Operação e alertas, Segurança, Offline, Dashboard, IA, Perfil da Empresa, Usuários e Banco.
- Cadastro/manutenção de usuários permanece fora do Perfil.
- Preferências visuais persistentes: densidade, redução de movimento, intensidade de animação, nível de detalhe e frequência de dicas, além de tema e zoom.
- Estados futuros de Segurança, Offline, Dashboard e IA aparecem como informativos quando ainda não há contrato normativo editável.
- Matriz oficial de escopo, hierarquia, permissões e itens não configuráveis registrada em `docs/CONFIGURACOES-MATRIZ-OFICIAL.md`.

## Próximo objetivo

1. Validar a nova página Configurações no navegador nas resoluções oficiais da norma visual.
2. Corrigir apenas defeitos observados e registrar evidências.
3. Não inventar autonomia, limiares, janelas ou autoridades da IA.
4. Quando o Modelo de Decisões Autônomas da IA estiver aprovado, revisar o impacto e iniciar IMP-013.
5. Depois de IMP-013, implementar IMP-014 como última fase, mantendo todos os fluxos determinísticos operacionais sem IA.

## Procedimento obrigatório de retomada

1. Usar exclusivamente a raiz canônica acima; `C:\Users\Ruan\Documents\Mheibos Gestor` contém snapshots e artefatos.
2. Executar `git status --short --branch` e preservar alterações existentes.
3. Ler `AGENTS.md`, `docs/ENG-SERIES-PLAN.md`, `docs/ENG-QUALITY-GATES.md`, `engineering/IMPLEMENTATION-CANONICAL-STATE.md`, `engineering/implementation/IMPLEMENTATION-PROGRESS.md`, RFCs aplicáveis e a matriz de Configurações.
4. Trabalhar em uma única fatia por vez.
5. Executar Quality Gates, testes, lint, type checking e validação visual proporcional ao risco.
6. Atualizar este guia, o Estado Canônico e o Progresso após cada fatia.
7. Comitar intencionalmente e publicar somente a branch oficial após validação.

## Validação registrada

- Suíte Django completa: **207 testes aprovados** com `MHEIBOS_DB_MODE=sqlite` e `SQLITE_DB_NAME=:memory:` para isolamento local.
- `manage.py check`: aprovado.
- Ruff: aprovado.
- JavaScript (`static/js/gestor_prefs.js`): sintaxe aprovada.
- `git diff --check`: aprovado.

## Restrições que não podem ser esquecidas

- IA desligada não pode impedir pedidos, arquivos, produção, entrega, pendências, dashboard ou configurações determinísticas.
- Arte oficial só pode ser criada ou vinculada pela interface do Mheibos.
- Nome, extensão, caminho oficial e estrutura Ano/Mês/Dia não são preferências livres do usuário.
- Ausência de documentação normativa é lacuna: registrar `DECISAO_HUMANA_NECESSARIA`, não escolher silenciosamente.
- O arquivo `engineering/implementation/IMP-010-VISUAL-VALIDATION-INVALID.md` é histórico não rastreado; não apagar sem decisão explícita.
