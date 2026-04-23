from pathlib import Path
import os
from decouple import config, Csv

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# The public-facing URL of this site — used to build absolute links in emails.
SITE_URL = config("SITE_URL", default="http://127.0.0.1:8000")

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third-party
    "django_htmx",
    "mailer",
    "widget_tweaks",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    # Local
    "projects.apps.ProjectsConfig",
    "users.apps.UsersConfig",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "devsearch.middleware.HtmxMessageMiddleware",
]

ROOT_URLCONF = "devsearch.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "devsearch.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (user-uploaded content: profile pictures, project images, etc.)
# All uploads are stored inside static/images/ — this keeps the existing files
# working without migration. For production, move uploads to a dedicated
# object storage bucket (e.g. S3) and update MEDIA_ROOT/MEDIA_URL accordingly.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static" / "images"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------

if DEBUG:
    EMAIL_HOST = config("DEV_EMAIL_HOST", default="sandbox.smtp.mailtrap.io")
    EMAIL_HOST_USER = config("DEV_EMAIL_USER")
    EMAIL_HOST_PASSWORD = config("DEV_EMAIL_PASSWORD")
    EMAIL_PORT = config("DEV_EMAIL_PORT", default=2525, cast=int)
else:
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_HOST_USER = config("EMAIL_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
    EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Use django-mailer to queue emails in the database.
# The background worker (run_mailer.sh) dispatches them via the SMTP backend below.
EMAIL_BACKEND = "mailer.backend.DbBackend"
MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# How long (seconds) the background worker sleeps when the queue is empty.
MAILER_EMPTY_QUEUE_SLEEP = 30

# ---------------------------------------------------------------------------
# django-allauth configuration
# ---------------------------------------------------------------------------

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_AUTO_SIGNUP = True

LOGIN_REDIRECT_URL = "/profiles/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

# GitHub OAuth — credentials supplied via environment variables.
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "SCOPE": ["user:email"],
        "APP": {
            "client_id": config("GITHUB_CLIENT_ID", default=""),
            "secret": config("GITHUB_CLIENT_SECRET", default=""),
        },
    },
}
