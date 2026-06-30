"""Tests de páginas públicas del núcleo."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_como_funciona_carga(client):
    url = reverse("core:como_funciona")
    response = client.get(url)
    assert response.status_code == 200
    assert b"C\xc3\xb3mo funciona el sistema" in response.content
    assert b"Inscripci\xc3\xb3n p\xc3\xbablica" in response.content
    assert b"Sem\xc3\xa1foro de habitabilidad" in response.content
