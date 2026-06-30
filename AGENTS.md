# AGENTS — Comisión Presidencial Habitabilidad (CPEH)

## Contexto

Sistema para la **Comisión Presidencial para la Evaluación de Habitabilidad** tras el doble terremoto del **24-jun-2026** en Venezuela. Coordinación citada en medios: Ing. Francisco Garcés. Actores: CIV, Funvisis, ministerios, universidades.

Leer primero: `docs/contexto/CONTEXTO-COMISION-PRESIDENCIAL.md`

## Qué construimos

1. **Capacitación masiva** — sedes, sesiones en lote, inscripción pública (URGENTE).
2. **Inspecciones ERD** — Planilla ANIH V.8, semáforo verde/amarillo/rojo.
3. **PDF** planilla y etiqueta.

## Stack

Django 5 · PostgreSQL · Bootstrap 5 · WeasyPrint · español (es-VE)

## Reglas de desarrollo

- Una BD: capacitación + inspecciones.
- No crear «curso» uno a uno: usar **Sede + Sesión en lote**.
- Inspector = usuario propio (no cuenta compartida).
- Variables inscripción: 10 campos del formulario oficial; lugar/fecha/hora vienen de la sesión.
- Priorizar Fase 1 antes de wizard de inspección.

## Rutas clave (objetivo)

| Ruta | Uso |
|------|-----|
| `/` | Inicio público |
| `/comision/` | Información institucional |
| `/como-funciona/` | Guía del sistema |
| `/inscripcion/` | Inscripción sede → sesión |
| `/inscripcion/sede/<slug>/` | QR universidad |
| `/panel/` | Coordinador |
| `/reportes/mapa/` | Mapa edificaciones |
| `/inspecciones/` | Portal inspector ERD |

## Producción y sync

- **URL:** https://cpeh-web.onrender.com
- **Git:** https://github.com/angelucv/comision-presidencial-habitabilidad (`main`)
- **Espejo Drive:** `MisProyectos-Espejo\D-CPEH` ↔ `clients\comision-presidencial-habitabilidad`
- **Handoff:** `docs/ESTADO-PROYECTO-Y-SYNC.md`
- **Aviso laptop:** `instrucciones-cursor/AVISO-PC-A-LAPTOP-CPEH-2026-06-29.md`

## Documento maestro

`docs/diseno/DOCUMENTO-MAESTRO-SISTEMA.docx` — pantallas, botones, flujos (v1.1+).

## Fases

`docs/diseno/FASES-IMPLEMENTACION.md`
