# Contexto institucional — Comisión Presidencial para la Evaluación de Habitabilidad

**Última actualización:** 2026-06-29  
**Propósito de este documento:** marco de referencia para el desarrollo del sistema de capacitación de inspectores e inspecciones ERD.

---

## 1. Hecho generador

El **miércoles 24 de junio de 2026** Venezuela registró un **doblete sísmico** (dos terremotos en ~39 segundos):

| Evento | Magnitud (Mw) | Hora local (aprox.) | Epicentro |
|--------|---------------|---------------------|-----------|
| Primer sismo | 7,2 | 18:04 | Región de San Felipe, Yaracuy |
| Segundo sismo | 7,5 | ~18:05 | Yumare (norte de Venezuela) |

Fuentes: [Funvisis](https://www.funvisis.gob.ve/), [Wikipedia — Terremotos de Venezuela de 2026](https://es.wikipedia.org/wiki/Terremotos_de_Venezuela_de_2026), medios nacionales.

**Impacto reportado (cifras en evolución según fuente y fecha):**
- Afectación en Caracas, La Guaira, Miranda, Aragua, Yaracuy y otros estados.
- Colapso y daño estructural en edificaciones residenciales y de infraestructura.
- Estado de emergencia declarado; actividades escolares suspendidas en varias zonas (anuncio 28-jun).

---

## 2. Comisión Presidencial

**Anuncio:** domingo **28 de junio de 2026** — presidenta encargada Delcy Rodríguez.

**Nombre oficial (variantes en medios):**
- Comisión Presidencial para la **evaluación de habitabilidad de viviendas e infraestructuras**.
- Comisión Presidencial para la Evaluación de la **Habitabilidad, Vivienda e Infraestructura**.

**Objetivo:** diagnosticar si viviendas e infraestructura (vialidad, puentes, elevados, etc.) son **habitables / seguras** tras los sismos, y tomar decisiones urgentes sobre reingreso o evacuación.

**Coordinación:** Ing. **Francisco Garcés** (encabezado citado en medios oficiales).

### 2.1 Sistema de semáforo (habitabilidad)

Alineado con la metodología **ERD / ANIH** (etiquetas verde, amarilla, roja) que digitaliza este proyecto:

| Color | Significado (comisión) | Equivalente ERD / planilla V.8 |
|-------|------------------------|--------------------------------|
| **Verde** | Acceso permitido; condiciones seguras para ocupación | Etiqueta verde |
| **Amarillo** | Acceso restringido; daños moderados; requiere reparación / precaución | Etiqueta amarilla |
| **Rojo** | No habitable; daños críticos; evacuación; riesgo de colapso | Etiqueta roja |

### 2.2 Actores e instituciones (no exhaustivo)

| Actor | Rol en el esfuerzo |
|-------|-------------------|
| Ministerio de Hábitat y Vivienda | Integrante comisión |
| Ministerio de Obras Públicas | Infraestructura vial, puentes |
| **Colegio de Ingenieros de Venezuela (CIV)** | Brigadas técnicas, inspectores, capacitación |
| Cuerpo de Ingenieros FANB | Apoyo técnico |
| **Funvisis** | Contexto sísmico |
| Cámara Venezolana de la Construcción | Criterios técnicos |
| Universidades (UCV, UC, UCAB, UEFA, etc.) | Sedes de inducción masiva, profesionales |

El **CIV** anunció brigadas de ingenieros para evaluación de daños y habitabilidad ([Descifrado, 25-jun-2026](https://www.descifrado.com/2026/06/25/colegio-de-ingenieros-de-venezuela-ofrece-brigadas-tecnicas-para-evaluar-danos-de-los-terremotos/)).

---

## 3. Relación con este sistema informático

| Necesidad operativa | Módulo del sistema |
|-------------------|-------------------|
| Inducciones masivas en universidades y auditorios | **Capacitación** (sedes, sesiones en lote, inscripción) |
| Registro de ingenieros/arquitectos capacitados | **Participantes** + certificación |
| Inspección rápida en campo (planilla V.8 / ANIH) | **Inspecciones ERD** (wizard + reglas) |
| Semáforo verde/amarillo/rojo en edificaciones | **Resultado acceso** + PDF etiqueta |
| Trazabilidad y reportes para la comisión | **Reportes** + exportación |

**Alcance fase 1 (urgente):** inscripción y gestión de capacitaciones.  
**Alcance fase 2+:** inspecciones y PDF oficial.

**Fuera de alcance inicial del software:** evaluación de puentes/vialidad como módulo completo (la comisión también cubre infraestructura; este sistema se enfoca en **edificaciones** según instrumento ERD).

---

## 4. Referencias web (verificación)

| Fuente | URL |
|--------|-----|
| Globovisión — creación comisión | https://www.globovision.com/nacional/58031/presidenta-e-rodriguez-anuncio-comision-presidencial-para-evaluar-habitabilidad-de-viviendas-e |
| Radio Mundial | https://radiomundial.com.ve/gobierno-nacional-crea-comision-presidencial-para-evaluar-la-habitabilidad-de-viviendas-e-infraestructuras/ |
| Sputnik Mundo (29-jun-2026) | https://noticiaslatam.lat/20260629/venezuela-crea-comision-presidencial-para-revisar-habitabilidad-de-hogares-tras-terremotos-1174091037.html |
| CIV — brigadas técnicas | https://www.descifrado.com/2026/06/25/colegio-de-ingenieros-de-venezuela-ofrece-brigadas-tecnicas-para-evaluar-danos-de-los-terremotos/ |
| Wikipedia evento sísmico | https://es.wikipedia.org/wiki/Terremotos_de_Venezuela_de_2026 |

---

## 5. Glosario

| Término | Definición |
|---------|------------|
| **ERD** | Evaluación Rápida de Daños (metodología ANIH, planilla V.8) |
| **Habitabilidad** | Condición de una edificación para ser ocupada con seguridad |
| **Sede** | Universidad, auditorio o institución donde se imparte la inducción |
| **Sesión** | Fecha/hora concreta de inducción en una sede |
| **Inspector habilitado** | Participante certificado autorizado a cargar inspecciones |
