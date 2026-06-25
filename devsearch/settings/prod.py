from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Production overrides
# ---------------------------------------------------------------------------

DEBUG = False

# Pxxl rotates IPs on every deploy.  Allow all hosts — the platform handles
# domain routing and SSL termination before requests reach this app.
ALLOWED_HOSTS = ["*"]

SECURE_HSTS_PRELOAD = True
