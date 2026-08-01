# AGENTS.md — Constituição operacional resumida do Mheibos

**Escopo:** todo o repositório. **Idioma:** português do Brasil.

Para implementação, correção, refatoração, revisão, planejamento, migração, modelos, banco, processos, eventos, segurança, offline, interface, IA, integrações, RFCs ou ENG, ativar obrigatoriamente `$mheibos-engineering` em `.agents/skills/mheibos-engineering/`. O procedimento integral e a versão histórica estão na Skill.

## Hierarquia das fontes

1. RFC-0000 e RFC-0001.
2. RFCs normativas.
3. Inventário Oficial, regras e contexto oficiais.
4. ENG e ADRs aprovados.
5. Diagnóstico e relatório funcional.
6. Código, testes, comentários e inferências.

RFC define o futuro; diagnóstico/código descrevem o presente; ENG planeja a transição. Fonte inferior não revoga superior. Conflito exige registro e parada da parte afetada.

## Invariantes e proibições

- Pedido não substitui Processo; um status único não representa toda a operação.
- Domínio e autorização determinística precedem persistência e interface.
- IA não é fonte da verdade, não autoriza e não substitui validações determinísticas.
- Cliente comercial não é Cliente Mheibos.
- Não correlacionar automaticamente mensagens de fornecedores terceirizados; exigir registro humano.
- A aplicação principal é integrada; clientes especializados usam a mesma Central.
- Mudanças relevantes geram eventos/auditoria; histórico não é apagado silenciosamente.
- Compatibilidade temporária exige plano de remoção.
- Código atual nunca prevalece sobre RFC. Não inventar regra de produto nem alterar RFC silenciosamente.

## Validação essencial

Descobrir os comandos reais. Executar testes aplicáveis, lint, type checking, checks de framework/migração, validações de segurança, eventos/auditoria e inspeção do diff. O baseline oficial executa `tools/quality.ps1`, reunindo lint, type checking, checks Django e testes.

```powershell
python .agents/skills/mheibos-engineering/scripts/validate_skill.py --root .
python .agents/skills/mheibos-engineering/scripts/validate_eng_series.py --root .
```

## Parada obrigatória

Parar a parte afetada por ausência de fonte, conflito, risco de dados, validação impossível, escopo explosivo, repetição sem progresso ou decisão humana. Registrar `DECISAO_HUMANA_NECESSARIA`; continuar somente partes independentes e seguras.

A IA é parte obrigatória da arquitetura final, porém sua implementação pertence à última fase. Sua ausência durante as fases anteriores não é condição de parada: implementar desde já os contratos, pontos de extensão, dados e fluxos correspondentes, com execução determinística ou humana enquanto a IA estiver desligada. Nenhum processo operacional nem o restante do desenvolvimento pode parar, bloquear ou depender da instalação de modelo local ou integração por API. Somente uma lacuna lógica realmente incontornável, após esgotar as fontes e alternativas determinísticas ou humanas, autoriza interromper a parte afetada, registrar `DECISAO_HUMANA_NECESSARIA` e perguntar ao responsável humano como prosseguir.

## Operação existente do repositório

Before working on this repository, check whether the project skill is installed:

- Project copy: `.codex/skills/mheibos-gestor-senior`
- Local install target on Windows: `$env:USERPROFILE\.codex\skills\mheibos-gestor-senior`

Derive the local target from the current Windows user instead of hardcoding a user profile:

```powershell
$projectSkill = ".\.codex\skills\mheibos-gestor-senior"
$localSkill = Join-Path $env:USERPROFILE ".codex\skills\mheibos-gestor-senior"
```

If the local skill is missing or older than the project copy, copy/install it to `$localSkill` before doing broad analysis. Use the skill's rules for token economy, intent translation, Git-first workflow, and senior technical intervention.

When the user uses approximate technical language, translate it into the likely product/workflow intent before searching literal terms.

## Quick server startup

When the user asks to "subir o servidor", use this path before broader discovery:

1. Start with the project skill rule:
   ```powershell
   git status --short --branch
   git diff --stat
   ```
2. Check whether port `8001` is free:
   ```powershell
   Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
   ```
3. Apply/check migrations with the project virtualenv:
   ```powershell
   $env:DJANGO_DEBUG='True'
   $env:DJANGO_ALLOWED_HOSTS='*'
   .\.venv\Scripts\python.exe manage.py migrate
   ```
4. Start the LAN server on port `8001`:
   ```powershell
   $env:DJANGO_DEBUG='True'
   $env:DJANGO_ALLOWED_HOSTS='*'
   $env:PYTHONUNBUFFERED='1'
   .\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8001 --noreload
   ```
   If the user needs the shell back, start it hidden with `Start-Process`, redirect logs under `.codex/runlogs/`, and keep `.codex/runlogs/` out of Git.
5. Validate before reporting success:
   ```powershell
   Invoke-WebRequest -Uri 'http://127.0.0.1:8001/' -UseBasicParsing -TimeoutSec 10
   Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.PrefixOrigin -ne 'WellKnown' }
   ```

Report the local URL `http://127.0.0.1:8001/` and the LAN URL using the active Ethernet/Wi-Fi IPv4, usually `http://IP_DO_SERVIDOR:8001/`.
