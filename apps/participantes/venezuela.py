"""Formatos y validación — cédula y teléfono venezolanos."""
from __future__ import annotations

import re

from django.core.exceptions import ValidationError

# Operadoras móviles (código de 4 dígitos incluyendo el 0 inicial)
CODIGOS_MOVIL_VE: list[tuple[str, str]] = [
    ("0412", "0412 — Digitel"),
    ("0414", "0414 — Movistar"),
    ("0416", "0416 — Movilnet"),
    ("0424", "0424 — Movistar"),
    ("0426", "0426 — Movilnet"),
    ("0422", "0422 — Digitel"),
]

CODIGOS_MOVIL_VALIDOS = {c[0] for c in CODIGOS_MOVIL_VE}

TIPO_CEDULA_CHOICES = [("V", "V — Venezolano"), ("E", "E — Extranjero")]


def solo_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor or "")


def validar_cedula_venezolana(valor: str) -> str:
    """Normaliza a V12345678 o E12345678."""
    valor = (valor or "").strip().upper().replace(" ", "").replace("-", "").replace(".", "")
    if not re.match(r"^[VE]\d{6,9}$", valor):
        raise ValidationError("La cédula debe ser V o E seguida de 6 a 9 dígitos.")
    return valor


def validar_cedula_partes(tipo: str, numero: str) -> str:
    tipo = (tipo or "").strip().upper()
    if tipo not in ("V", "E"):
        raise ValidationError("Seleccione V o E.")
    digitos = solo_digitos(numero)
    if len(digitos) < 6 or len(digitos) > 9:
        raise ValidationError("El número de cédula debe tener entre 6 y 9 dígitos.")
    return validar_cedula_venezolana(f"{tipo}{digitos}")


def validar_telefono_movil_ve(valor: str) -> str:
    """Normaliza a 11 dígitos: 04XX + 7 dígitos."""
    digitos = solo_digitos(valor)
    if len(digitos) != 11:
        raise ValidationError("El celular debe tener 11 dígitos (04XX + 7 números).")
    if not digitos.startswith("04"):
        raise ValidationError("El celular debe comenzar con 04.")
    codigo = digitos[:4]
    if codigo not in CODIGOS_MOVIL_VALIDOS:
        raise ValidationError(
            f"Código de operadora no válido ({codigo}). Use 0412, 0414, 0416, 0424, 0426 o 0422."
        )
    return digitos


def validar_telefono_partes(codigo: str, linea: str) -> str:
    return validar_telefono_movil_ve(f"{codigo}{solo_digitos(linea)}")


def separar_cedula(cedula: str) -> tuple[str, str]:
    cedula = (cedula or "").strip().upper()
    if len(cedula) >= 2 and cedula[0] in "VE":
        return cedula[0], cedula[1:]
    return "V", solo_digitos(cedula)


def separar_telefono(telefono: str) -> tuple[str, str]:
    digitos = solo_digitos(telefono)
    if len(digitos) >= 11:
        return digitos[:4], digitos[4:11]
    if len(digitos) >= 4:
        return digitos[:4], digitos[4:]
    return "0412", digitos


def formato_cedula_mostrar(cedula: str) -> str:
    """Ej: V-12.345.678"""
    tipo, num = separar_cedula(cedula)
    if not num:
        return tipo
    # Puntos cada 3 desde la derecha
    partes = []
    while num:
        partes.insert(0, num[-3:])
        num = num[:-3]
    return f"{tipo}-{'.'.join(partes)}"


def formato_cedula_numero_input(numero: str) -> str:
    """Solo dígitos con puntos para el campo de entrada."""
    d = solo_digitos(numero)
    if not d:
        return ""
    partes = []
    while d:
        partes.insert(0, d[-3:])
        d = d[:-3]
    return ".".join(partes)


def formato_telefono_mostrar(telefono: str) -> str:
    """Ej: 0414-123-4567"""
    d = solo_digitos(telefono)
    if len(d) == 11:
        return f"{d[:4]}-{d[4:7]}-{d[7:]}"
    return telefono or ""


def formato_telefono_linea_input(linea: str) -> str:
    """Ej: 123-4567 (7 dígitos)."""
    d = solo_digitos(linea)[:7]
    if len(d) <= 3:
        return d
    return f"{d[:3]}-{d[3:]}"
