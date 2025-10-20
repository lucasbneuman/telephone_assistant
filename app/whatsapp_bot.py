"""
WhatsApp Bot - Integración con Twilio para WhatsApp
Permite recibir mensajes de voz y texto por WhatsApp y responder con el asistente.
"""

import os
import logging
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import tempfile
import requests

from .ai_assistant import AIAssistant
from .voice_handler import VoiceHandler

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración de Flask
app = Flask(__name__)

# Configuración de Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

# Diccionario para mantener sesiones de usuarios
user_sessions = {}


def get_or_create_session(phone_number: str) -> AIAssistant:
    """
    Obtiene o crea una sesión de asistente para un número de teléfono.

    Args:
        phone_number: Número de teléfono del usuario

    Returns:
        Instancia de AIAssistant
    """
    if phone_number not in user_sessions:
        user_sessions[phone_number] = AIAssistant()
        logger.info(f"Nueva sesión creada para {phone_number}")

    return user_sessions[phone_number]


def clear_session(phone_number: str):
    """Limpia la sesión de un usuario."""
    if phone_number in user_sessions:
        del user_sessions[phone_number]
        logger.info(f"Sesión eliminada para {phone_number}")


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Webhook para recibir mensajes de WhatsApp desde Twilio.
    """
    try:
        # Obtener datos del mensaje
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        media_url = request.values.get('MediaUrl0', None)  # URL del audio si hay
        media_content_type = request.values.get('MediaContentType0', '')

        logger.info(f"Mensaje recibido de {from_number}: {incoming_msg[:50]}...")

        # Crear respuesta de Twilio
        resp = MessagingResponse()

        # Obtener o crear sesión del usuario
        assistant = get_or_create_session(from_number)

        # Procesar mensaje de voz si hay audio
        if media_url and 'audio' in media_content_type:
            logger.info(f"Procesando audio de {from_number}")

            # Descargar audio
            audio_response = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

            if audio_response.status_code == 200:
                # Guardar audio temporalmente
                with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_audio:
                    temp_audio.write(audio_response.content)
                    temp_audio_path = temp_audio.name

                try:
                    # Convertir voz a texto
                    voice_handler = VoiceHandler()
                    success, text = voice_handler.speech_to_text_from_file(temp_audio_path)

                    if success:
                        incoming_msg = text
                        logger.info(f"Audio transcrito: {text}")
                    else:
                        resp.message("❌ No pude entender el audio. Por favor, intenta de nuevo o escribe tu mensaje.")
                        return Response(str(resp), mimetype='application/xml')

                finally:
                    # Limpiar archivo temporal
                    if os.path.exists(temp_audio_path):
                        os.unlink(temp_audio_path)
            else:
                resp.message("❌ No pude descargar el audio. Por favor, intenta de nuevo.")
                return Response(str(resp), mimetype='application/xml')

        # Si no hay mensaje de texto ni audio
        if not incoming_msg:
            resp.message("Por favor envía un mensaje de texto o de voz.")
            return Response(str(resp), mimetype='application/xml')

        # Comandos especiales
        if incoming_msg.lower() in ['reiniciar', 'reset', 'nuevo']:
            clear_session(from_number)
            assistant = get_or_create_session(from_number)
            resp.message("✅ Conversación reiniciada. " + assistant.obtener_saludo_inicial())
            return Response(str(resp), mimetype='application/xml')

        if incoming_msg.lower() in ['ayuda', 'help', 'comandos']:
            help_text = """🤖 *Asistente de Clínica San Rafael*

Puedo ayudarte con:
• 📅 Sacar turnos
• 🏥 Consultar especialidades
• 💳 Verificar coberturas
• 📍 Información de la clínica
• ❓ Responder preguntas

*Comandos:*
• *reiniciar* - Comenzar nueva conversación
• *ayuda* - Ver este mensaje

¿En qué puedo ayudarte?"""
            resp.message(help_text)
            return Response(str(resp), mimetype='application/xml')

        # Procesar mensaje con el asistente
        response_text = assistant.procesar_mensaje(incoming_msg)

        # Enviar respuesta
        resp.message(response_text)

        # Si el usuario se despide, limpiar sesión después de un tiempo
        if any(word in incoming_msg.lower() for word in ['chau', 'adiós', 'adios', 'gracias nada más']):
            # La sesión se limpiará después de 5 minutos de inactividad
            pass

        logger.info(f"Respuesta enviada a {from_number}: {response_text[:50]}...")

        return Response(str(resp), mimetype='application/xml')

    except Exception as e:
        logger.error(f"Error en webhook de WhatsApp: {e}", exc_info=True)
        resp = MessagingResponse()
        resp.message("❌ Ocurrió un error. Por favor, intenta de nuevo en unos momentos.")
        return Response(str(resp), mimetype='application/xml')


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servicio está funcionando."""
    return {'status': 'ok', 'service': 'telephone_assistant'}, 200


@app.route('/', methods=['GET'])
def index():
    """Página de inicio."""
    return """
    <html>
        <head><title>Asistente Telefónico - Clínica San Rafael</title></head>
        <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #2c3e50;">🏥 Asistente Telefónico</h1>
                <h2 style="color: #3498db;">Clínica San Rafael</h2>
                <p style="color: #555; line-height: 1.6;">
                    Bot de WhatsApp para atención automatizada de pacientes.
                </p>
                <h3 style="color: #2c3e50;">📱 Cómo usar:</h3>
                <ol style="color: #555; line-height: 1.8;">
                    <li>Envía un mensaje de WhatsApp al número configurado</li>
                    <li>Puedes enviar texto o notas de voz</li>
                    <li>El asistente te responderá automáticamente</li>
                </ol>
                <h3 style="color: #2c3e50;">✨ Funciones:</h3>
                <ul style="color: #555; line-height: 1.8;">
                    <li>Gestión de turnos médicos</li>
                    <li>Consultas sobre especialidades</li>
                    <li>Verificación de coberturas</li>
                    <li>Respuestas a preguntas frecuentes</li>
                </ul>
                <div style="margin-top: 30px; padding: 15px; background: #ecf0f1; border-radius: 5px;">
                    <p style="margin: 0; color: #555;">
                        <strong>Estado:</strong> <span style="color: #27ae60;">✓ Servicio activo</span>
                    </p>
                </div>
            </div>
        </body>
    </html>
    """


def run_server(host='0.0.0.0', port=5000, debug=False):
    """
    Inicia el servidor Flask.

    Args:
        host: Host donde escuchar
        port: Puerto donde escuchar
        debug: Modo debug
    """
    logger.info(f"Iniciando servidor en {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Verificar configuración de Twilio
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.error("TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN deben estar configurados en .env")
        exit(1)

    # Iniciar servidor
    port = int(os.getenv('PORT', 5000))
    run_server(host='0.0.0.0', port=port, debug=False)
