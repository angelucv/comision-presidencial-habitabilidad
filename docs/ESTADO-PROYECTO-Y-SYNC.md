# CPEH — Estado del proyecto y sincronía Drive

**Última actualización:** 2026-07-20 ~23:00 (UTC-4) · **Equipo:** PC (perfil `Angel`)

## Producción

| Concepto | Valor |
|----------|--------|
| **URL** | https://cpeh-web.onrender.com |
| **Repo Git** | https://github.com/angelucv/comision-presidencial-habitabilidad |
| **Rama** | `main` |
| **Último commit** | `fa61ee8` — navbar responsive |
| **Plan Render** | Starter (dejó de ser free) |

### Accesos demo

| Rol | Usuario | Clave |
|-----|---------|-------|
| Admin / coordinador | `admin` | `cpeh2026` |
| Login | `/cuentas/login/` | |
| Admin Django | `/admin/` | |

## Espejo Google Drive (multi-equipo)

| Local | Espejo Drive |
|-------|----------------|
| `Projects\clients\comision-presidencial-habitabilidad` | `G:\My Drive\MisProyectos-Espejo\D-CPEH` |

**Git** sigue siendo la fuente de verdad del código (`git pull` en la laptop). Drive complementa documentación, contexto y árbol sin depender solo del remoto.

Ver también: `instrucciones-cursor/RUTAS-CANONICAS-ESPEJO-DRIVE.md` (cuarta pareja canónica).

## Qué está implementado (jun 2026)

### Fase 1 — Capacitación
- Inscripción pública `/inscripcion/` + QR por sede
- Panel coordinador `/panel/` (sedes, sesiones, import Excel, export inscritos)
- Máscaras cédula/teléfono VE
- Página **La Comisión** `/comision/`
- Página **Cómo funciona** `/como-funciona/`

### Fase 2 — Certificación e inspecciones (inicial)
- Asistencia y certificación por sesión → crea usuario inspector + correo
- Registro de edificaciones en panel
- Portal inspector `/inspecciones/` + wizard ERD simplificado
- Mapa Venezuela `/reportes/mapa/` (Leaflet local, fix locale `json_script`)

### Infra
- Deploy Render + PostgreSQL (`render.yaml`)
- Correo vía **Brevo API** (`BREVO_API_KEY` en variables Render; no SMTP en plan free)
- Correo institucional: `capacitacion.cpeh@gmail.com`
- Superusuario auto en deploy (`ensure_superuser`)
- Datos demo: sedes, sesiones, 8 edificios

## Pendiente / conocido

| Tema | Notas |
|------|--------|
| **Correos** | Verificar `BREVO_API_KEY` y remitente verificado en Brevo Senders |
| **Wizard ERD** | Planilla V.8 completa, PDF semáforo |
| **Import masivo edificios** | Excel |
| **Cambio de clave inspectores** | Flujo self-service |

## URLs útiles

| Ruta | Uso |
|------|-----|
| `/` | Inicio |
| `/como-funciona/` | Guía del sistema |
| `/comision/` | Información institucional |
| `/inscripcion/` | Inscripción pública |
| `/panel/` | Coordinador (staff) |
| `/reportes/mapa/` | Mapa edificaciones |
| `/inspecciones/` | Inspector certificado |

## Laptop — al retomar

1. Esperar Google Drive sin errores.
2. `robocopy` espejo → local: `D-CPEH` → `Projects\clients\comision-presidencial-habitabilidad`.
3. `git clone` o `git pull` en el repo (preferible para código).
4. Leer `AVISO-PC-A-LAPTOP-CPEH-2026-06-29.md` en `instrucciones-cursor`.
5. Abrir workspace: `clients\comision-presidencial-habitabilidad`.

### BI cruce inspecciones (activo — 2026-07-20)

| Concepto | Valor |
|----------|--------|
| **Repo Git (privado)** | https://github.com/angelucv/bi-cruce-inspecciones |
| **Último commit (PC)** | `3121d66` — mapa operativo compacto |
| **Deploy hermano** | https://github.com/angelucv/habitable |
| **Local** | `Projects\clients\comision-presidencial-habitabilidad\bi-cruce-inspecciones` |
| **Espejo Drive** | `MisProyectos-Espejo\D-CPEH\bi-cruce-inspecciones` |

**Avance reciente (jul 2026):** cruce caso a caso (Excel contacto); Habitable ~17 k insp.; pestaña **1×10 pendientes** (mapa + listado + análisis descripción); sidebar **Corte de información**; mapa operativo compacto (KPIs en línea, sin scroll largo).

En la laptop (preferible Git):

```powershell
cd $env:USERPROFILE\Projects\clients\comision-presidencial-habitabilidad
git clone https://github.com/angelucv/bi-cruce-inspecciones.git
# si ya existe:
cd bi-cruce-inspecciones; git pull
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Ajustar config.toml y generar parquet: python src\prepare_data.py
streamlit run app.py
```

Los parquet con contacto **no** van en Git; generarlos en cada máquina o copiarlos por Drive si hace falta. Aviso handoff: `instrucciones-cursor/AVISO-PC-A-LAPTOP-CPEH-BI-CRUCE-2026-07-20.md`.