from django.apps import AppConfig


class LegacyMigrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.legacy_migration"
    verbose_name = "Migracao do legado"
