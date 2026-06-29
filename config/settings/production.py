"""Producción (Render)."""
import os

from .base import *  # noqa: F403

DEBUG = False

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

if not SECRET_KEY or SECRET_KEY == "dev-insecure-change-me":  # noqa: F405
    raise ValueError("SECRET_KEY debe configurarse en producción")

# Render / HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
if _render_host:
    ALLOWED_HOSTS.append(_render_host)  # noqa: F405

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
if _render_host:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")

if EMAIL_HOST:  # noqa: F405
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
