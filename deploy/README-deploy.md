# Despliegue en Render

1. Crear repositorio y conectar Render.
2. Usar `deploy/render.yaml` o configurar manualmente:
   - **Build:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start:** `gunicorn config.wsgi:application`
   - **Settings:** `DJANGO_SETTINGS_MODULE=config.settings.production`
3. Variables: `SECRET_KEY`, `ALLOWED_HOSTS` (dominio Render), `DATABASE_URL` (PostgreSQL).
4. Tras el primer deploy: `python manage.py createsuperuser` vía shell de Render.
5. Cargar sedes reales en admin o con `python manage.py cargar_datos_iniciales`.
