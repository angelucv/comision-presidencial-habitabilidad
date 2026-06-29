# Estructura del proyecto CPEH

```
comision-presidencial-habitabilidad/
├── README.md
├── AGENTS.md
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
│
├── config/                      # Proyecto Django
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                    # Páginas inicio, utilidades
│   ├── cuentas/                 # Auth, perfiles, roles
│   ├── capacitacion/            # Campaña, Sede, Sesión, Inscripción
│   ├── participantes/           # Personas (C.I., contacto)
│   ├── inspecciones/            # ERD wizard, PDF, adjuntos
│   └── reportes/                # Dashboards, exports
│
├── templates/
│   ├── base.html
│   ├── core/
│   ├── cuentas/
│   ├── capacitacion/
│   ├── inspecciones/
│   └── pdf/                     # HTML → WeasyPrint
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/                     # Logo comisión / CIV
│
├── media/                       # Fotos inspección (gitignore)
│
├── docs/
│   ├── contexto/
│   ├── diseno/
│   └── referencias/
│
├── scripts/
│   ├── generar_documento_maestro.py
│   └── import_sesiones_excel.py   # (fase 2)
│
├── deploy/
│   ├── render.yaml
│   └── README-deploy.md
│
└── tests/
    ├── test_capacitacion/
    └── test_inspecciones/
```

## Convención de nombres

| Código interno | Significado |
|----------------|-------------|
| **CPEH** | Comisión Presidencial Evaluación Habitabilidad |
| **ERD** | Evaluación Rápida de Daños |
| **Sede** | Lugar fijo de inducción (universidad, auditorio) |
| **Sesión** | Instancia fecha+hora de inducción |
