"""Backends de correo — Brevo vía HTTPS (funciona en Render plan gratis)."""
from __future__ import annotations

import email.utils
import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _parse_sender(from_email: str) -> tuple[str, str]:
    name, addr = email.utils.parseaddr(from_email or "")
    if not addr:
        addr = getattr(settings, "EMAIL_HOST_USER", "") or "noreply@example.com"
    if not name:
        name = "CPEH"
    return name, addr


class BrevoEmailBackend(BaseEmailBackend):
    """Envía correo con la API REST de Brevo (puerto 443, no SMTP)."""

    def send_messages(self, email_messages):
        api_key = getattr(settings, "BREVO_API_KEY", "")
        if not api_key:
            if self.fail_silently:
                return 0
            raise ValueError("BREVO_API_KEY no está configurada.")

        sent = 0
        for message in email_messages:
            try:
                self._send_one(message, api_key)
                sent += 1
            except Exception:
                logger.exception("Error enviando correo vía Brevo a %s", message.to)
                if not self.fail_silently:
                    raise
        return sent

    def _send_one(self, message: EmailMessage, api_key: str) -> None:
        sender_name, sender_email = _parse_sender(message.from_email)
        payload = {
            "sender": {"name": sender_name, "email": sender_email},
            "to": [{"email": addr} for addr in message.to],
            "subject": message.subject,
            "textContent": message.body,
        }
        if message.cc:
            payload["cc"] = [{"email": addr} for addr in message.cc]
        if message.bcc:
            payload["bcc"] = [{"email": addr} for addr in message.bcc]

        html_body = None
        if isinstance(message, EmailMultiAlternatives):
            for content, mime_type in message.alternatives:
                if mime_type == "text/html":
                    html_body = content
                    break
        if html_body:
            payload["htmlContent"] = html_body

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            BREVO_API_URL,
            data=data,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": api_key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=getattr(settings, "EMAIL_TIMEOUT", 15)) as response:
                if response.status >= 400:
                    raise urllib.error.HTTPError(
                        BREVO_API_URL, response.status, response.reason, response.headers, response
                    )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            logger.error("Brevo HTTP %s: %s", exc.code, body)
            raise
