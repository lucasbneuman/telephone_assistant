"""
Datos ficticios de la Clínica San Rafael
Este archivo contiene toda la información que el asistente necesita conocer sobre la clínica.
Puedes editar estos datos fácilmente para personalizarlos.
"""

from datetime import datetime, timedelta

# ==================== INFORMACIÓN GENERAL ====================

CLINICA = {
    "nombre": "Clínica San Rafael",
    "direccion": "Av. Libertador 1234, CABA",
    "telefono": "(011) 4567-8900",
    "email": "info@clinicasanrafael.com.ar",
    "sitio_web": "www.clinicasanrafael.com.ar"
}

HORARIOS = {
    "lunes_viernes": "8:00 a 20:00",
    "sabados": "9:00 a 13:00",
    "domingos": "Cerrado",
    "feriados": "Cerrado"
}

# ==================== ESPECIALIDADES Y MÉDICOS ====================

ESPECIALIDADES = {
    "clinica_medica": {
        "nombre": "Clínica Médica",
        "medicos": [
            {
                "nombre": "Dr. Carlos Méndez",
                "dias": ["Lunes", "Miércoles", "Jueves"],
                "horario": "8:00 a 13:00"
            },
            {
                "nombre": "Dra. Ana Torres",
                "dias": ["Martes", "Viernes"],
                "horario": "14:00 a 20:00"
            }
        ]
    },
    "cardiologia": {
        "nombre": "Cardiología",
        "medicos": [
            {
                "nombre": "Dr. Roberto Silva",
                "dias": ["Lunes", "Miércoles", "Viernes"],
                "horario": "9:00 a 14:00"
            },
            {
                "nombre": "Dra. Laura Gómez",
                "dias": ["Jueves", "Viernes"],
                "horario": "15:00 a 19:00"
            }
        ]
    },
    "traumatologia": {
        "nombre": "Traumatología",
        "medicos": [
            {
                "nombre": "Dr. Martín López",
                "dias": ["Lunes", "Martes", "Jueves", "Viernes"],
                "horario": "10:00 a 18:00"
            }
        ]
    },
    "pediatria": {
        "nombre": "Pediatría",
        "medicos": [
            {
                "nombre": "Dra. Sofía Fernández",
                "dias": ["Lunes", "Miércoles", "Jueves"],
                "horario": "8:00 a 14:00"
            },
            {
                "nombre": "Dr. Diego Ruiz",
                "dias": ["Martes", "Viernes"],
                "horario": "14:00 a 20:00"
            }
        ]
    },
    "dermatologia": {
        "nombre": "Dermatología",
        "medicos": [
            {
                "nombre": "Dra. Patricia Valdés",
                "dias": ["Martes", "Jueves"],
                "horario": "9:00 a 15:00"
            }
        ]
    },
    "ginecologia": {
        "nombre": "Ginecología",
        "medicos": [
            {
                "nombre": "Dra. Marcela Russo",
                "dias": ["Lunes", "Miércoles", "Viernes"],
                "horario": "10:00 a 16:00"
            }
        ]
    },
    "oftalmologia": {
        "nombre": "Oftalmología",
        "medicos": [
            {
                "nombre": "Dr. Pablo Moreno",
                "dias": ["Martes", "Jueves"],
                "horario": "8:00 a 13:00"
            }
        ]
    }
}

# ==================== COBERTURAS Y PRECIOS ====================

OBRAS_SOCIALES = [
    "OSDE",
    "Swiss Medical",
    "GALENO",
    "IOMA",
    "PAMI",
    "OSECAC",
    "OSPEDYC",
    "OSDEPYM",
    "UOM"
]

PREPAGAS = [
    "Medifé",
    "Sancor Salud",
    "Accord Salud",
    "Prevención Salud"
]

PRECIOS = {
    "consulta_particular": 15000,
    "consulta_pediatria": 12000,
    "consulta_especialista": 18000,
    "certificado": 5000,
    "receta": 2000
}

# ==================== TURNOS DISPONIBLES (MOCK) ====================

def generar_turnos_mock():
    """
    Genera turnos ficticios para los próximos 3 días.
    En una implementación real, esto consultaría una base de datos.
    """
    hoy = datetime.now()

    turnos = {
        "hoy": {
            "fecha": hoy.strftime("%d/%m/%Y"),
            "disponibles": []  # Completo
        },
        "manana": {
            "fecha": (hoy + timedelta(days=1)).strftime("%d/%m/%Y"),
            "disponibles": ["10:00", "14:30", "16:00", "17:30"]
        },
        "pasado_manana": {
            "fecha": (hoy + timedelta(days=2)).strftime("%d/%m/%Y"),
            "disponibles": ["09:00", "11:30", "15:00", "17:30", "18:30"]
        }
    }

    return turnos

TURNOS_MOCK = generar_turnos_mock()

# ==================== SERVICIOS ADICIONALES ====================

SERVICIOS = {
    "laboratorio": {
        "nombre": "Laboratorio de Análisis Clínicos",
        "horario": "Lunes a Viernes 7:00 a 10:00 (ayuno)",
        "requiere_turno": False,
        "requiere_orden": True
    },
    "ecografia": {
        "nombre": "Ecografía",
        "horario": "Lunes a Viernes 9:00 a 18:00",
        "requiere_turno": True,
        "requiere_orden": True
    },
    "electrocardiograma": {
        "nombre": "Electrocardiograma",
        "horario": "Lunes a Viernes 8:00 a 19:00",
        "requiere_turno": True,
        "requiere_orden": True
    },
    "radiografia": {
        "nombre": "Radiografía",
        "horario": "Lunes a Viernes 8:00 a 18:00, Sábados 9:00 a 12:00",
        "requiere_turno": True,
        "requiere_orden": True
    }
}

# ==================== FAQs ====================

FAQS = {
    "como_llegar": {
        "pregunta": "¿Cómo llegar a la clínica?",
        "respuesta": """Estamos en Av. Libertador 1234, CABA. Puede llegar en:
- Colectivos: 10, 37, 59, 60, 93, 130, 152
- Subte: Línea D, estación Palermo, a 5 cuadras
- Tren: Estación Palermo, a 8 cuadras
Contamos con estacionamiento para pacientes."""
    },
    "retirar_resultados": {
        "pregunta": "¿Cómo retirar resultados de estudios?",
        "respuesta": """Puede retirar sus resultados de dos formas:
1. Presencial: En recepción con su DNI, de lunes a viernes de 8:00 a 20:00
2. Por email: Los resultados se envían automáticamente al correo registrado en 24-48hs
Para resultados de laboratorio: 48-72hs hábiles."""
    },
    "urgencias": {
        "pregunta": "¿Atienden urgencias?",
        "respuesta": """No contamos con servicio de guardia. Para urgencias, recomendamos acudir al Hospital Fernández (Av. Cerviño 3356) o al Hospital Rivadavia (Av. Gral. Las Heras 2670), ambos con guardia 24hs."""
    },
    "formas_pago": {
        "pregunta": "¿Qué formas de pago aceptan?",
        "respuesta": """Aceptamos:
- Efectivo
- Tarjetas de débito y crédito (Visa, Mastercard, American Express)
- Transferencias bancarias (CBU disponible en recepción)
- Mercado Pago
- Para consultas particulares: planes de pago en 3 cuotas sin interés."""
    },
    "primera_vez": {
        "pregunta": "¿Qué debo llevar si es mi primera vez?",
        "respuesta": """Por favor traiga:
- DNI original
- Credencial de obra social o prepaga (si corresponde)
- Orden médica (si fue derivado)
- Estudios previos relacionados con la consulta
- Llegue 10 minutos antes para completar la ficha médica."""
    },
    "cancelar_turno": {
        "pregunta": "¿Cómo cancelo o reagendo un turno?",
        "respuesta": """Puede cancelar o reagendar llamando al (011) 4567-8900 o por WhatsApp al mismo número. Le pedimos avisar con al menos 24hs de anticipación para que otro paciente pueda tomar ese horario."""
    },
    "recetas_certificados": {
        "pregunta": "¿Puedo pedir recetas o certificados sin turno?",
        "respuesta": """Los certificados y recetas deben ser solicitados en consulta con el médico. Si necesita una renovación de receta y es paciente regular, puede solicitarla por WhatsApp y retirarla en 48hs (sujeto a aprobación médica)."""
    }
}

# ==================== INFORMACIÓN DE CONTACTO ADICIONAL ====================

CONTACTO = {
    "whatsapp": "(011) 4567-8900",
    "email_turnos": "turnos@clinicasanrafael.com.ar",
    "email_resultados": "resultados@clinicasanrafael.com.ar",
    "email_administracion": "administracion@clinicasanrafael.com.ar",
    "redes_sociales": {
        "instagram": "@clinicasanrafael",
        "facebook": "ClinicaSanRafaelOficial"
    }
}

# ==================== FUNCIONES AUXILIARES ====================

def obtener_especialidades_disponibles():
    """Retorna una lista con los nombres de todas las especialidades."""
    return [esp["nombre"] for esp in ESPECIALIDADES.values()]

def obtener_medicos_por_especialidad(especialidad_key):
    """Retorna los médicos de una especialidad específica."""
    if especialidad_key in ESPECIALIDADES:
        return ESPECIALIDADES[especialidad_key]["medicos"]
    return []

def verificar_cobertura(cobertura):
    """Verifica si la clínica trabaja con la cobertura mencionada."""
    cobertura_upper = cobertura.upper()

    # Verificar obras sociales
    for os in OBRAS_SOCIALES:
        if os.upper() in cobertura_upper or cobertura_upper in os.upper():
            return True, "obra social", os

    # Verificar prepagas
    for pp in PREPAGAS:
        if pp.upper() in cobertura_upper or cobertura_upper in pp.upper():
            return True, "prepaga", pp

    return False, None, None

def obtener_turnos_disponibles(cuando="manana"):
    """Retorna los turnos disponibles según el día solicitado."""
    if cuando in TURNOS_MOCK:
        return TURNOS_MOCK[cuando]
    return None

def buscar_faq(consulta):
    """Busca una FAQ que coincida con la consulta del usuario."""
    consulta_lower = consulta.lower()

    keywords = {
        "como_llegar": ["llegar", "donde", "direccion", "ubicacion", "transporte", "colectivo", "subte"],
        "retirar_resultados": ["resultados", "retirar", "laboratorio", "estudios", "analisis"],
        "urgencias": ["urgencia", "emergencia", "guardia", "grave"],
        "formas_pago": ["pago", "tarjeta", "efectivo", "transferencia", "precio", "costo"],
        "primera_vez": ["primera vez", "nuevo paciente", "que llevar", "que traer"],
        "cancelar_turno": ["cancelar", "reagendar", "cambiar turno", "modificar"],
        "recetas_certificados": ["receta", "certificado", "prescripcion"]
    }

    for faq_key, words in keywords.items():
        if any(word in consulta_lower for word in words):
            return FAQS[faq_key]

    return None
