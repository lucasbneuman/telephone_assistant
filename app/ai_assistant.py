"""
AI Assistant - Lógica del asistente conversacional con OpenAI
Este módulo maneja la inteligencia del asistente telefónico.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Importar configuración
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import prompts, datos_clinica

logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()


class AIAssistant:
    """Asistente de IA para la clínica médica."""

    def __init__(self, model: str = None):
        """
        Inicializa el asistente de IA.

        Args:
            model: Modelo de OpenAI a usar (default: gpt-4o-mini desde .env)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en variables de entorno")

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # Historial de conversación
        self.conversation_history: List[Dict[str, str]] = []

        # Datos extraídos del paciente
        self.patient_data = {
            "nombre_completo": None,
            "dni": None,
            "cobertura": None,
            "tipo_consulta": None,
            "especialidad": None,
            "fecha_preferida": None,
            "sintomas_graves": False,
            "turno_confirmado": None
        }

        # Inicializar conversación con prompt del sistema
        self._inicializar_sistema()

        logger.info(f"AIAssistant inicializado con modelo: {self.model}")

    def _inicializar_sistema(self):
        """Inicializa el sistema con el prompt base y contexto de la clínica."""
        # Obtener información de la clínica
        info_clinica = self._generar_contexto_clinica()

        # Prompt del sistema completo
        system_prompt = f"""{prompts.obtener_prompt_sistema()}

INFORMACIÓN DE LA CLÍNICA QUE DEBES CONOCER:
{info_clinica}

HORA ACTUAL: {datetime.now().strftime('%H:%M')}
FECHA ACTUAL: {datetime.now().strftime('%d/%m/%Y')}

Recuerda: Eres el primer punto de contacto del paciente. Sé empático, profesional y eficiente.
"""

        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

    def _generar_contexto_clinica(self) -> str:
        """Genera un resumen de la información de la clínica para el contexto."""
        context = f"""
CLÍNICA: {datos_clinica.CLINICA['nombre']}
DIRECCIÓN: {datos_clinica.CLINICA['direccion']}
TELÉFONO: {datos_clinica.CLINICA['telefono']}

HORARIOS:
- Lunes a Viernes: {datos_clinica.HORARIOS['lunes_viernes']}
- Sábados: {datos_clinica.HORARIOS['sabados']}
- Domingos y Feriados: {datos_clinica.HORARIOS['domingos']}

ESPECIALIDADES DISPONIBLES:
"""
        for key, esp in datos_clinica.ESPECIALIDADES.items():
            context += f"\n- {esp['nombre']}:"
            for medico in esp['medicos']:
                context += f"\n  * {medico['nombre']} - {', '.join(medico['dias'])} ({medico['horario']})"

        context += f"\n\nOBRAS SOCIALES ACEPTADAS: {', '.join(datos_clinica.OBRAS_SOCIALES)}"
        context += f"\n\nPREPAGAS ACEPTADAS: {', '.join(datos_clinica.PREPAGAS)}"
        context += f"\n\nPRECIO CONSULTA PARTICULAR: ${datos_clinica.PRECIOS['consulta_particular']}"

        # Turnos disponibles
        turnos = datos_clinica.generar_turnos_mock()
        context += f"\n\nTURNOS DISPONIBLES:"
        context += f"\n- Hoy ({turnos['hoy']['fecha']}): {turnos['hoy']['disponibles'] if turnos['hoy']['disponibles'] else 'COMPLETO'}"
        context += f"\n- Mañana ({turnos['manana']['fecha']}): {', '.join(turnos['manana']['disponibles'])}"
        context += f"\n- Pasado mañana ({turnos['pasado_manana']['fecha']}): {', '.join(turnos['pasado_manana']['disponibles'])}"

        return context

    def procesar_mensaje(self, mensaje_usuario: str) -> str:
        """
        Procesa un mensaje del usuario y genera una respuesta.

        Args:
            mensaje_usuario: Mensaje del usuario

        Returns:
            Respuesta del asistente
        """
        try:
            # Agregar mensaje del usuario al historial
            self.conversation_history.append({
                "role": "user",
                "content": mensaje_usuario
            })

            # Extraer información del mensaje
            self._extraer_informacion(mensaje_usuario)

            # Verificar si hay síntomas graves
            if self.patient_data["sintomas_graves"]:
                respuesta = self._manejar_urgencia()
            else:
                # Generar respuesta con OpenAI
                respuesta = self._generar_respuesta()

            # Agregar respuesta al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": respuesta
            })

            logger.info(f"Usuario: {mensaje_usuario[:50]}... | Asistente: {respuesta[:50]}...")

            return respuesta

        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return "Disculpe, tuve un problema procesando su solicitud. ¿Podría repetir?"

    def _generar_respuesta(self) -> str:
        """Genera una respuesta usando OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=300
            )

            respuesta = response.choices[0].message.content
            return respuesta

        except Exception as e:
            logger.error(f"Error llamando a OpenAI API: {e}")
            return "Disculpe, estoy teniendo problemas técnicos. ¿Podría intentar nuevamente?"

    def _extraer_informacion(self, mensaje: str):
        """
        Extrae información clave del mensaje del usuario.

        Args:
            mensaje: Mensaje del usuario
        """
        # Intentar extraer información usando OpenAI
        try:
            extraction_prompt = f"""{prompts.PROMPT_EXTRACCION_DATOS}

Conversación hasta ahora:
{self._obtener_resumen_conversacion()}

Último mensaje del usuario: "{mensaje}"

Datos actuales del paciente: {json.dumps(self.patient_data, ensure_ascii=False)}

Extrae SOLO la nueva información del último mensaje y actualiza los datos. Si un campo ya tiene valor y no se menciona en el último mensaje, mantén el valor anterior.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en extracción de información estructurada."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )

            # Parsear respuesta JSON
            extracted_data = json.loads(response.choices[0].message.content)

            # Actualizar datos del paciente (solo campos no nulos)
            for key, value in extracted_data.items():
                if value is not None and key in self.patient_data:
                    self.patient_data[key] = value

            logger.info(f"Datos extraídos: {self.patient_data}")

        except json.JSONDecodeError as e:
            logger.warning(f"Error parseando JSON de extracción: {e}")
        except Exception as e:
            logger.error(f"Error extrayendo información: {e}")

    def _manejar_urgencia(self) -> str:
        """Maneja casos de urgencia médica."""
        return """Por su seguridad, le recomiendo que acuda inmediatamente a la guardia del Hospital Fernández (Av. Cerviño 3356) o al Hospital Rivadavia (Av. Gral. Las Heras 2670), ambos con guardia 24hs. También puede llamar al 107 para emergencias médicas.

Nuestra clínica no cuenta con servicio de urgencias. ¿Necesita la dirección de algún hospital cercano?"""

    def _obtener_resumen_conversacion(self) -> str:
        """Obtiene un resumen de la conversación para contexto."""
        # Obtener últimos 4 mensajes (sin contar el system)
        mensajes_recientes = self.conversation_history[-4:]
        resumen = ""
        for msg in mensajes_recientes:
            if msg["role"] != "system":
                role = "Usuario" if msg["role"] == "user" else "Asistente"
                resumen += f"{role}: {msg['content']}\n"
        return resumen

    def obtener_saludo_inicial(self) -> str:
        """Genera el saludo inicial del asistente."""
        hora = datetime.now().hour

        if 6 <= hora < 12:
            saludo = "Buenos días"
        elif 12 <= hora < 20:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"

        return f"{saludo}, Clínica San Rafael, ¿en qué puedo ayudarlo?"

    def verificar_cobertura(self, cobertura: str) -> Tuple[bool, str]:
        """
        Verifica si la clínica trabaja con una cobertura específica.

        Args:
            cobertura: Nombre de la obra social o prepaga

        Returns:
            Tupla (acepta: bool, mensaje: str)
        """
        acepta, tipo, nombre = datos_clinica.verificar_cobertura(cobertura)

        if acepta:
            return True, f"Sí, trabajamos con {nombre}. Con gusto lo atendemos."
        else:
            precio = datos_clinica.PRECIOS['consulta_particular']
            return False, f"Lamentablemente no tenemos convenio con esa obra social. La consulta sería particular, con un costo de ${precio}. ¿Desea agendar de todas formas?"

    def obtener_turnos_disponibles(self, cuando: str = "manana") -> Dict:
        """
        Obtiene los turnos disponibles.

        Args:
            cuando: "hoy", "manana" o "pasado_manana"

        Returns:
            Diccionario con turnos disponibles
        """
        return datos_clinica.obtener_turnos_disponibles(cuando)

    def confirmar_turno(
        self,
        fecha: str,
        hora: str,
        especialidad: str,
        medico: str = None
    ) -> str:
        """
        Confirma un turno y genera mensaje de confirmación.

        Args:
            fecha: Fecha del turno
            hora: Hora del turno
            especialidad: Especialidad
            medico: Nombre del médico (opcional)

        Returns:
            Mensaje de confirmación
        """
        self.patient_data["turno_confirmado"] = {
            "fecha": fecha,
            "hora": hora,
            "especialidad": especialidad,
            "medico": medico
        }

        medico_str = f"con {medico}" if medico else f"en {especialidad}"
        nombre = self.patient_data.get("nombre_completo", "")

        confirmacion = f"""Perfecto{', ' + nombre.split()[0] if nombre else ''}, su turno quedó confirmado para el {fecha} a las {hora} {medico_str}.

Por favor llegue 10 minutos antes con su DNI"""

        if self.patient_data.get("cobertura") and self.patient_data["cobertura"] != "particular":
            confirmacion += f" y su credencial de {self.patient_data['cobertura']}"

        confirmacion += f".\n\nLa clínica está en {datos_clinica.CLINICA['direccion']}."

        return confirmacion

    def buscar_faq(self, consulta: str) -> Optional[str]:
        """
        Busca una respuesta en las FAQs.

        Args:
            consulta: Consulta del usuario

        Returns:
            Respuesta de la FAQ o None
        """
        faq = datos_clinica.buscar_faq(consulta)
        if faq:
            return faq["respuesta"]
        return None

    def obtener_datos_paciente(self) -> Dict:
        """Retorna los datos recolectados del paciente."""
        return self.patient_data.copy()

    def reiniciar_conversacion(self):
        """Reinicia la conversación (para una nueva llamada)."""
        self._inicializar_sistema()
        self.patient_data = {
            "nombre_completo": None,
            "dni": None,
            "cobertura": None,
            "tipo_consulta": None,
            "especialidad": None,
            "fecha_preferida": None,
            "sintomas_graves": False,
            "turno_confirmado": None
        }
        logger.info("Conversación reiniciada")

    def obtener_historial(self) -> List[Dict[str, str]]:
        """Retorna el historial completo de la conversación."""
        return self.conversation_history.copy()

    def generar_resumen_llamada(self) -> str:
        """Genera un resumen de la llamada para logs."""
        resumen = f"""
=== RESUMEN DE LLAMADA ===
Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

DATOS DEL PACIENTE:
- Nombre: {self.patient_data.get('nombre_completo') or 'No proporcionado'}
- DNI: {self.patient_data.get('dni') or 'No proporcionado'}
- Cobertura: {self.patient_data.get('cobertura') or 'No proporcionado'}
- Tipo de consulta: {self.patient_data.get('tipo_consulta') or 'No identificado'}
- Especialidad solicitada: {self.patient_data.get('especialidad') or 'No especificada'}

TURNO:
"""
        if self.patient_data.get('turno_confirmado'):
            turno = self.patient_data['turno_confirmado']
            resumen += f"- CONFIRMADO para {turno['fecha']} a las {turno['hora']}\n"
            resumen += f"- Especialidad: {turno['especialidad']}\n"
            if turno.get('medico'):
                resumen += f"- Médico: {turno['medico']}\n"
        else:
            resumen += "- No se confirmó turno\n"

        resumen += f"\nTotal de mensajes intercambiados: {len(self.conversation_history) - 1}\n"
        resumen += "========================\n"

        return resumen


# ==================== FUNCIONES DE UTILIDAD ====================

def crear_asistente(model: str = None) -> AIAssistant:
    """
    Crea una instancia del asistente.

    Args:
        model: Modelo de OpenAI a usar

    Returns:
        Instancia de AIAssistant
    """
    return AIAssistant(model=model)


# Para pruebas directas del módulo
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("=== Prueba del AI Assistant ===\n")

    try:
        assistant = crear_asistente()
        print(f"Asistente: {assistant.obtener_saludo_inicial()}\n")

        # Simulación de conversación
        mensajes_prueba = [
            "Hola, necesito un turno para cardiología",
            "Me llamo Juan Pérez",
            "Tengo OSDE",
            "Mañana a las 10 me viene bien",
            "Mi DNI es 12345678"
        ]

        for msg in mensajes_prueba:
            print(f"Usuario: {msg}")
            respuesta = assistant.procesar_mensaje(msg)
            print(f"Asistente: {respuesta}\n")

        # Mostrar resumen
        print(assistant.generar_resumen_llamada())

    except ValueError as e:
        print(f"Error: {e}")
        print("Asegúrate de tener configurada la variable OPENAI_API_KEY en el archivo .env")
