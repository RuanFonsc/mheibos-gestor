import sys
from pathlib import Path

from decouple import Csv, config


BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
DATA_DIR = Path(config("MHEIBOS_DATA_DIR", default=str(BASE_DIR))).resolve()

SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-only-change-me")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.clientes",
    "apps.catalogo",
    "apps.pedidos",
    "apps.vendas",
    "apps.financeiro",
    "apps.aprendizado",
    "apps.auditoria",
    "apps.operacao",
    "apps.pendencias",
    "apps.cognicao",
    "apps.legacy_migration",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "config.middleware.IntegridadeArquivosMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "config.middleware.LicencaMiddleware",
    "config.middleware.PrimeiroAdminMiddleware",
    "config.middleware.OperadorLoginMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [RESOURCE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.preferencias_ui",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

if config("MHEIBOS_DB_MODE", default="postgres").lower() == "sqlite":
    sqlite_name = config("SQLITE_DB_NAME", default="mheibos_gestor.sqlite3")
    if sqlite_name == ":memory:":
        sqlite_path = sqlite_name
    else:
        if not sqlite_name.lower().endswith((".sqlite", ".sqlite3", ".db")):
            sqlite_name = f"{sqlite_name}.sqlite3"
        sqlite_path = str(DATA_DIR / sqlite_name)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": sqlite_path,
        },
        "legacy": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": sqlite_path,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="gestor_web"),
            "USER": config("DB_USER", default="postgres"),
            "PASSWORD": config("DB_PASSWORD", default="123456"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        },
        "legacy": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("LEGACY_DB_NAME", default=config("DB_NAME", default="gestor_web")),
            "USER": config("LEGACY_DB_USER", default=config("DB_USER", default="postgres")),
            "PASSWORD": config("LEGACY_DB_PASSWORD", default=config("DB_PASSWORD", default="123456")),
            "HOST": config("LEGACY_DB_HOST", default=config("DB_HOST", default="localhost")),
            "PORT": config("LEGACY_DB_PORT", default=config("DB_PORT", default="5432")),
        },
    }

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = DATA_DIR / "staticfiles"
STATICFILES_DIRS = [RESOURCE_DIR / "static"]
MEDIA_URL = "media/"
MEDIA_ROOT = DATA_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MHEIBOS_APP_VERSION = config("MHEIBOS_APP_VERSION", default="dev")
MHEIBOS_LICENSE_ENFORCED = config("MHEIBOS_LICENSE_ENFORCED", default=False, cast=bool)
MHEIBOS_LICENSE_PUBLIC_KEY = config("MHEIBOS_LICENSE_PUBLIC_KEY", default="")
MHEIBOS_LICENSE_SERVER_URL = config("MHEIBOS_LICENSE_SERVER_URL", default="")
MHEIBOS_LICENSE_OFFLINE_DAYS = config("MHEIBOS_LICENSE_OFFLINE_DAYS", default=30, cast=int)
MHEIBOS_INTEGRITY_ENFORCED = config("MHEIBOS_INTEGRITY_ENFORCED", default=False, cast=bool)
MHEIBOS_IA_ENABLED = config("MHEIBOS_IA_ENABLED", default=False, cast=bool)
MHEIBOS_IA_PROVIDER = config("MHEIBOS_IA_PROVIDER", default="none").lower()
MHEIBOS_IA_MODEL = config("MHEIBOS_IA_MODEL", default="gemini-3.6-flash")
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
