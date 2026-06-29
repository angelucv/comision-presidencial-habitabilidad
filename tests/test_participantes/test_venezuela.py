"""Tests validación y formato Venezuela."""
import pytest
from django.core.exceptions import ValidationError

from apps.participantes.venezuela import (
    formato_cedula_mostrar,
    formato_telefono_mostrar,
    validar_cedula_partes,
    validar_telefono_partes,
)


def test_cedula_partes_ok():
    assert validar_cedula_partes("V", "12.345.678") == "V12345678"
    assert validar_cedula_partes("E", "8765432") == "E8765432"


def test_cedula_partes_invalida():
    with pytest.raises(ValidationError):
        validar_cedula_partes("V", "12345")


def test_telefono_partes_ok():
    assert validar_telefono_partes("0414", "123-4567") == "04141234567"


def test_telefono_operadora_invalida():
    with pytest.raises(ValidationError):
        validar_telefono_partes("0499", "1234567")


def test_formato_mostrar():
    assert formato_cedula_mostrar("V12345678") == "V-12.345.678"
    assert formato_telefono_mostrar("04141234567") == "0414-123-4567"
