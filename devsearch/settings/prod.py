from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Production overrides
# ---------------------------------------------------------------------------

DEBUG = False

# Pxxl rotates IPs on every deploy.  Allow all hosts — the platform handles
# domain routing and SSL termination before requests reach this app.
ALLOWED_HOSTS = ["*"]

SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------------
# Production email (overrides the dev-only Mailtrap sandbox in base.py)
# Set these on Pxxl as normal env vars (not DEV_ prefixed).
# ---------------------------------------------------------------------------

EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
