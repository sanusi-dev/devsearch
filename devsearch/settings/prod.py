from .base import *  # noqa: F401, F403
from decouple import config  # noqa: F811

# ---------------------------------------------------------------------------
# Production overrides
# ---------------------------------------------------------------------------

DEBUG = False

ALLOWED_HOSTS = ["*"]

SECURE_HSTS_PRELOAD = True

# ---------------------------------------------------------------------------
# Production email (overrides the dev-only Mailtrap sandbox in base.py)
# ---------------------------------------------------------------------------

EMAIL_HOST = config("EMAIL_HOST", default="")
EMAIL_HOST_USER = config("EMAIL_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD", default="")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)

# ---------------------------------------------------------------------------
# Backblaze B2 object storage (S3-compatible)
# ---------------------------------------------------------------------------

if config("B2_APPLICATION_KEY_ID", default=""):
    INSTALLED_APPS = list(INSTALLED_APPS) + ["storages"]

    B2_ENDPOINT = config("B2_ENDPOINT", default="https://s3.us-east-005.backblazeb2.com")
    B2_BUCKET = config("B2_BUCKET_NAME", default="devsearchh")

    AWS_ACCESS_KEY_ID = config("B2_APPLICATION_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("B2_APPLICATION_KEY")
    AWS_S3_ENDPOINT_URL = B2_ENDPOINT
    AWS_STORAGE_BUCKET_NAME = B2_BUCKET
    AWS_S3_REGION_NAME = config("B2_REGION", default="us-east-005")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = ""

    MEDIA_URL = f"{B2_ENDPOINT}/{B2_BUCKET}/"

    # Django 6.0+ uses STORAGES dict instead of DEFAULT_FILE_STORAGE.
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
