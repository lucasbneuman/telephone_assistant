# 📞 Asistente Telefónico con IA - Llamadas de Voz

Asistente inteligente para clínicas que atiende **llamadas telefónicas reales** usando IA (OpenAI GPT-4o-mini) y Twilio Voice.

## 🚀 Características

- ✅ **Llamadas de voz bidireccionales en tiempo real**
- ✅ Usuario habla → Bot transcribe automáticamente
- ✅ Bot responde con voz sintetizada (español argentino)
- ✅ Gestión de turnos médicos
- ✅ Verificación de coberturas
- ✅ Respuestas automáticas con IA
- ✅ Sesiones por llamada
- ✅ Despliegue en Render
- ✅ Funciona 24/7

## 📋 Requisitos

- Cuenta de OpenAI (API Key)
- Cuenta de Twilio (para llamadas)
- Python 3.12+
- Cuenta de Render (para deployment)

## 🎯 Cómo Funciona

```
1. Cliente llama al número de teléfono
2. Twilio responde automáticamente
3. Bot saluda con voz: "Buenos días, Clínica San Rafael..."
4. Cliente habla: "Quiero un turno para cardiología"
5. Bot transcribe y procesa con IA
6. Bot responde con voz: "Perfecto, ¿me podría decir su nombre?"
7. Conversación continúa hasta finalizar
```

**Es una llamada telefónica real, como hablar con una recepcionista.**

## 🔧 Configuración Local

### 1. Clonar repositorio

```bash
git clone <tu-repo>
cd telephone_assistant
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env`:

```env
OPENAI_API_KEY=tu_api_key_aqui
OPENAI_MODEL=gpt-4o-mini

TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui

PORT=5000
```

### 5. Ejecutar localmente

```bash
python -m app.voice_call_bot
```

El servidor estará en `http://localhost:5000`

Para probarlo necesitas ngrok para exponer tu localhost a internet.

## 🌐 Deploy en Render

### 1. Subir a GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Crear Web Service en Render

1. Ir a https://render.com
2. New → Web Service
3. Conectar tu repositorio
4. Render detectará automáticamente `render.yaml`

### 3. Configurar variables de entorno

En Render dashboard:

```
OPENAI_API_KEY = tu_api_key
TWILIO_ACCOUNT_SID = tu_account_sid
TWILIO_AUTH_TOKEN = tu_auth_token
PORT = 10000
```

### 4. Deploy

Render desplegará automáticamente. Obtendrás URL:
```
https://tu-servicio.onrender.com
```

## 📱 Configurar Twilio Voice

### 1. Crear cuenta Twilio

Ir a https://console.twilio.com/ y registrarse (gratis)

### 2. Obtener número de teléfono

**Opción A - Sandbox (GRATIS para pruebas):**
- Usar número de prueba que te da Twilio
- Solo puedes llamar desde números verificados
- Perfecto para desarrollo

**Opción B - Comprar número (Producción):**
- Phone Numbers → Buy a number
- Buscar número en tu país
- Costo: ~$1-2/mes
- Cualquiera puede llamar

### 3. Configurar Webhook

En Twilio Console → Phone Numbers → Tu número:

**A call comes in:**
```
https://tu-servicio.onrender.com/webhook/voice
HTTP POST
```

**Call Status Changes:**
```
https://tu-servicio.onrender.com/webhook/voice/status
HTTP POST
```

**Save**

### 4. Verificar tu número (si usas sandbox)

1. Phone Numbers → Verified Caller IDs
2. Add a Caller ID
3. Ingresar tu celular
4. Recibirás llamada con código
5. Verificar

### 5. ¡Llamar y probar!

Llama al número de Twilio desde tu teléfono y habla con el bot.

## 💬 Ejemplo de Conversación

```
[Llamas al número]

Bot: "Buenos días, Clínica San Rafael, ¿en qué puedo ayudarlo?"

Tú: "Hola, necesito un turno para cardiología"

Bot: "Perfecto, ¿me podría decir su nombre completo?"

Tú: "María González"

Bot: "Gracias María. ¿Tiene alguna cobertura médica?"

Tú: "Sí, tengo OSDE"

Bot: "Excelente, trabajamos con OSDE. Tenemos disponibilidad
      para mañana a las 10, 14:30 o 16 horas. ¿Cuál le sirve?"

Tú: "Mañana a las 10"

Bot: "Perfecto, confirmamos turno para mañana a las 10 con
      cardiología. ¿Me confirma su DNI?"

Tú: "12345678"

Bot: "Listo María, su turno está confirmado. Por favor llegue
      10 minutos antes con DNI y credencial. ¿Algo más?"

Tú: "No, gracias"

Bot: "Perfecto, que tenga un buen día. Hasta luego."

[Llamada finaliza]
```

## 📝 Personalización

### Cambiar datos de la clínica

Editar `config/datos_clinica.py`:

```python
CLINICA = {
    "nombre": "Tu Clínica",
    "direccion": "Tu Dirección",
    ...
}
```

### Ajustar comportamiento del asistente

Editar `config/prompts.py`:

```python
PROMPT_SISTEMA = """Tu prompt personalizado..."""
```

### Cambiar la voz

En `app/voice_call_bot.py`:

```python
voice='Polly.Lucia'    # Mujer argentina (actual)
voice='Polly.Miguel'   # Hombre argentino
voice='Polly.Lupe'     # Mujer mexicana
```

Ver voces disponibles: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html

## 🏗️ Estructura del Proyecto

```
telephone_assistant/
├── app/
│   ├── voice_call_bot.py     # Bot de llamadas (principal)
│   ├── ai_assistant.py       # Lógica IA con OpenAI
│   ├── voice_handler.py      # Procesamiento de voz
│   ├── call_manager.py       # Gestión de conversaciones
│   └── whatsapp_bot.py       # Bot de WhatsApp (alternativo)
├── config/
│   ├── prompts.py            # Prompts del asistente
│   └── datos_clinica.py      # Datos de la clínica
├── requirements.txt          # Dependencias
├── Procfile                  # Config para Render
├── render.yaml               # Config para deploy
├── runtime.txt               # Versión de Python
├── README.md                 # Este archivo
└── VOICE_CALLS_GUIDE.md      # Guía detallada de voz
```

## 🔍 Endpoints

- `GET /` - Página de inicio
- `POST /webhook/voice` - Llamada entrante (inicio)
- `POST /webhook/voice/process` - Procesar respuesta del usuario
- `POST /webhook/voice/no-input` - Usuario no respondió
- `POST /webhook/voice/status` - Estado de la llamada
- `GET /health` - Health check

## 💰 Costos

### OpenAI
- Modelo: gpt-4o-mini
- ~$0.0015 USD por conversación

### Twilio Voice
- Número de teléfono: ~$1-2/mes (opcional, sandbox es gratis)
- Llamadas entrantes: ~$0.0085/minuto
- Speech-to-Text: ~$0.02/minuto
- Text-to-Speech (Polly): ~$0.004/minuto

**Total por minuto de llamada: ~$0.03 USD**

**Ejemplo:**
- 100 minutos de llamadas al mes: ~$3 USD (Twilio) + $1.50 (OpenAI) = **$4.50/mes**
- Más número de teléfono: +$1-2/mes
- Render: Gratis (o $7/mes para no tener sleep)

### Render
- Plan gratuito disponible (con sleep después de 15 min inactividad)
- Plan Starter: $7/mes (sin sleep)

## 🐛 Troubleshooting

### No puedo llamar al bot

1. **Verificar que el webhook está configurado:**
   ```bash
   curl https://tu-servicio.onrender.com/health
   ```

2. **Si usas sandbox, verificar que tu número está en Verified Caller IDs**

3. **Ver logs en Render y Twilio Console**

### El bot no me entiende

- Hablar claro y pausado
- Evitar ruido de fondo
- Ver logs de transcripción en Twilio Console

### El bot no responde

- Verificar `OPENAI_API_KEY` en Render
- Ver logs en Render dashboard
- Probar endpoint `/health`

## 📚 Documentación Adicional

- **VOICE_CALLS_GUIDE.md** - Guía completa de llamadas de voz
- **DEPLOYMENT.md** - Guía de deployment general
- [OpenAI API](https://platform.openai.com/docs)
- [Twilio Voice API](https://www.twilio.com/docs/voice)
- [Render Docs](https://render.com/docs)

## 🎯 Comparación: WhatsApp vs Llamadas

El proyecto incluye ambas opciones:

| Característica | WhatsApp Bot | Voice Calls |
|----------------|--------------|-------------|
| **Archivo** | `whatsapp_bot.py` | `voice_call_bot.py` |
| **Tipo** | Mensajes (texto/audio) | Llamada en tiempo real |
| **Usuario** | Envía texto o nota de voz | Habla en tiempo real |
| **Bot** | Responde texto | Responde con voz |
| **Costo** | ~$0.005/mensaje | ~$0.03/minuto |
| **Mejor para** | Consultas asíncronas | Atención inmediata |

**Actual en producción:** Voice Calls (ver `Procfile`)

Para cambiar a WhatsApp:
```bash
# En Procfile:
web: gunicorn app.whatsapp_bot:app
```

## 📄 Licencia

Proyecto de demostración. Uso libre.

## 🤝 Contribuciones

Pull requests bienvenidos.

---

**Desarrollado para Clínica San Rafael**

**Estado:** 🟢 Listo para producción con llamadas de voz
