# Mheibos Gestor Project Map

Use this file only when project-specific orientation is needed.

## Repository

- Path: `C:\Users\ruan_\Documents\GESTOR\mheibos-gestor`
- GitHub: `https://github.com/RuanFonsc/mheibos-gestor.git`
- Branch: `main`
- Product name: `Mheibos Gestor`

## Stack

- Django 5
- PostgreSQL via `psycopg`
- `python-decouple` for environment settings
- `openpyxl` for spreadsheet import/report workflows
- Static JavaScript in `static/js`
- Django templates in `templates` and app template folders

## Important Paths

- `manage.py`: Django entry point
- `config/settings.py`: project settings
- `config/urls.py`: global URL routes
- `templates/base.html`: global layout
- `templates/home.html`: home/dashboard entry
- `static/js/gestor_prefs.js`: UI preference behavior
- `static/js/gestor_widgets.js`: widget behavior
- `docs/MAPA_MIGRACAO.md`: migration and domain notes

## Apps

- `apps/clientes`: CRM/customer model.
- `apps/pedidos`: orders, items, payments, order views/templates.
- `apps/catalogo`: products/services, UI preferences, operators, assistencia/widget support.
- `apps/financeiro`: financial categories, accounts, entries, reports, dashboard.
- `apps/legacy_migration`: import and normalization from legacy data.

## Migration Direction

- The legacy PyQt app is a source of rules and data, not the target UX.
- Keep Base64 art out of the database; store files under media and keep metadata in Django.
- Normalize text-heavy legacy fields into domain models where practical.
- Financial reports should come from normalized `LancamentoFinanceiro`, not copied spreadsheet logic.
- WhatsApp, AI assistant, printing, PDFs, and advanced integrations should come after core pedidos/clientes/financeiro stability.

## Default Validation

- For model/migration/settings changes: `python manage.py check`
- For database changes: run migrations only after checking `.env` and target database assumptions.
- For template/static UI changes: run the server or inspect with browser when visual risk is meaningful.
- For importers: start with dry runs or small limits.

## Do Not Version

- `.env`
- `.venv`
- `db.sqlite3`
- `media/`
- `staticfiles/`
- logs
- backups, `.rar`, installers, copied legacy folders
