# ✅ PROYECTO LISTO - Llamadas de Voz

## 🎯 Sistema Implementado

**Asistente Telefónico con Llamadas de Voz en Tiempo Real**

### ✅ Funcionalidades:
- ✅ **Llamadas telefónicas reales**
- ✅ Usuario habla → Bot transcribe automáticamente
- ✅ Bot responde con voz sintetizada (español argentino)
- ✅ Conversación bidireccional en tiempo real
- ✅ Gestión de turnos, coberturas, FAQs
- ✅ Funciona 24/7 en la nube

---

## 📞 Cómo Funciona

```
1. Cliente LLAMA al número de teléfono
2. Twilio responde automáticamente
3. Bot SALUDA con voz: "Buenos días, Clínica San Rafael..."
4. Cliente HABLA: "Quiero un turno para cardiología"
5. Bot TRANSCRIBE y procesa con IA
6. Bot RESPONDE con voz: "Perfecto, ¿su nombre completo?"
7. Conversación continúa hasta finalizar
```

**Es una llamada real como con una recepcionista humana.**

---

## 📁 Archivos Clave

```
telephone_assistant/
├── app/
│   ├── voice_call_bot.py     ⭐ PRINCIPAL - Bot de llamadas
│   ├── ai_assistant.py       ✓ Lógica IA
│   ├── whatsapp_bot.py       📝 Alternativa (no se usa)
│   ├── voice_handler.py      ✓ Utilidades de voz
│   └── call_manager.py       ✓ (no se usa en voice)
│
├── config/
│   ├── prompts.py            📝 EDITAR - Comportamiento
│   └── datos_clinica.py      📝 EDITAR - Datos
│
├── Procfile                  → voice_call_bot
├── README.md                 ✓ Documentación completa
├── VOICE_CALLS_GUIDE.md      ⭐ Guía detallada
└── requirements.txt          ✓ Dependencias
```

---

## 🚀 Configuración en 3 Pasos

### Paso 1: Twilio (10 minutos)

1. **Crear cuenta:** https://console.twilio.com/
2. **Obtener credenciales:**
   - Account SID
   - Auth Token
3. **Obtener número:**
   - **Sandbox (GRATIS):** Usar número de prueba
   - **Producción:** Comprar número (~$1-2/mes)
4. **Verificar tu número** (si usas sandbox):
   - Phone Numbers → Verified Caller IDs
   - Agregar tu celular
   - Recibir código por llamada

### Paso 2: Render (10 minutos)

1. **Subir a GitHub:**
   ```bash
   git add .
   git commit -m "Voice call bot"
   git push origin main
   ```

2. **Deployar en Render:**
   - New Web Service
   - Conectar repo
   - Configurar variables de entorno:
     ```
     OPENAI_API_KEY = tu_key
     TWILIO_ACCOUNT_SID = tu_sid
     TWILIO_AUTH_TOKEN = tu_token
     ```

3. **Obtener URL:** `https://tu-bot.onrender.com`

### Paso 3: Conectar (5 minutos)

1. **En Twilio Console:**
   - Phone Numbers → Tu número
   - **A call comes in:**
     ```
     https://tu-bot.onrender.com/webhook/voice
     HTTP POST
     ```
   - **Save**

2. **¡Llamar y probar!**
   - Llamar al número de Twilio
   - Hablar con el bot

**Tiempo total: ~25 minutos**

---

## 💰 Costos (Por Minuto de Llamada)

```
Twilio Voice:        ~$0.0085/min
Speech-to-Text:      ~$0.02/min
Text-to-Speech:      ~$0.004/min
OpenAI (GPT-4o-mini):~$0.0015/min
--------------------------------
TOTAL:               ~$0.03/min
```

**Ejemplos mensuales:**
- 100 min/mes: ~$3 USD
- 500 min/mes: ~$15 USD
- 1000 min/mes: ~$30 USD

Más:
- Número de teléfono: $1-2/mes (opcional, sandbox es gratis)
- Render: Gratis o $7/mes

---

## 🎤 Ejemplo de Conversación Real

```
[Suena el teléfono...]

Bot: "Buenos días, Clínica San Rafael, ¿en qué puedo ayudarlo?"

Usuario: "Hola, necesito sacar un turno para cardiología"

Bot: "Perfecto, ¿me podría decir su nombre completo?"

Usuario: "María González"

Bot: "Gracias María. ¿Tiene alguna cobertura médica?"

Usuario: "Sí, OSDE"

Bot: "Excelente, trabajamos con OSDE. Tenemos disponibilidad
      para mañana a las diez, dos y media de la tarde, o
      cuatro de la tarde. ¿Cuál le viene mejor?"

Usuario: "Mañana a las diez"

Bot: "Perfecto María, confirmamos turno para mañana a las
      diez de la mañana con cardiología. ¿Me confirma su DNI?"

Usuario: "Doce millones trescientos cuarenta y cinco mil
         seiscientos setenta y ocho"

Bot: "Listo, su turno está confirmado. Por favor llegue
      diez minutos antes con DNI y credencial de OSDE.
      ¿Algo más en lo que pueda ayudarlo?"

Usuario: "No, eso es todo. Muchas gracias"

Bot: "Perfecto, que tenga un buen día. Hasta luego."

[Llamada finaliza]
```

---

## 📝 Personalización

### Cambiar la voz

En `app/voice_call_bot.py` línea ~80:

```python
voice='Polly.Lucia'    # Mujer argentina (ACTUAL)
voice='Polly.Miguel'   # Hombre argentino
voice='Polly.Lupe'     # Mujer mexicana
voice='Polly.Mia'      # Mujer española
```

### Editar datos de la clínica

`config/datos_clinica.py`:
```python
CLINICA = {
    "nombre": "Tu Clínica",
    "direccion": "Tu Dirección",
    ...
}
```

### Ajustar comportamiento

`config/prompts.py`:
```python
PROMPT_SISTEMA = """
Eres un asistente más formal/informal/etc...
"""
```

---

## 🔧 Testing Local

```bash
# 1. Activar entorno
source venv/bin/activate  # o venv\Scripts\activate

# 2. Ejecutar bot
python -m app.voice_call_bot

# 3. Para probar, necesitas ngrok:
ngrok http 5000

# 4. Usar URL de ngrok en webhook de Twilio temporalmente
```

---

## 📚 Documentación

### Lee PRIMERO:
1. **README.md** - Guía completa
2. **VOICE_CALLS_GUIDE.md** - Detalles técnicos

### Referencia:
- [Twilio Voice Docs](https://www.twilio.com/docs/voice)
- [Amazon Polly Voices](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html)

---

## 🎯 Diferencia con WhatsApp

| Característica | WhatsApp | Voice Calls (ACTUAL) |
|----------------|----------|----------------------|
| **Tipo** | Mensajes asíncronos | Llamada en tiempo real |
| **Usuario** | Escribe o envía audio | Habla en llamada |
| **Bot** | Responde texto | Responde con voz |
| **Experiencia** | Chat | Llamada telefónica |
| **Costo** | ~$0.005/mensaje | ~$0.03/minuto |
| **Archivo** | `whatsapp_bot.py` | `voice_call_bot.py` ⭐ |

**ACTUAL:** Voice Calls (ver `Procfile`)

**Para cambiar a WhatsApp:**
```bash
# En Procfile:
web: gunicorn app.whatsapp_bot:app
```

---

## ✅ Checklist

- [ ] Código en GitHub
- [ ] Cuenta Twilio creada
- [ ] Account SID y Auth Token obtenidos
- [ ] Número de Twilio obtenido (sandbox o comprado)
- [ ] Tu número verificado (si usas sandbox)
- [ ] Deployado en Render
- [ ] Variables de entorno configuradas
- [ ] Webhook configurado en Twilio
- [ ] Primera llamada de prueba realizada
- [ ] Bot responde correctamente

---

## 🐛 Problemas Comunes

### "No puedo llamar al bot"
- Verificar que tu número esté en Verified Caller IDs (sandbox)
- Ver logs en Twilio Console
- Verificar webhook configurado

### "El bot no me entiende"
- Hablar más claro y pausado
- Evitar ruido de fondo
- Ver transcripción en logs de Twilio

### "El bot no responde"
- Verificar OPENAI_API_KEY en Render
- Ver logs en Render dashboard
- Probar: `curl https://tu-url.onrender.com/health`

---

## 🎉 Resumen

```
✅ Sistema de llamadas de voz implementado
✅ Conversación bidireccional en tiempo real
✅ Transcripción automática (Twilio)
✅ Respuestas con voz (Amazon Polly)
✅ Procesamiento con IA (OpenAI)
✅ Listo para sandbox (gratis)
✅ Listo para producción
✅ Documentación completa
```

**Estado:** 🟢 LISTO PARA DEPLOYAR

**Próximo paso:** Lee `VOICE_CALLS_GUIDE.md` y sigue la guía paso a paso 📞

**Costo estimado:** ~$0.03/minuto + $7/mes Render (opcional)

---

**¿Dudas?** Todo está documentado en `VOICE_CALLS_GUIDE.md` 🚀
