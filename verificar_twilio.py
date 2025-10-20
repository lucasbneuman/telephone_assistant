"""
Script para verificar tu configuración de Twilio y número disponible
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

print("="*60)
print("VERIFICACIÓN DE TWILIO")
print("="*60)
print()

# Obtener credenciales
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

if not account_sid or not auth_token:
    print("❌ Error: Credenciales no encontradas en .env")
    exit(1)

print(f"✓ Account SID: {account_sid}")
print(f"✓ Auth Token: {auth_token[:8]}...")
print()

try:
    # Crear cliente Twilio
    client = Client(account_sid, auth_token)

    # Obtener información de la cuenta
    account = client.api.accounts(account_sid).fetch()
    print(f"✓ Cuenta activa: {account.friendly_name}")
    print(f"✓ Estado: {account.status}")
    print()

    # Obtener números de teléfono
    print("NÚMEROS DISPONIBLES:")
    print("-"*60)

    numbers = client.incoming_phone_numbers.list()

    if numbers:
        for number in numbers:
            print(f"\n📞 Número: {number.phone_number}")
            print(f"   Nombre: {number.friendly_name}")
            print(f"   Capacidades: ", end="")
            capabilities = []
            if number.capabilities.get('voice'):
                capabilities.append("Voz ✓")
            if number.capabilities.get('sms'):
                capabilities.append("SMS ✓")
            print(", ".join(capabilities))

            # Mostrar webhook configurado
            if number.voice_url:
                print(f"   Webhook de voz: {number.voice_url}")
            else:
                print(f"   Webhook de voz: ⚠️  NO CONFIGURADO")
    else:
        print("⚠️  No tienes números asignados")
        print()
        print("OPCIONES:")
        print("1. Obtener número Trial gratuito:")
        print("   → https://console.twilio.com/us1/develop/phone-numbers/manage/search")
        print()
        print("2. Si eres cuenta Trial, ya deberías tener uno asignado.")
        print("   Verifica en: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming")

    print()
    print("-"*60)
    print()

    # Obtener números verificados (Caller IDs)
    print("NÚMEROS VERIFICADOS (Caller IDs):")
    print("-"*60)

    caller_ids = client.outgoing_caller_ids.list()

    if caller_ids:
        for caller_id in caller_ids:
            print(f"✓ {caller_id.phone_number} ({caller_id.friendly_name})")
    else:
        print("⚠️  No tienes números verificados")
        print()
        print("Para verificar tu celular:")
        print("1. Ir a: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
        print("2. Click en '+' para agregar")
        print("3. Ingresar tu número de celular")
        print("4. Recibir código por llamada")
        print("5. Verificar")

    print()
    print("="*60)
    print("SIGUIENTE PASO:")
    print("="*60)

    if numbers:
        print(f"""
1. Tu número de Twilio: {numbers[0].phone_number}

2. Verifica tu celular en:
   https://console.twilio.com/us1/develop/phone-numbers/manage/verified

3. Llama al número de Twilio desde tu celular verificado

4. ¡El bot responderá!
""")
    else:
        print("""
1. Ve a Twilio Console
2. Deberías tener un número Trial asignado automáticamente
3. Si no, búscalo en la consola
4. Una vez que lo tengas, vuelve a ejecutar este script
""")

except Exception as e:
    print(f"❌ Error conectando con Twilio: {e}")
    print()
    print("Verifica que tus credenciales sean correctas")

print()
