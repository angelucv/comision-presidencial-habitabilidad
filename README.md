# CPEH — Sistema de Capacitación e Inspecciones

Sistema web para la **Comisión Presidencial para la Evaluación de Habitabilidad de Viviendas e Infraestructuras** (Venezuela, post-terremoto 24-jun-2026).

## Objetivo

1. **Capacitar y registrar** inspectores (inducciones masivas en sedes universitarias).
2. **Digitalizar** la Evaluación Rápida de Daños (ERD) — Planilla ANIH V.8.
3. **Emitir** semáforo verde / amarillo / rojo y PDF de planilla.

## Stack

- Python 3.12+
- Django 5.x
- PostgreSQL (producción) / SQLite (desarrollo)
- Bootstrap 5 · WeasyPrint (PDF)

## Inicio rápido

```powershell
cd clients\comision-presidencial-habitabilidad
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_datos_iniciales   # sedes de ejemplo (opcional)
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/ — crear superusuario con `createsuperuser`.

### Rutas públicas (Fase 1)

| Ruta | Descripción |
|------|-------------|
| `/` | Inicio institucional |
| `/inscripcion/` | Elegir sede y sesión |
| `/inscripcion/sede/<slug>/` | Inscripción por QR (ej. `/inscripcion/sede/ucv/`) |

### Panel coordinador

| Ruta | Función |
|------|---------|
| `/panel/` | Dashboard (usuario staff) |
| `/panel/importar/` | Subir Excel sedes/sesiones |
| `/panel/plantilla-excel/` | Descargar plantilla |
| `/panel/sedes/` | Enlaces y QR PNG por sede |

Ver flujo completo: `docs/diseno/FLUJO-PROCESOS.md`

### Tests

```powershell
python -m pytest tests/ -v
```

## Documentación

| Documento | Ubicación |
|-----------|-----------|
| Contexto comisión | `docs/contexto/CONTEXTO-COMISION-PRESIDENCIAL.md` |
| Documento maestro (pantallas, flujos) | `docs/diseno/DOCUMENTO-MAESTRO-SISTEMA.docx` |
| Fases de implementación | `docs/diseno/FASES-IMPLEMENTACION.md` |
| Planilla ERD (texto extraído) | `docs/referencias/planilla-erd-v8-extracto.txt` |

## Estructura

Ver `docs/diseno/ESTRUCTURA-PROYECTO.md`.

## Urgencia

**Fase 1:** inscripción pública + sedes + sesiones en lote (ver fases).
