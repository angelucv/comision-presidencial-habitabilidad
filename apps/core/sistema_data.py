"""Contenido de la página «Cómo funciona el sistema»."""

ROLES = [
    {
        "titulo": "Participante",
        "descripcion": (
            "Profesional que se inscribe a una inducción ERD en una sede y fecha. "
            "No necesita usuario ni contraseña para registrarse."
        ),
        "acciones": [
            "Elegir sede y sesión",
            "Completar datos personales",
            "Recibir código de inscripción y correo de confirmación",
        ],
    },
    {
        "titulo": "Coordinador",
        "descripcion": (
            "Personal de la comisión que organiza capacitaciones, controla asistencia "
            "y habilita inspectores certificados."
        ),
        "acciones": [
            "Cargar sedes y sesiones (Excel o panel)",
            "Descargar QR por sede para inscripción rápida",
            "Marcar asistencia y certificar participantes",
            "Registrar edificaciones y consultar el mapa",
        ],
    },
    {
        "titulo": "Inspector",
        "descripcion": (
            "Participante certificado que realiza inspecciones en campo con la "
            "metodología ERD (planilla V.8)."
        ),
        "acciones": [
            "Iniciar sesión con credenciales enviadas al certificar",
            "Seleccionar edificación asignada",
            "Completar el wizard de inspección",
            "Obtener semáforo verde, amarillo o rojo",
        ],
    },
]

PASOS_FLUJO = [
    {
        "numero": 1,
        "titulo": "Inscripción pública",
        "detalle": (
            "El participante elige sede y sesión, completa el formulario y recibe "
            "un código (ej. INS-2026-0007) y un correo de confirmación."
        ),
        "url_name": "capacitacion_public:paso1",
        "url_etiqueta": "Inscribirse",
    },
    {
        "numero": 2,
        "titulo": "Inducción y asistencia",
        "detalle": (
            "El coordinador marca quién asistió a la charla en el panel de la sesión. "
            "Las sesiones pasadas pueden registrarse de forma retroactiva."
        ),
        "url_name": None,
        "url_etiqueta": None,
    },
    {
        "numero": 3,
        "titulo": "Certificación",
        "detalle": (
            "Al certificar, el sistema crea un usuario inspector, genera una clave "
            "temporal y envía un correo con acceso al portal y contenido de la inducción."
        ),
        "url_name": None,
        "url_etiqueta": None,
    },
    {
        "numero": 4,
        "titulo": "Inspección ERD",
        "detalle": (
            "El inspector inicia sesión, abre una edificación y recorre el wizard "
            "de evaluación rápida de daños hasta asignar el semáforo."
        ),
        "url_name": "cuentas:login",
        "url_etiqueta": "Iniciar sesión",
    },
    {
        "numero": 5,
        "titulo": "Mapa y reportes",
        "detalle": (
            "Las edificaciones inspeccionadas aparecen en el mapa de Venezuela con "
            "color según habitabilidad; el coordinador exporta listas en Excel."
        ),
        "url_name": "reportes:mapa_edificios",
        "url_etiqueta": "Ver mapa",
    },
]

SEMAFORO_RESUMEN = [
    ("verde", "Habitable", "Uso normal con las precauciones habituales."),
    ("amarillo", "Acceso restringido", "Ingreso limitado; requiere evaluación adicional."),
    ("rojo", "No habitable", "No ingresar; riesgo alto según criterios ERD."),
    ("gris", "Pendiente", "Edificación registrada, aún sin inspección cerrada."),
]
