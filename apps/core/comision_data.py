"""Contenido institucional de la Comisión — editable sin tocar plantillas."""

OBJETIVOS = [
    "Diagnosticar si viviendas e infraestructuras afectadas por el doble terremoto del "
    "24 de junio de 2026 son habitables y seguras para su ocupación.",
    "Determinar de forma urgente si procede el reingreso de familias o la evacuación "
    "de edificaciones con riesgo estructural.",
    "Evaluar daños en viviendas, vialidad, puentes, elevados y obras públicas con "
    "criterios técnicos unificados.",
    "Capacitar y registrar brigadas de inspectores (inducciones programadas o ya realizadas) "
    "para aplicar la metodología ERD/ANIH en campo (planilla V.8).",
    "Emitir recomendaciones de acceso mediante semáforo verde, amarillo y rojo, "
    "con trazabilidad para la toma de decisiones de la comisión.",
]

# Enlaces para la página de inicio (nombre visible + web / Instagram verificados)
INSTITUCIONES_ENLACES = [
    {
        "nombre": "Ing. Francisco Garcés — Coordinación técnica",
        "web": None,
        "instagram": "https://www.instagram.com/garcesfrancisco",
    },
    {
        "nombre": "Colegio de Ingenieros de Venezuela (CIV)",
        "web": "https://civ.net.ve",
        "instagram": "https://www.instagram.com/civoficial",
    },
    {
        "nombre": "Fundación Venezolana de Investigaciones Sismológicas (Funvisis)",
        "web": "http://www.funvisis.gob.ve",
        "instagram": "https://www.instagram.com/funvisis",
    },
    {
        "nombre": "Ministerio del Poder Popular para el Hábitat y la Vivienda (MINHVI)",
        "web": "https://www.minhvi.gob.ve",
        "instagram": "https://www.instagram.com/minvivienda_ve",
    },
    {
        "nombre": "Ministerio del Poder Popular de Obras Públicas (MPPOP)",
        "web": None,
        "instagram": "https://www.instagram.com/minobraspublicas_ve",
    },
    {
        "nombre": "Cámara Venezolana de la Construcción (CVC)",
        "web": "https://www.cvc.com.ve",
        "instagram": "https://www.instagram.com/cvconstruccion",
    },
]

MIEMBROS = [
    {
        "institucion": "Presidencia de la República",
        "rol": "Anuncio y conducción política de la comisión",
        "detalle": "Anunciada el 28 de junio de 2026 por la presidenta encargada Delcy Rodríguez.",
        "web": "https://www.presidencia.gob.ve",
        "instagram": None,
    },
    {
        "institucion": "Coordinación técnica",
        "rol": "Dirección del esfuerzo de evaluación",
        "detalle": "Ing. Francisco Garcés.",
        "web": None,
        "instagram": "https://www.instagram.com/garcesfrancisco",
    },
    {
        "institucion": "Ministerio del Poder Popular para el Hábitat y la Vivienda (MINHVI)",
        "rol": "Integrante de la comisión",
        "detalle": "Política habitacional y vivienda afectada.",
        "web": "https://www.minhvi.gob.ve",
        "instagram": "https://www.instagram.com/minvivienda_ve",
    },
    {
        "institucion": "Ministerio del Poder Popular de Obras Públicas (MPPOP)",
        "rol": "Integrante de la comisión",
        "detalle": "Infraestructura vial, puentes y obras públicas.",
        "web": None,
        "instagram": "https://www.instagram.com/minobraspublicas_ve",
    },
    {
        "institucion": "Colegio de Ingenieros de Venezuela (CIV)",
        "rol": "Brigadas técnicas y capacitación",
        "detalle": "Inspectores, inducciones masivas y evaluación de daños en edificaciones.",
        "web": "https://civ.net.ve",
        "instagram": "https://www.instagram.com/civoficial",
    },
    {
        "institucion": "Cuerpo de Ingenieros de la FANB",
        "rol": "Apoyo técnico",
        "detalle": "Refuerzo en evaluación e inspección de infraestructura.",
        "web": None,
        "instagram": None,
    },
    {
        "institucion": "Fundación Venezolana de Investigaciones Sismológicas (Funvisis)",
        "rol": "Contexto sísmico",
        "detalle": "Información del evento del 24-jun-2026 (Mw 7,2 y 7,5).",
        "web": "http://www.funvisis.gob.ve",
        "instagram": "https://www.instagram.com/funvisis",
    },
    {
        "institucion": "Cámara Venezolana de la Construcción (CVC)",
        "rol": "Criterios técnicos",
        "detalle": "Estándares y buenas prácticas de la construcción.",
        "web": "https://www.cvc.com.ve",
        "instagram": "https://www.instagram.com/cvconstruccion",
    },
    {
        "institucion": "Universidades e instituciones académicas",
        "rol": "Sedes de inducción",
        "detalle": "UCV, UC, UCAB, UNEXPO y otras — capacitación masiva de profesionales.",
        "web": "https://www.ucv.ve",
        "instagram": None,
    },
]

SEMAFORO = [
    ("verde", "Habitable", "Acceso permitido. Condiciones seguras para la ocupación."),
    ("amarillo", "Acceso restringido", "Daños moderados. Requiere precaución, reparación o uso limitado."),
    ("rojo", "No habitable", "Daños críticos. Evacuación. Riesgo de colapso o falla estructural."),
]

EVENTO_SISMO = [
    ("Primer evento", "Mw 7,2", "18:04", "Región de San Felipe, Yaracuy"),
    ("Segundo evento", "Mw 7,5", "~18:05", "Yumare (norte de Venezuela)"),
]
