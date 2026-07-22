# CPEH — Estado del proyecto y sincronía Drive

**Última actualización:** 2026-07-22 ~00:40 (UTC-4) · **Equipo:** PC (perfil `Angel`)

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

### BI cruce inspecciones (activo — 2026-07-22)

| Concepto | Valor |
|----------|--------|
| **Repo Git (privado)** | https://github.com/angelucv/bi-cruce-inspecciones |
| **Último commit (PC)** | `3dc1be9` — Mapa NASA + análisis 1×10/Habitable/IA |
| **Deploy hermano** | https://github.com/angelucv/habitable · `2a93718` |
| **URL BI prod** | https://habitable.onrender.com |
| **Local** | `Projects\clients\comision-presidencial-habitabilidad\bi-cruce-inspecciones` |
| **Espejo Drive** | `MisProyectos-Espejo\D-CPEH\bi-cruce-inspecciones` |

**Avance 22-jul 2026:** cruces detallados NASA (2,7 M en local); seed map-lite + cruces en Git; sección **Mapa NASA** y 3 análisis (cola 1×10, confiabilidad Habitable, acuerdo IA). Aviso: `AVISO-PC-A-LAPTOP-CPEH-BI-NASA-2026-07-22.md`. **Drive G: no montado** al cerrar — pendiente `robocopy` → D-CPEH.

**Avance previo (jul 2026):** cruce caso a caso; Habitable corte 21-jul; **1×10 pendientes**; **Mapas de abordaje**; sidebar **Corte de información**.

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

Los parquet con contacto **no** van en Git; generarlos en cada máquina o copiarlos por Drive si hace falta. Seed NASA lite/cruces **sí** vienen en el pull. Avisos: `AVISO-PC-A-LAPTOP-CPEH-BI-NASA-2026-07-22.md` y `AVISO-PC-A-LAPTOP-CPEH-BI-CRUCE-2026-07-20.md`.
