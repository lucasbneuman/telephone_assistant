"""
Script de prueba local para verificar que todo funciona antes de deployar.
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("VERIFICACIÓN DEL PROYECTO")
print("="*60)
print()

# 1. Verificar variables de entorno
print("1. Variables de entorno:")
openai_key = os.getenv('OPENAI_API_KEY')
twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_token = os.getenv('TWILIO_AUTH_TOKEN')

print(f"   OPENAI_API_KEY: {'✓ Configurada' if openai_key else '✗ NO configurada'}")
print(f"   TWILIO_ACCOUNT_SID: {'✓ Configurada' if twilio_sid else '✗ NO configurada'}")
print(f"   TWILIO_AUTH_TOKEN: {'✓ Configurada' if twilio_token else '✗ NO configurada'}")
print()

# 2. Verificar imports
print("2. Verificando imports:")
try:
    import flask
    print("   Flask: ✓")
except ImportError:
    print("   Flask: ✗ NO instalada")

try:
    import openai
    print("   OpenAI: ✓")
except ImportError:
    print("   OpenAI: ✗ NO instalada")

try:
    import twilio
    print("   Twilio: ✓")
except ImportError:
    print("   Twilio: ✗ NO instalada")

try:
    from app.ai_assistant import AIAssistant
    print("   AIAssistant: ✓")
except Exception as e:
    print(f"   AIAssistant: ✗ Error - {e}")

try:
    from app.whatsapp_bot import app
    print("   WhatsApp Bot: ✓")
except Exception as e:
    print(f"   WhatsApp Bot: ✗ Error - {e}")

print()

# 3. Probar AI Assistant
print("3. Probando AI Assistant:")
try:
    if openai_key and openai_key != 'tu_api_key_aqui':
        from app.ai_assistant import AIAssistant
        assistant = AIAssistant()
        print("   ✓ Instancia creada correctamente")

        # Probar mensaje
        respuesta = assistant.procesar_mensaje("Hola")
        print(f"   ✓ Respuesta recibida: {respuesta[:50]}...")
    else:
        print("   ⚠ Omitiendo prueba (API key no configurada)")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()
print("="*60)
print("RESUMEN")
print("="*60)

if openai_key and twilio_sid and twilio_token:
    print("✓ Proyecto listo para deployar")
    print()
    print("Próximos pasos:")
    print("1. Subir a GitHub: git push origin main")
    print("2. Deployar en Render siguiendo DEPLOYMENT.md")
    print("3. Configurar webhook en Twilio")
else:
    print("⚠ Faltan configuraciones:")
    if not openai_key or openai_key == 'tu_api_key_aqui':
        print("   - Configurar OPENAI_API_KEY en .env")
    if not twilio_sid or twilio_sid == 'tu_account_sid_aqui':
        print("   - Configurar TWILIO_ACCOUNT_SID en .env")
    if not twilio_token or twilio_token == 'tu_auth_token_aqui':
        print("   - Configurar TWILIO_AUTH_TOKEN en .env")

print()
print("="*60)
