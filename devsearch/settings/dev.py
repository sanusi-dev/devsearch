from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Development overrides
# ---------------------------------------------------------------------------

DEBUG = True

# Disable production security settings for local development.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# Use the non-compressing, non-manifest static files storage in dev
# so changes are reflected immediately without running collectstatic.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
