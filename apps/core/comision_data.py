"""Contenido institucional de la Comisión — editable sin tocar plantillas."""

OBJETIVOS = [
    "Diagnosticar si viviendas e infraestructuras afectadas por el doble terremoto del "
    "24 de junio de 2026 son habitables y seguras para su ocupación.",
    "Determinar de forma urgente si procede el reingreso de familias o la evacuación "
    "de edificaciones con riesgo estructural.",
    "Evaluar daños en viviendas, vialidad, puentes, elevados y obras públicas con "
    "criterios técnicos unificados.",
    "Capacitar y organizar brigadas de inspectores para aplicar la metodología ERD/ANIH "
    "en campo (planilla V.8).",
    "Emitir recomendaciones de acceso mediante semáforo verde, amarillo y rojo, "
    "con trazabilidad para la toma de decisiones de la comisión.",
]

MIEMBROS = [
    {
        "institucion": "Presidencia de la República",
        "rol": "Anuncio y conducción política de la comisión",
        "detalle": "Anunciada el 28 de junio de 2026 por la presidenta encargada Delcy Rodríguez.",
    },
    {
        "institucion": "Coordinación técnica",
        "rol": "Dirección del esfuerzo de evaluación",
        "detalle": "Ing. Francisco Garcés (coordinación citada en medios oficiales).",
    },
    {
        "institucion": "Ministerio de Hábitat y Vivienda",
        "rol": "Integrante de la comisión",
        "detalle": "Política habitacional y vivienda afectada.",
    },
    {
        "institucion": "Ministerio de Obras Públicas",
        "rol": "Integrante de la comisión",
        "detalle": "Infraestructura vial, puentes y obras públicas.",
    },
    {
        "institucion": "Colegio de Ingenieros de Venezuela (CIV)",
        "rol": "Brigadas técnicas y capacitación",
        "detalle": "Inspectores, inducciones masivas y evaluación de daños en edificaciones.",
    },
    {
        "institucion": "Cuerpo de Ingenieros de la FANB",
        "rol": "Apoyo técnico",
        "detalle": "Refuerzo en evaluación e inspección de infraestructura.",
    },
    {
        "institucion": "Funvisis",
        "rol": "Contexto sísmico",
        "detalle": "Información del evento del 24-jun-2026 (Mw 7,2 y 7,5).",
    },
    {
        "institucion": "Cámara Venezolana de la Construcción",
        "rol": "Criterios técnicos",
        "detalle": "Estándares y buenas prácticas de la construcción.",
    },
    {
        "institucion": "Universidades e instituciones académicas",
        "rol": "Sedes de inducción",
        "detalle": "UCV, UC, UCAB, UNEXPO y otras — capacitación masiva de profesionales.",
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
