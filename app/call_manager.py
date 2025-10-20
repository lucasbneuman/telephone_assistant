"""
Call Manager - Gestión de llamadas telefónicas
Este módulo coordina el flujo de una llamada: recibe audio, procesa con IA, responde con voz.
"""

import os
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from .ai_assistant import AIAssistant
from .voice_handler import VoiceHandler

logger = logging.getLogger(__name__)


class CallManager:
    """Gestiona el flujo completo de una llamada telefónica."""

    def __init__(
        self,
        use_voice: bool = True,
        tts_engine: str = "pyttsx3",
        log_conversations: bool = True
    ):
        """
        Inicializa el gestor de llamadas.

        Args:
            use_voice: Si True, usa síntesis y reconocimiento de voz
            tts_engine: Motor de TTS a usar ("pyttsx3" o "gtts")
            log_conversations: Si True, guarda logs de las conversaciones
        """
        self.use_voice = use_voice
        self.log_conversations = log_conversations

        # Inicializar componentes
        self.assistant = AIAssistant()

        if use_voice:
            self.voice_handler = VoiceHandler(tts_engine=tts_engine)
        else:
            self.voice_handler = None

        # Estado de la llamada
        self.call_active = False
        self.call_start_time = None
        self.message_count = 0

        logger.info("CallManager inicializado")

    def iniciar_llamada(self) -> str:
        """
        Inicia una nueva llamada.

        Returns:
            Saludo inicial del asistente
        """
        self.call_active = True
        self.call_start_time = datetime.now()
        self.message_count = 0

        saludo = self.assistant.obtener_saludo_inicial()

        if self.use_voice and self.voice_handler:
            self.voice_handler.text_to_speech(saludo)

        logger.info("Llamada iniciada")
        return saludo

    def procesar_turno_conversacion(self, input_usuario: Optional[str] = None) -> tuple[str, bool]:
        """
        Procesa un turno de la conversación.

        Args:
            input_usuario: Texto del usuario (si None y use_voice=True, usa micrófono)

        Returns:
            Tupla (respuesta_asistente: str, continuar: bool)
        """
        if not self.call_active:
            return "La llamada no está activa. Llame a iniciar_llamada() primero.", False

        # Obtener input del usuario
        if input_usuario is None and self.use_voice:
            # Reconocimiento de voz
            success, texto = self.voice_handler.speech_to_text(timeout=10)

            if not success:
                respuesta_error = "Disculpe, no pude escucharlo bien. ¿Puede repetir?"
                if self.voice_handler:
                    self.voice_handler.text_to_speech(respuesta_error)
                return respuesta_error, True

            input_usuario = texto
        elif input_usuario is None:
            raise ValueError("Se debe proporcionar input_usuario cuando use_voice=False")

        # Verificar si el usuario quiere terminar
        if self._es_despedida(input_usuario):
            return self.finalizar_llamada(), False

        # Procesar con el asistente
        respuesta = self.assistant.procesar_mensaje(input_usuario)

        # Reproducir respuesta si está habilitada la voz
        if self.use_voice and self.voice_handler:
            self.voice_handler.text_to_speech(respuesta)

        self.message_count += 1

        return respuesta, True

    def finalizar_llamada(self) -> str:
        """
        Finaliza la llamada actual.

        Returns:
            Mensaje de despedida
        """
        if not self.call_active:
            return "No hay llamada activa."

        # Generar despedida
        despedida = "Perfecto, que tenga un buen día. Hasta luego."

        if self.use_voice and self.voice_handler:
            self.voice_handler.text_to_speech(despedida)

        # Calcular duración
        if self.call_start_time:
            duracion = datetime.now() - self.call_start_time
            logger.info(f"Llamada finalizada. Duración: {duracion.seconds} segundos")

        # Guardar log si está habilitado
        if self.log_conversations:
            self._guardar_log_conversacion()

        # Limpiar estado
        self.call_active = False
        self.message_count = 0

        return despedida

    def reiniciar_para_nueva_llamada(self):
        """Reinicia el gestor para una nueva llamada."""
        if self.call_active:
            self.finalizar_llamada()

        self.assistant.reiniciar_conversacion()
        logger.info("CallManager listo para nueva llamada")

    def ejecutar_llamada_consola(self):
        """
        Ejecuta una llamada en modo consola (sin voz, solo texto).
        Útil para pruebas y desarrollo.
        """
        print("\n" + "="*60)
        print("SIMULADOR DE LLAMADA - CLÍNICA SAN RAFAEL")
        print("="*60)
        print("Escribe 'salir', 'chau' o 'adios' para terminar la llamada")
        print("="*60 + "\n")

        # Iniciar llamada
        saludo = self.iniciar_llamada()
        print(f"[ASISTENTE]: {saludo}\n")

        # Loop de conversación
        while self.call_active:
            try:
                # Obtener input del usuario
                user_input = input("[USTED]: ").strip()

                if not user_input:
                    continue

                # Procesar turno
                respuesta, continuar = self.procesar_turno_conversacion(user_input)

                print(f"[ASISTENTE]: {respuesta}\n")

                if not continuar:
                    break

            except KeyboardInterrupt:
                print("\n\n[SISTEMA] Llamada interrumpida por el usuario")
                self.finalizar_llamada()
                break
            except Exception as e:
                logger.error(f"Error durante la llamada: {e}")
                print(f"[ERROR] Ocurrió un error: {e}")
                break

        # Mostrar resumen
        print("\n" + "="*60)
        print(self.assistant.generar_resumen_llamada())
        print("="*60 + "\n")

    def ejecutar_llamada_con_voz(self):
        """
        Ejecuta una llamada usando reconocimiento y síntesis de voz.
        """
        if not self.use_voice:
            print("Error: CallManager no fue inicializado con use_voice=True")
            return

        print("\n" + "="*60)
        print("LLAMADA CON VOZ - CLÍNICA SAN RAFAEL")
        print("="*60)
        print("Presiona Ctrl+C para terminar la llamada")
        print("="*60 + "\n")

        # Probar micrófono
        if not self.voice_handler.test_microphone():
            print("Error: No se pudo acceder al micrófono")
            return

        # Iniciar llamada
        saludo = self.iniciar_llamada()
        print(f"[ASISTENTE]: {saludo}")

        # Loop de conversación
        while self.call_active:
            try:
                print("\n[Escuchando...]")

                # Procesar turno (None = usar micrófono)
                respuesta, continuar = self.procesar_turno_conversacion(None)

                print(f"[ASISTENTE]: {respuesta}")

                if not continuar:
                    break

            except KeyboardInterrupt:
                print("\n\n[SISTEMA] Llamada interrumpida")
                self.finalizar_llamada()
                break
            except Exception as e:
                logger.error(f"Error durante la llamada: {e}")
                print(f"[ERROR] {e}")
                break

        # Mostrar resumen
        print("\n" + "="*60)
        print(self.assistant.generar_resumen_llamada())
        print("="*60 + "\n")

    def obtener_datos_llamada(self) -> dict:
        """
        Obtiene información sobre la llamada actual.

        Returns:
            Diccionario con datos de la llamada
        """
        duracion = None
        if self.call_start_time:
            duracion = (datetime.now() - self.call_start_time).seconds

        return {
            "activa": self.call_active,
            "inicio": self.call_start_time.isoformat() if self.call_start_time else None,
            "duracion_segundos": duracion,
            "mensajes_intercambiados": self.message_count,
            "datos_paciente": self.assistant.obtener_datos_paciente()
        }

    def _es_despedida(self, texto: str) -> bool:
        """
        Verifica si el texto del usuario indica que quiere terminar.

        Args:
            texto: Texto del usuario

        Returns:
            True si es una despedida
        """
        texto_lower = texto.lower().strip()
        despedidas = [
            "adios", "adiós", "chau", "hasta luego", "nos vemos",
            "salir", "terminar", "colgar", "gracias, nada más",
            "no, gracias", "eso es todo", "nada más"
        ]

        return any(desp in texto_lower for desp in despedidas)

    def _guardar_log_conversacion(self):
        """Guarda el log de la conversación en un archivo."""
        try:
            # Crear directorio de logs si no existe
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            # Nombre del archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"llamada_{timestamp}.log"

            # Generar contenido del log
            resumen = self.assistant.generar_resumen_llamada()

            # Agregar conversación completa
            conversacion = "\n=== TRANSCRIPCIÓN COMPLETA ===\n"
            for msg in self.assistant.obtener_historial():
                if msg["role"] != "system":
                    role = "Usuario" if msg["role"] == "user" else "Asistente"
                    conversacion += f"\n[{role}]: {msg['content']}\n"

            # Guardar en archivo
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(resumen)
                f.write(conversacion)

            logger.info(f"Log de conversación guardado en: {log_file}")

            # También agregar a log consolidado
            log_consolidado = Path(os.getenv("LOG_FILE", "conversaciones.log"))
            with open(log_consolidado, 'a', encoding='utf-8') as f:
                f.write("\n" + resumen + "\n")

        except Exception as e:
            logger.error(f"Error guardando log de conversación: {e}")


# ==================== FUNCIONES DE UTILIDAD ====================

def crear_call_manager(
    use_voice: bool = False,
    tts_engine: str = "pyttsx3",
    log_conversations: bool = True
) -> CallManager:
    """
    Crea una instancia del gestor de llamadas.

    Args:
        use_voice: Si True, usa síntesis y reconocimiento de voz
        tts_engine: Motor de TTS a usar
        log_conversations: Si True, guarda logs

    Returns:
        Instancia de CallManager
    """
    return CallManager(
        use_voice=use_voice,
        tts_engine=tts_engine,
        log_conversations=log_conversations
    )


# Para pruebas directas del módulo
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Determinar modo
    modo = sys.argv[1] if len(sys.argv) > 1 else "consola"

    if modo == "voz":
        print("Iniciando en modo VOZ...")
        manager = crear_call_manager(use_voice=True)
        manager.ejecutar_llamada_con_voz()
    else:
        print("Iniciando en modo CONSOLA...")
        manager = crear_call_manager(use_voice=False)
        manager.ejecutar_llamada_consola()
