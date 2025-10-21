"""
Voice Handler - Manejo de TTS (Text-to-Speech) y STT (Speech-to-Text)
Este módulo gestiona la conversión de voz a texto y texto a voz.
"""

import speech_recognition as sr
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    pyttsx3 = None
from gtts import gTTS
import os
import tempfile
import platform
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class VoiceHandler:
    """Maneja la síntesis de voz (TTS) y reconocimiento de voz (STT)."""

    def __init__(self, tts_engine: str = "pyttsx3", language: str = "es"):
        """
        Inicializa el manejador de voz.

        Args:
            tts_engine: Motor de TTS a usar ("pyttsx3" o "gtts")
            language: Código de idioma (default: "es" para español)
        """
        self.tts_engine_type = tts_engine
        self.language = language
        self.recognizer = sr.Recognizer()

        # Inicializar motor TTS
        if tts_engine == "pyttsx3":
            if not PYTTSX3_AVAILABLE:
                logger.warning("pyttsx3 no está disponible. Usando gTTS como respaldo")
                self.tts_engine_type = "gtts"
                self.tts_engine = None
            else:
                try:
                    self.tts_engine = pyttsx3.init()
                    self._configurar_pyttsx3()
                except Exception as e:
                    logger.error(f"Error inicializando pyttsx3: {e}")
                    logger.info("Cambiando a gTTS como respaldo")
                    self.tts_engine_type = "gtts"
                    self.tts_engine = None
        else:
            self.tts_engine = None

        logger.info(f"VoiceHandler inicializado con motor TTS: {self.tts_engine_type}")

    def _configurar_pyttsx3(self):
        """Configura el motor pyttsx3 para voz en español."""
        if self.tts_engine is None:
            return

        try:
            # Configurar velocidad de habla
            rate = self.tts_engine.getProperty('rate')
            self.tts_engine.setProperty('rate', rate - 20)  # Un poco más lento

            # Configurar volumen
            self.tts_engine.setProperty('volume', 0.9)

            # Intentar configurar voz en español
            voices = self.tts_engine.getProperty('voices')

            # Buscar voz en español
            spanish_voice = None
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                    spanish_voice = voice.id
                    break
                # En Windows, buscar voces con ES
                if platform.system() == 'Windows' and 'ES' in voice.id:
                    spanish_voice = voice.id
                    break

            if spanish_voice:
                self.tts_engine.setProperty('voice', spanish_voice)
                logger.info(f"Voz en español configurada: {spanish_voice}")
            else:
                logger.warning("No se encontró voz en español, usando voz por defecto")

        except Exception as e:
            logger.error(f"Error configurando pyttsx3: {e}")

    def text_to_speech(self, text: str, play_audio: bool = True) -> Optional[str]:
        """
        Convierte texto a voz.

        Args:
            text: Texto a convertir
            play_audio: Si True, reproduce el audio; si False, solo guarda

        Returns:
            Ruta del archivo de audio generado (si se usó gTTS) o None
        """
        if not text:
            logger.warning("Texto vacío proporcionado para TTS")
            return None

        try:
            if self.tts_engine_type == "pyttsx3" and self.tts_engine:
                # Usar pyttsx3 (offline, más rápido)
                if play_audio:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                return None

            else:
                # Usar gTTS (online, mejor calidad)
                return self._gtts_speak(text, play_audio)

        except Exception as e:
            logger.error(f"Error en text_to_speech: {e}")
            return None

    def _gtts_speak(self, text: str, play_audio: bool = True) -> str:
        """
        Usa Google TTS para generar audio.

        Args:
            text: Texto a convertir
            play_audio: Si True, reproduce el audio

        Returns:
            Ruta del archivo de audio generado
        """
        try:
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_filename = temp_file.name
            temp_file.close()

            # Generar audio
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(temp_filename)

            if play_audio:
                # Reproducir audio (requiere un reproductor)
                if platform.system() == 'Windows':
                    os.system(f'start {temp_filename}')
                elif platform.system() == 'Darwin':  # macOS
                    os.system(f'afplay {temp_filename}')
                else:  # Linux
                    os.system(f'mpg123 {temp_filename}')

            return temp_filename

        except Exception as e:
            logger.error(f"Error en gTTS: {e}")
            return None

    def speech_to_text(
        self,
        audio_source: Optional[sr.AudioSource] = None,
        timeout: int = 5,
        phrase_time_limit: int = 10
    ) -> Tuple[bool, str]:
        """
        Convierte voz a texto usando micrófono o fuente de audio.

        Args:
            audio_source: Fuente de audio (si None, usa micrófono)
            timeout: Tiempo de espera para comenzar a hablar (segundos)
            phrase_time_limit: Tiempo máximo de grabación (segundos)

        Returns:
            Tupla (éxito: bool, texto: str)
        """
        try:
            if audio_source is None:
                # Usar micrófono por defecto
                with sr.Microphone() as source:
                    logger.info("Escuchando...")
                    # Ajustar ruido ambiental
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    # Escuchar
                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit
                    )
            else:
                # Usar fuente de audio proporcionada
                logger.info("Procesando audio...")
                audio = self.recognizer.record(audio_source)

            # Convertir a texto usando Google Speech Recognition (gratis)
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Texto reconocido: {text}")
            return True, text

        except sr.WaitTimeoutError:
            logger.warning("Timeout: No se detectó voz")
            return False, "Timeout: No se detectó voz en el tiempo especificado"

        except sr.UnknownValueError:
            logger.warning("No se pudo entender el audio")
            return False, "No se pudo entender el audio"

        except sr.RequestError as e:
            logger.error(f"Error en el servicio de reconocimiento: {e}")
            return False, f"Error en el servicio de reconocimiento: {e}"

        except Exception as e:
            logger.error(f"Error inesperado en speech_to_text: {e}")
            return False, f"Error: {e}"

    def speech_to_text_from_file(self, audio_file_path: str) -> Tuple[bool, str]:
        """
        Convierte un archivo de audio a texto.

        Args:
            audio_file_path: Ruta al archivo de audio

        Returns:
            Tupla (éxito: bool, texto: str)
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Texto reconocido del archivo: {text}")
                return True, text

        except sr.UnknownValueError:
            logger.warning("No se pudo entender el audio del archivo")
            return False, "No se pudo entender el audio"

        except sr.RequestError as e:
            logger.error(f"Error en el servicio de reconocimiento: {e}")
            return False, f"Error en el servicio: {e}"

        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {audio_file_path}")
            return False, f"Archivo no encontrado: {audio_file_path}"

        except Exception as e:
            logger.error(f"Error procesando archivo de audio: {e}")
            return False, f"Error: {e}"

    def test_microphone(self) -> bool:
        """
        Prueba si el micrófono está funcionando correctamente.

        Returns:
            True si el micrófono funciona, False en caso contrario
        """
        try:
            with sr.Microphone() as source:
                logger.info("Probando micrófono...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Micrófono funcionando correctamente")
                return True
        except Exception as e:
            logger.error(f"Error probando micrófono: {e}")
            return False

    def set_language(self, language: str):
        """
        Cambia el idioma del reconocimiento y síntesis de voz.

        Args:
            language: Código de idioma (ej: "es", "en")
        """
        self.language = language
        logger.info(f"Idioma cambiado a: {language}")


# ==================== FUNCIONES DE UTILIDAD ====================

def crear_voice_handler(
    tts_engine: str = "pyttsx3",
    language: str = "es"
) -> VoiceHandler:
    """
    Función helper para crear un VoiceHandler.

    Args:
        tts_engine: Motor TTS a usar ("pyttsx3" o "gtts")
        language: Código de idioma

    Returns:
        Instancia de VoiceHandler
    """
    return VoiceHandler(tts_engine=tts_engine, language=language)


def probar_voz(texto: str = "Hola, soy el asistente de Clínica San Rafael"):
    """
    Función de prueba rápida para TTS.

    Args:
        texto: Texto a sintetizar
    """
    vh = VoiceHandler(tts_engine="pyttsx3")
    print(f"Diciendo: {texto}")
    vh.text_to_speech(texto)


def probar_reconocimiento():
    """
    Función de prueba rápida para STT.
    """
    vh = VoiceHandler()
    print("Habla algo...")
    success, text = vh.speech_to_text(timeout=5)

    if success:
        print(f"Entendí: {text}")
    else:
        print(f"Error: {text}")


# Para pruebas directas del módulo
if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "tts":
            probar_voz()
        elif sys.argv[1] == "stt":
            probar_reconocimiento()
    else:
        print("Uso:")
        print("  python voice_handler.py tts   - Probar síntesis de voz")
        print("  python voice_handler.py stt   - Probar reconocimiento de voz")
