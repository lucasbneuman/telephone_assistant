"""
Main - Punto de entrada principal del Asistente Telefónico
Este es el archivo principal para ejecutar el asistente.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.call_manager import CallManager

# Cargar variables de entorno
load_dotenv()


def configurar_logging(verbose: bool = False):
    """
    Configura el sistema de logging.

    Args:
        verbose: Si True, muestra logs detallados
    """
    nivel = logging.DEBUG if verbose else logging.INFO

    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configurar formato
    formato = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configurar logging
    logging.basicConfig(
        level=nivel,
        format=formato,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "asistente.log", encoding='utf-8')
        ]
    )


def verificar_configuracion():
    """
    Verifica que la configuración necesaria esté presente.

    Returns:
        True si la configuración es válida, False en caso contrario
    """
    # Verificar API key de OpenAI
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "tu_api_key_aqui":
        print("ERROR: No se encontró una API key válida de OpenAI")
        print("\nPor favor:")
        print("1. Copia el archivo .env.example a .env")
        print("2. Edita .env y coloca tu OPENAI_API_KEY")
        print("\nPuedes obtener una API key en: https://platform.openai.com/api-keys")
        return False

    return True


def modo_consola():
    """Ejecuta el asistente en modo consola (sin voz)."""
    print("\n" + "="*70)
    print(" ASISTENTE TELEFÓNICO - CLÍNICA SAN RAFAEL")
    print(" Modo: CONSOLA (Texto)")
    print("="*70)

    manager = CallManager(use_voice=False, log_conversations=True)
    manager.ejecutar_llamada_consola()


def modo_voz(tts_engine: str = "pyttsx3"):
    """
    Ejecuta el asistente con voz.

    Args:
        tts_engine: Motor TTS a usar ("pyttsx3" o "gtts")
    """
    print("\n" + "="*70)
    print(" ASISTENTE TELEFÓNICO - CLÍNICA SAN RAFAEL")
    print(f" Modo: VOZ (Motor TTS: {tts_engine})")
    print("="*70)

    manager = CallManager(
        use_voice=True,
        tts_engine=tts_engine,
        log_conversations=True
    )
    manager.ejecutar_llamada_con_voz()


def modo_demo():
    """Ejecuta una conversación de demostración."""
    print("\n" + "="*70)
    print(" DEMO - ASISTENTE TELEFÓNICO")
    print("="*70)
    print("\nEjecutando conversación de ejemplo...\n")

    manager = CallManager(use_voice=False, log_conversations=True)

    # Conversación de ejemplo
    conversacion_demo = [
        ("iniciar", None),
        ("Hola, quería sacar un turno para cardiología", None),
        ("Me llamo Juan Pérez", None),
        ("Tengo OSDE", None),
        ("Mañana a las 10 me viene bien", None),
        ("Mi DNI es 12345678", None),
        ("¿Cómo llego a la clínica?", None),
        ("No, eso es todo. Gracias", None)
    ]

    print("-"*70)
    saludo = manager.iniciar_llamada()
    print(f"\n[ASISTENTE]: {saludo}\n")

    for mensaje, _ in conversacion_demo[1:]:
        print(f"[PACIENTE]: {mensaje}")
        respuesta, continuar = manager.procesar_turno_conversacion(mensaje)
        print(f"[ASISTENTE]: {respuesta}\n")

        if not continuar:
            break

    print("-"*70)
    print("\n" + manager.assistant.generar_resumen_llamada())


def mostrar_ayuda():
    """Muestra información de ayuda."""
    ayuda = """
╔════════════════════════════════════════════════════════════════╗
║  ASISTENTE TELEFÓNICO CON IA - CLÍNICA SAN RAFAEL            ║
╚════════════════════════════════════════════════════════════════╝

MODOS DE USO:

1. MODO CONSOLA (Recomendado para pruebas)
   python -m app.main --modo consola

   - Interacción por texto en la terminal
   - No requiere micrófono ni bocinas
   - Ideal para desarrollo y pruebas

2. MODO VOZ
   python -m app.main --modo voz

   - Usa reconocimiento y síntesis de voz
   - Requiere micrófono funcional
   - Experiencia más realista

3. MODO DEMO
   python -m app.main --modo demo

   - Ejecuta una conversación de ejemplo
   - No requiere interacción
   - Útil para ver capacidades del asistente

OPCIONES ADICIONALES:

  --tts-engine [pyttsx3|gtts]
      Motor de síntesis de voz (default: pyttsx3)
      - pyttsx3: Offline, más rápido
      - gtts: Online, mejor calidad

  --verbose, -v
      Muestra logs detallados

  --help, -h
      Muestra esta ayuda

EJEMPLOS:

  # Iniciar en modo consola
  python -m app.main

  # Iniciar con voz usando Google TTS
  python -m app.main --modo voz --tts-engine gtts

  # Ejecutar demo con logs detallados
  python -m app.main --modo demo --verbose

CONFIGURACIÓN:

  Antes de usar, asegúrate de:
  1. Copiar .env.example a .env
  2. Configurar tu OPENAI_API_KEY en .env

EDITAR COMPORTAMIENTO:

  - Prompts del asistente: config/prompts.py
  - Datos de la clínica: config/datos_clinica.py

Para más información: README.md
"""
    print(ayuda)


def main():
    """Función principal."""
    # Parser de argumentos
    parser = argparse.ArgumentParser(
        description="Asistente Telefónico con IA - Clínica San Rafael",
        add_help=False
    )

    parser.add_argument(
        '--modo',
        choices=['consola', 'voz', 'demo'],
        default='consola',
        help='Modo de ejecución (default: consola)'
    )

    parser.add_argument(
        '--tts-engine',
        choices=['pyttsx3', 'gtts'],
        default='pyttsx3',
        help='Motor de síntesis de voz (default: pyttsx3)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar logs detallados'
    )

    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Mostrar ayuda'
    )

    args = parser.parse_args()

    # Mostrar ayuda si se solicita
    if args.help:
        mostrar_ayuda()
        return

    # Configurar logging
    configurar_logging(args.verbose)

    # Banner
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  ASISTENTE TELEFÓNICO CON IA - CLÍNICA SAN RAFAEL".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")

    # Verificar configuración
    if not verificar_configuracion():
        sys.exit(1)

    # Ejecutar según modo
    try:
        if args.modo == 'consola':
            modo_consola()
        elif args.modo == 'voz':
            modo_voz(args.tts_engine)
        elif args.modo == 'demo':
            modo_demo()

    except KeyboardInterrupt:
        print("\n\n[SISTEMA] Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error fatal: {e}", exc_info=True)
        print(f"\n[ERROR] Ocurrió un error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
