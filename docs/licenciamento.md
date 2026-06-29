# Licenciamento do Mheibos Gestor

O app valida licencas assinadas com Ed25519. A chave privada fica fora do app, e a build final recebe somente a chave publica em `MHEIBOS_LICENSE_PUBLIC_KEY`.

## Opcao gratuita recomendada

Use Cloudflare Workers no plano gratis como central de licencas. O Worker pode receber `license_key` e `machine_id`, consultar uma base simples e devolver uma licenca assinada. A chave privada deve ficar em segredo do Worker, nunca dentro do app desktop.

Alternativas gratuitas:

- Cloudflare Workers + D1/KV: melhor para comecar, nao costuma dormir.
- Supabase free: bom se quiser painel e banco pronto.
- Firebase free: funciona, mas prende mais no ecossistema Google.
- GitHub: bom para releases/update, ruim para central de licenca.

## Variaveis da build final

```env
MHEIBOS_LICENSE_ENFORCED=true
MHEIBOS_LICENSE_PUBLIC_KEY=<chave-publica-base64url>
MHEIBOS_LICENSE_SERVER_URL=https://sua-central.exemplo.workers.dev
MHEIBOS_LICENSE_OFFLINE_DAYS=30
MHEIBOS_INTEGRITY_ENFORCED=true
```

## Gerar chaves

```powershell
python manage.py generate_license_keys
```

Guarde a chave privada fora do repositorio. A chave publica vai para a configuracao da build.

## Emitir licenca offline

```powershell
python manage.py issue_license --private-key C:\seguro\mheibos-private.pem --license-id MHEIBOS-001 --customer "Cliente" --machine <id-da-maquina>
```

O cliente pode colar o `LICENSE_TOKEN` na tela `/licenca/`.

## Integridade dos arquivos

Antes de empacotar a versao final, gere o manifesto:

```powershell
python manage.py build_integrity_manifest
```

Com `MHEIBOS_INTEGRITY_ENFORCED=true`, o app bloqueia se arquivos principais forem alterados depois do manifesto.
