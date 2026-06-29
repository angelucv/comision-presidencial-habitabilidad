# Fases de implementación — CPEH

**Marco:** Comisión Presidencial · Habitabilidad post-terremoto 24-jun-2026  
**Prioridad:** Fase 0–1 inmediata (capacitación masiva en universidades)

---

## Fase 0 — Arranque (1–2 días) ✓ en curso

- [x] Directorio y documentación institucional
- [x] Proyecto Django `config/` + apps base
- [x] `.env`, requirements, README
- [ ] Deploy staging (Render)

**Entregable:** repositorio ejecutable con admin.

---

## Fase 1 🔴 — Inscripción masiva (3–5 días)

**Urgencia:** inducciones en UCV, UC, auditorios, CIV.

- Catálogo **Sedes** ✓ (modelo + admin)
- **Sesiones en lote** (comando `crear_sesiones_lote`) ✓
- Inscripción pública `/inscripcion/` (sede → sesión → datos) ✓
- QR por sede ✓
- Admin: listado inscritos por sesión ✓

**Entregable:** enlace/QR operativo en sedes.

---

## Fase 2 — Día del curso (3–4 días)

- Pantalla **Sesiones de hoy**
- Asistencia y certificación
- Walk-in manual
- Export Excel

---

## Fase 3 — Inspectores (3–4 días)

- Usuario por inspector certificado
- Vinculación Participante ↔ User
- Roles coordinador / inspector

---

## Fase 4 — Inspección ERD (2–3 semanas)

- Wizard planilla V.8 (pasos 0–8)
- Reglas corte → etiqueta roja
- Fotos y cierre

---

## Fase 5 — Salidas oficiales (1–2 semanas)

- PDF planilla + etiqueta semáforo
- Correos SMTP
- Reportes comisión
- Producción HTTPS

---

## Alineación institucional

| Fase | Apoyo a la comisión |
|------|---------------------|
| 1–2 | Escalar capacitación de brigadas (CIV + universidades) |
| 3–4 | Inspecciones con criterio único ERD / semáforo |
| 5 | Evidencia PDF para decisiones de habitabilidad |
