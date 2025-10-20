"""
Voice Call Bot - Integración con Twilio Voice para llamadas telefónicas
Permite conversaciones de voz bidireccionales en tiempo real.
"""

import os
import logging
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv

from .ai_assistant import AIAssistant

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Configuración de Flask
app = Flask(__name__)

# Configuración de Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Sesiones de llamadas activas
call_sessions = {}


def get_or_create_session(call_sid: str) -> AIAssistant:
    """
    Obtiene o crea una sesión de asistente para una llamada.

    Args:
        call_sid: ID único de la llamada de Twilio

    Returns:
        Instancia de AIAssistant
    """
    if call_sid not in call_sessions:
        call_sessions[call_sid] = AIAssistant()
        logger.info(f"Nueva sesión de llamada creada: {call_sid}")

    return call_sessions[call_sid]


def clear_session(call_sid: str):
    """Limpia la sesión de una llamada."""
    if call_sid in call_sessions:
        del call_sessions[call_sid]
        logger.info(f"Sesión de llamada eliminada: {call_sid}")


@app.route('/webhook/voice', methods=['POST'])
def voice_webhook():
    """
    Webhook principal para llamadas entrantes.
    Se ejecuta cuando alguien llama al número de Twilio.
    """
    try:
        call_sid = request.values.get('CallSid', '')
        from_number = request.values.get('From', '')

        logger.info(f"Llamada entrante de {from_number} (CallSid: {call_sid})")

        # Crear respuesta de voz
        response = VoiceResponse()

        # Obtener o crear sesión
        assistant = get_or_create_session(call_sid)

        # Saludo inicial
        saludo = assistant.obtener_saludo_inicial()

        # Usar Gather para capturar la respuesta del usuario
        gather = Gather(
            input='speech',
            action='/webhook/voice/process',
            method='POST',
            language='es-AR',
            speechTimeout='auto',
            timeout=5,
            hints='turno, cardiología, especialidad, doctor, médico, horario'
        )

        gather.say(
            saludo,
            voice='Polly.Lucia',
            language='es-AR'
        )

        response.append(gather)

        # Si no hay respuesta, repetir
        response.redirect('/webhook/voice/no-input')

        return Response(str(response), mimetype='application/xml')

    except Exception as e:
        logger.error(f"Error en webhook de voz: {e}", exc_info=True)
        response = VoiceResponse()
        response.say(
            "Ocurrió un error. Por favor, intente nuevamente.",
            voice='Polly.Lucia',
            language='es-AR'
        )
        response.hangup()
        return Response(str(response), mimetype='application/xml')


@app.route('/webhook/voice/process', methods=['POST'])
def process_speech():
    """
    Procesa la respuesta del usuario (speech-to-text de Twilio).
    """
    try:
        call_sid = request.values.get('CallSid', '')
        speech_result = request.values.get('SpeechResult', '')
        confidence = request.values.get('Confidence', '0')

        logger.info(f"[{call_sid}] Usuario dijo: {speech_result} (confianza: {confidence})")

        # Si no se entendió bien, pedir repetición
        if not speech_result or float(confidence) < 0.5:
            response = VoiceResponse()
            gather = Gather(
                input='speech',
                action='/webhook/voice/process',
                method='POST',
                language='es-AR',
                speechTimeout='auto',
                timeout=5
            )
            gather.say(
                "Disculpe, no le escuché bien. ¿Podría repetir?",
                voice='Polly.Lucia',
                language='es-AR'
            )
            response.append(gather)
            response.redirect('/webhook/voice/no-input')
            return Response(str(response), mimetype='application/xml')

        # Obtener asistente de la sesión
        assistant = get_or_create_session(call_sid)

        # Verificar si el usuario quiere terminar
        if any(word in speech_result.lower() for word in ['adiós', 'adios', 'chau', 'colgar', 'gracias nada más']):
            response = VoiceResponse()
            response.say(
                "Perfecto, que tenga un buen día. Hasta luego.",
                voice='Polly.Lucia',
                language='es-AR'
            )
            response.hangup()
            clear_session(call_sid)
            return Response(str(response), mimetype='application/xml')

        # Procesar mensaje con el asistente
        respuesta_texto = assistant.procesar_mensaje(speech_result)

        logger.info(f"[{call_sid}] Asistente responde: {respuesta_texto[:100]}...")

        # Crear respuesta de voz
        response = VoiceResponse()

        # Continuar conversación
        gather = Gather(
            input='speech',
            action='/webhook/voice/process',
            method='POST',
            language='es-AR',
            speechTimeout='auto',
            timeout=5,
            hints='turno, cardiología, especialidad, doctor, médico, horario, DNI, obra social'
        )

        gather.say(
            respuesta_texto,
            voice='Polly.Lucia',
            language='es-AR'
        )

        response.append(gather)

        # Si no hay respuesta, ir a no-input
        response.redirect('/webhook/voice/no-input')

        return Response(str(response), mimetype='application/xml')

    except Exception as e:
        logger.error(f"Error procesando speech: {e}", exc_info=True)
        response = VoiceResponse()
        response.say(
            "Ocurrió un error. Por favor, intente nuevamente.",
            voice='Polly.Lucia',
            language='es-AR'
        )
        response.hangup()
        return Response(str(response), mimetype='application/xml')


@app.route('/webhook/voice/no-input', methods=['POST'])
def no_input():
    """
    Se ejecuta cuando el usuario no dice nada.
    """
    call_sid = request.values.get('CallSid', '')

    logger.info(f"[{call_sid}] No input detectado")

    response = VoiceResponse()

    gather = Gather(
        input='speech',
        action='/webhook/voice/process',
        method='POST',
        language='es-AR',
        speechTimeout='auto',
        timeout=5
    )

    gather.say(
        "¿Sigue ahí? ¿En qué puedo ayudarlo?",
        voice='Polly.Lucia',
        language='es-AR'
    )

    response.append(gather)

    # Si sigue sin respuesta, despedirse
    response.say(
        "Parece que se cortó la comunicación. Llamenos nuevamente cuando lo necesite. Hasta luego.",
        voice='Polly.Lucia',
        language='es-AR'
    )
    response.hangup()

    clear_session(call_sid)

    return Response(str(response), mimetype='application/xml')


@app.route('/webhook/voice/status', methods=['POST'])
def call_status():
    """
    Webhook para eventos de la llamada (completada, fallida, etc.).
    """
    call_sid = request.values.get('CallSid', '')
    call_status = request.values.get('CallStatus', '')

    logger.info(f"[{call_sid}] Estado de llamada: {call_status}")

    # Limpiar sesión cuando la llamada termina
    if call_status in ['completed', 'failed', 'busy', 'no-answer']:
        clear_session(call_sid)

    return '', 200


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servicio está funcionando."""
    return {'status': 'ok', 'service': 'voice_call_bot'}, 200


@app.route('/', methods=['GET'])
def index():
    """Página de inicio."""
    return """
    <html>
        <head><title>Asistente Telefónico de Voz - Clínica San Rafael</title></head>
        <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #2c3e50;">📞 Asistente Telefónico de Voz</h1>
                <h2 style="color: #3498db;">Clínica San Rafael</h2>

                <p style="color: #555; line-height: 1.6;">
                    Sistema de atención telefónica automatizada con inteligencia artificial.
                </p>

                <h3 style="color: #2c3e50;">🎙️ Cómo funciona:</h3>
                <ol style="color: #555; line-height: 1.8;">
                    <li>Llama al número configurado</li>
                    <li>Habla naturalmente con el asistente</li>
                    <li>El asistente responde con voz sintetizada</li>
                    <li>Conversación en tiempo real</li>
                </ol>

                <h3 style="color: #2c3e50;">✨ Funciones:</h3>
                <ul style="color: #555; line-height: 1.8;">
                    <li>Gestión de turnos médicos</li>
                    <li>Consultas sobre especialidades</li>
                    <li>Verificación de coberturas</li>
                    <li>Respuestas a preguntas frecuentes</li>
                    <li>Conversación natural bidireccional</li>
                </ul>

                <h3 style="color: #2c3e50;">🔊 Voces disponibles:</h3>
                <p style="color: #555;">
                    <strong>Polly.Lucia</strong> (Español argentino, voz femenina)
                </p>

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
    logger.info(f"Iniciando servidor de llamadas de voz en {host}:{port}")
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
