# Guia de atualização do Mheibos Gestor na máquina da gráfica

**Executor:** Google Antigravity  
**Repositório:** `https://github.com/RuanFonsc/mheibos-gestor.git`  
**Branch:** `agent/engineering-baseline`

Este guia atualiza a máquina que ainda usa o Mheibos legado, mantendo banco, artes, webhook e integrações reversíveis. Não instalar por cima da pasta legada, não apagar dados e não executar migração sem backup verificável. Se houver dúvida sobre banco, serviço ou contêiner, interromper antes do corte.

## 1. Diagnóstico e backup

Antes da atualização:

- confirmar janela sem usuários editando;
- identificar pasta do legado, processo/serviço, porta, banco, artes e configuração;
- guardar cópia da pasta legada, `.env`, mídia, artes e configurações dos contêineres;
- fazer backup PostgreSQL com `pg_dump` ou copiar SQLite somente com o servidor parado;
- testar restauração em ambiente separado quando possível.

Não registrar senhas, chaves, tokens ou segredos no relatório.

## 2. Baixar a versão oficial

Usar uma pasta nova e preservar a pasta legada para rollback:

```powershell
git clone https://github.com/RuanFonsc/mheibos-gestor.git mheibos-gestor-atualizado
Set-Location .\mheibos-gestor-atualizado
git fetch origin
git checkout agent/engineering-baseline
git pull --ff-only origin agent/engineering-baseline
git rev-parse HEAD
```

Guardar o commit instalado. Não usar `reset --hard` nem descartar alterações locais.

## 3. Dependências e configuração

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm install
```

Copiar o `.env` antigo somente para a instalação nova e revisar os valores. Para a Central PostgreSQL, confirmar `MHEIBOS_DB_MODE=postgres`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, as variáveis `LEGACY_DB_*`, `MHEIBOS_RUNTIME_ROLE=central` e `MHEIBOS_IA_ENABLED=false`.

Para uma estação offline, manter `client_offline`, `MHEIBOS_STATION_ID`, `MHEIBOS_STATION_SECRET` e `MHEIBOS_CENTRAL_URL` do provisionamento oficial. O segredo deve ficar protegido pelo cofre do Windows.

## 4. Banco legado e migrations

`migrate` aplica o schema Django novo; não é importação automática do legado.

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py migrate --plan
.\.venv\Scripts\python.exe manage.py migrate --noinput
.\.venv\Scripts\python.exe manage.py importar_legado --dry-run
```

Executar `importar_legado` somente após confirmar dry-run, backup e autorização. Nunca apontar SQLite para o PostgreSQL da gráfica.

## 5. Artes e empresa

Confirmar no Perfil da Empresa a pasta compartilhada real das artes oficiais. Ela deve ser acessível pelo servidor e outras instâncias, por UNC ou unidade mapeada. Não mover nem renomear artes durante o corte; restaurações passam pela interface do Mheibos.

Validar leitura/escrita com arquivo temporário fora da pasta oficial e removê-lo depois. Confirmar também `MEDIA_ROOT` e exportações.

## 6. Aprendizado e webhook

O endpoint atual é `http://IP_DA_CENTRAL:8001/webhook`. O teste local é:

```powershell
Invoke-WebRequest http://127.0.0.1:8001/webhook -UseBasicParsing
```

O retorno deve indicar `ok: true` e `modulo: Mheibos Aprendizado`. Depois de iniciar o Gestor em `0.0.0.0:8001`, testar localhost e IP da rede, conferir a Evolution API apontando para `/webhook`, enviar uma mensagem controlada e confirmar sua entrada em Aprendizado.

O template atual referencia `http://host.docker.internal:8001/webhook` quando a Evolution roda em contêiner no mesmo host Windows. Usar esse endereço somente nesse cenário; em outro host, usar o IP alcançável da Central.

## 7. Contêineres

Os nomes reais não podem ser inventados pelo repositório. Inventariar antes de alterar:

```powershell
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
docker compose ls
docker volume ls
```

Registrar nomes, imagens, portas, redes e volumes, sem segredos. Não executar `docker compose down`, `docker system prune`, remoção de volume ou recriação sem backup e autorização. Confirmar que os contêineres da Evolution/Aprendizado continuam ativos e alcançam a porta 8001.

## 8. Inicialização e validação

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate --noinput
.\iniciar_mheibos_servidor_rede.bat
```

Validar `http://127.0.0.1:8001/`, acesso pelo IP e, se necessário, `npm run electron:gestor`. Não manter legado e versão nova escrevendo simultaneamente no mesmo banco.

Testar login, pedidos legados, clientes, financeiro, Preparação de Arte, Produção, Entrega, artes, webhook e uma mensagem de teste do Aprendizado. Confirmar que as funções normais funcionam com IA desligada.

## 9. Rollback

Se qualquer validação crítica falhar: parar a versão nova, preservar logs, restaurar pasta e `.env` legados, restaurar banco somente após confirmar backup e impacto das migrations, restaurar endpoint anterior do webhook, confirmar contêineres/volumes e validar o legado. Não apagar operações novas sem análise; preservar a base nova e os backups até revisão.

## 10. Relatório final

Entregar sem segredos: commit instalado, caminho, banco/modo, migrations e importação, pasta de artes, URL/teste do webhook, contêineres/volumes, validações, backup, resultado `ATUALIZADO`, `ATUALIZADO_COM_LACUNAS` ou `ROLLBACK`, e decisões humanas pendentes.

Se GitHub, banco, webhook ou contêineres não puderem ser confirmados, parar antes do corte e registrar o bloqueio.
