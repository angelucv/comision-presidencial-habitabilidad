# Deploy en Render — paso a paso (CPEH)

Guía para publicar el sistema en **https://cpeh-web.onrender.com** (o el nombre que elijas).

---

## Requisitos previos

- Cuenta en [render.com](https://render.com) (gratis con GitHub)
- Cuenta en [github.com](https://github.com)
- El proyecto en: `clients/comision-presidencial-habitabilidad`

---

## Paso 1 — Subir el código a GitHub

Abre **PowerShell** en la carpeta del proyecto:

```powershell
cd C:\Users\Angel\Projects\clients\comision-presidencial-habitabilidad

git init
git add .
git commit -m "CPEH: sistema capacitación e inscripción — listo para Render"
```

En GitHub: **New repository** → nombre ej. `cpeh-habitabilidad` → **sin** README (ya existe local).

Luego:

```powershell
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cpeh-habitabilidad.git
git push -u origin main
```

(Sustituye `TU_USUARIO` por tu usuario de GitHub.)

---

## Paso 2 — Crear cuenta y conectar Render con GitHub

1. Entra a [dashboard.render.com](https://dashboard.render.com)
2. **Sign Up** → **GitHub** → autoriza Render
3. Verifica tu correo si lo pide

---

## Paso 3 — Desplegar con Blueprint (recomendado)

1. En Render: **New +** → **Blueprint**
2. Conecta el repositorio `cpeh-habitabilidad`
3. Render detectará `render.yaml` en la raíz
4. Revisa:
   - **Web Service:** `cpeh-web`
   - **Database:** `cpeh-db` (PostgreSQL gratis)
5. **Apply**

El primer deploy tarda **5–10 minutos**.

---

## Paso 4 — Ajustar variables de entorno

Cuando termine el build, entra al servicio **cpeh-web** → **Environment**:

| Variable | Valor | Notas |
|----------|--------|--------|
| `ALLOWED_HOSTS` | `cpeh-web.onrender.com` | Si cambiaste el nombre del servicio, usa ese dominio |
| `SITE_URL` | `https://cpeh-web.onrender.com` | **Importante para QR y correos** |
| `CSRF_TRUSTED_ORIGINS` | `https://cpeh-web.onrender.com` | Obligatorio para formularios HTTPS |
| `CPEH_NOMBRE_COMISION` | (opcional) nombre completo | |
| `EMAIL_*` | (opcional) SMTP | Si quieres correos reales |

Pulsa **Save Changes** → Render redesplegará solo.

> Si tu URL final es distinta (ej. `cpeh-habitabilidad.onrender.com`), actualiza las tres variables con **tu** dominio exacto.

---

## Paso 5 — Crear usuario administrador

1. Servicio **cpeh-web** → pestaña **Shell**
2. Ejecuta:

```bash
python manage.py createsuperuser
```

Usuario sugerido: `admin` (contraseña segura que recuerdes).

---

## Paso 6 — Datos iniciales (opcional)

En la misma **Shell**:

```bash
python manage.py cargar_datos_iniciales
```

O importa sedes reales desde el **Panel** → Importar Excel.

---

## Paso 7 — Probar el sitio

| Página | URL |
|--------|-----|
| Inicio | `https://cpeh-web.onrender.com/` |
| Inscripción | `https://cpeh-web.onrender.com/inscripcion/` |
| Panel | `https://cpeh-web.onrender.com/panel/` |
| Admin | `https://cpeh-web.onrender.com/admin/` |

**Nota plan gratis:** el servicio se **duerme** tras ~15 min sin visitas; la primera carga puede tardar 30–60 s.

---

## Paso 8 — QR en producción

1. Entra al **Panel** con tu usuario admin
2. **Sedes y QR** → Descargar PNG
3. Los QR apuntarán a `SITE_URL` + `/inscripcion/sede/<slug>/`

---

## Despliegue manual (sin Blueprint)

Si prefieres crear todo a mano:

### A) Base de datos
**New +** → **PostgreSQL** → nombre `cpeh-db` → plan Free → Create

### B) Web Service
**New +** → **Web Service** → mismo repo → configuración:

| Campo | Valor |
|-------|--------|
| Name | `cpeh-web` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| Start Command | `gunicorn config.wsgi:application` |

**Environment variables:**

```
DJANGO_SETTINGS_MODULE=config.settings.production
PYTHON_VERSION=3.12.0
SECRET_KEY=<generar valor aleatorio largo>
DEBUG=false
DATABASE_URL=<Internal Database URL de cpeh-db>
ALLOWED_HOSTS=cpeh-web.onrender.com
SITE_URL=https://cpeh-web.onrender.com
CSRF_TRUSTED_ORIGINS=https://cpeh-web.onrender.com
```

Render inyecta `RENDER_EXTERNAL_HOSTNAME` automáticamente.

---

## Si el build falla

| Error | Solución |
|-------|----------|
| `SECRET_KEY debe configurarse` | Añade `SECRET_KEY` en Environment |
| `DisallowedHost` | Corrige `ALLOWED_HOSTS` con tu dominio `.onrender.com` |
| CSRF al enviar formulario | Añade `CSRF_TRUSTED_ORIGINS=https://tu-dominio.onrender.com` |
| `postgres://` | Ya corregido en settings (usa `postgresql://`) |
| Static files 404 | Revisa que el build incluya `collectstatic` |

Logs: servicio **cpeh-web** → **Logs** → **Deploy logs** o **Runtime logs**.

---

## Actualizar después de cambios

```powershell
git add .
git commit -m "descripción del cambio"
git push
```

Render redespliega automáticamente en cada push a `main`.

---

## Checklist final

- [ ] Repo en GitHub
- [ ] Blueprint o Web Service + PostgreSQL creados
- [ ] Build en verde (Live)
- [ ] `SITE_URL` y `CSRF_TRUSTED_ORIGINS` correctos
- [ ] Superusuario creado en Shell
- [ ] `/inscripcion/` abre en HTTPS
- [ ] QR descargado desde Panel
