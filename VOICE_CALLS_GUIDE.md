# 📞 Guía de Llamadas de Voz - Twilio Voice

Sistema de atención telefónica con IA que permite conversaciones de voz bidireccionales en tiempo real.

## 🎯 Cómo Funciona

```
Usuario → Llama al número → Twilio → Tu servidor → Asistente IA → Responde con voz
                                ↑                                      ↓
                                └──────── Conversación en tiempo real ──┘
```

### Flujo de la Llamada:

1. **Usuario llama** al número de Twilio
2. **Twilio responde** y ejecuta tu webhook
3. **Bot saluda** con voz sintetizada (Polly.Lucia - español argentino)
4. **Usuario habla** → Twilio transcribe en tiempo real (speech-to-text)
5. **Asistente procesa** con OpenAI GPT-4o-mini
6. **Bot responde** con voz sintetizada
7. **Conversación continúa** hasta que el usuario se despide o cuelga

---

## 🚀 Configuración Paso a Paso

### Paso 1: Obtener Número de Teléfono Twilio

#### Opción A: Número de Prueba (GRATIS - Sandbox)

1. Ir a https://console.twilio.com/
2. En el dashboard verás tu **número de prueba gratis**
3. Es algo como: `+1 (XXX) XXX-XXXX`
4. ⚠️ **Limitación**: Solo puedes llamar desde números verificados

**Verificar tu número:**
1. En Twilio Console: Phone Numbers → Verified Caller IDs
2. Click "Add a new Caller ID"
3. Ingresar tu número de celular
4. Recibirás llamada con código de verificación
5. Ingresar código
6. ✅ Ahora puedes llamar al bot desde ese número

#### Opción B: Comprar Número (Producción)

1. En Twilio Console: Phone Numbers → Buy a number
2. Buscar número en Argentina (o país que prefieras)
3. Filtrar por "Voice" capabilities
4. Comprar (~$1-2/mes)
5. Cualquier persona puede llamar a ese número

---

### Paso 2: Deployar en Render

Seguir los pasos de `DEPLOYMENT.md` pero asegurándote de que:

- ✅ `Procfile` dice: `web: gunicorn app.voice_call_bot:app`
- ✅ Variables de entorno configuradas en Render:
  ```
  OPENAI_API_KEY=tu_api_key
  TWILIO_ACCOUNT_SID=tu_account_sid
  TWILIO_AUTH_TOKEN=tu_auth_token
  PORT=10000
  ```

URL que obtendrás: `https://tu-servicio.onrender.com`

---

### Paso 3: Configurar Webhook en Twilio

1. Ir a Twilio Console
2. Phone Numbers → Manage → Active numbers
3. Click en tu número
4. En **Voice Configuration**:

   **A call comes in:**
   ```
   Webhook: https://tu-servicio.onrender.com/webhook/voice
   HTTP: POST
   ```

   **Call Status Changes:**
   ```
   Webhook: https://tu-servicio.onrender.com/webhook/voice/status
   HTTP: POST
   ```

5. **Save**

---

### Paso 4: ¡Probar!

1. **Llamar** al número de Twilio desde tu teléfono (verificado si es sandbox)
2. **Escuchar** el saludo del bot
3. **Hablar** naturalmente: "Quiero un turno para cardiología"
4. **Bot responde** con voz
5. **Continuar** la conversación

---

## 🎤 Voces Disponibles

Actualmente usando: **Polly.Lucia** (Amazon Polly)
- Idioma: Español argentino
- Género: Femenino
- Calidad: Alta (neural)

### Otras voces disponibles:

```python
# En app/voice_call_bot.py, cambiar:
voice='Polly.Lucia'    # Mujer argentina (actual)
voice='Polly.Miguel'   # Hombre argentino
voice='Polly.Lupe'     # Mujer mexicana
voice='Polly.Mia'      # Mujer española
```

---

## 💰 Costos

### Desarrollo con Sandbox
- **Número de prueba**: GRATIS
- **Llamadas entrantes**: $0.0085/min
- **Speech Recognition**: $0.02/min
- **Text-to-Speech (Polly)**: $0.004/min
- **OpenAI**: ~$0.0015/conversación

**Total:** ~$0.03 por minuto de llamada

### Producción
- **Número de teléfono**: ~$1-2/mes
- **Llamadas**: ~$0.0085-0.013/min (según país)
- **Resto igual**

**Ejemplo:** 100 minutos de llamadas al mes = ~$3-4 USD

---

## 🎯 Endpoints

```
GET  /                          → Página de inicio
POST /webhook/voice             → Llamada entrante (inicio)
POST /webhook/voice/process     → Procesar respuesta del usuario
POST /webhook/voice/no-input    → Usuario no dijo nada
POST /webhook/voice/status      → Estado de la llamada
GET  /health                    → Health check
```

---

## 🔧 Personalización

### Cambiar el saludo

Editar `config/prompts.py`:
```python
# El método obtener_saludo_inicial() del asistente
```

### Cambiar datos de la clínica

Editar `config/datos_clinica.py`:
```python
CLINICA = {
    "nombre": "Tu Clínica",
    ...
}
```

### Cambiar la voz

En `app/voice_call_bot.py`, buscar:
```python
voice='Polly.Lucia'
```

Y cambiar por otra voz de Amazon Polly.

### Ajustar timeout

```python
Gather(
    timeout=5,  # Segundos esperando respuesta
    speechTimeout='auto'  # Tiempo después de que deja de hablar
)
```

---

## 🐛 Troubleshooting

### La llamada no conecta

1. **Verificar webhook configurado:**
   ```bash
   curl https://tu-servicio.onrender.com/health
   ```
   Debe responder: `{"status":"ok"}`

2. **Verificar logs en Render:**
   - Ir al dashboard de Render
   - Ver logs en tiempo real
   - Buscar errores

3. **Verificar número verificado (sandbox):**
   - Tu número debe estar en Verified Caller IDs en Twilio

### El bot no entiende lo que digo

1. **Hablar más claro y pausado**
2. **Verificar que estás usando español:**
   ```python
   language='es-AR'  # En el código
   ```
3. **Ver logs de Twilio:**
   - Twilio Console → Monitor → Logs
   - Ver la transcripción que obtuvo

### El bot no responde

1. **Ver logs en Render**
2. **Verificar API key de OpenAI:**
   - Debe estar configurada en variables de entorno
3. **Probar endpoint directamente:**
   ```bash
   curl https://tu-servicio.onrender.com/health
   ```

### La voz suena cortada o robótica

- Esto es normal con voces standard
- Para mejor calidad: usar voces Neural de Polly (puede costar más)

---

## 📊 Monitoreo

### Ver llamadas en tiempo real

**Twilio Console:**
1. Monitor → Logs → Calls
2. Ver duración, estado, errores
3. Escuchar grabaciones (si las habilitas)

**Render Dashboard:**
1. Tu servicio → Logs
2. Ver logs en tiempo real
3. Buscar errores de la aplicación

---

## 🎓 Ejemplo de Conversación

```
[SUENA EL TELÉFONO]

Bot: "Buenos días, Clínica San Rafael, ¿en qué puedo ayudarlo?"

Usuario: "Hola, quiero sacar un turno para cardiología"

Bot: "Perfecto, ¿me podría decir su nombre completo?"

Usuario: "Juan Pérez"

Bot: "Gracias Juan. ¿Tiene alguna obra social o prepaga?"

Usuario: "Tengo OSDE"

Bot: "Excelente, trabajamos con OSDE. Tenemos disponibilidad para
      cardiología: mañana a las diez de la mañana, dos y media de la
      tarde, o cuatro de la tarde. ¿Cuál le viene mejor?"

Usuario: "Mañana a las diez"

Bot: "Perfecto, entonces confirmamos turno para mañana a las diez de
      la mañana con cardiología. ¿Me confirma su DNI para registrar
      el turno?"

Usuario: "Doce millones trescientos cuarenta y cinco mil seiscientos
         setenta y ocho"

Bot: "Listo Juan, su turno quedó confirmado para mañana a las diez
      de la mañana en Clínica San Rafael, Avenida Libertador mil
      doscientos treinta y cuatro. Por favor llegue diez minutos antes
      con su DNI y credencial de OSDE. ¿Algo más en lo que pueda
      ayudarlo?"

Usuario: "No, eso es todo. Muchas gracias"

Bot: "Perfecto, que tenga un buen día. Hasta luego."

[LLAMADA TERMINA]
```

---

## 🚀 Siguientes Pasos

### Para Mejorar:

1. **Grabar llamadas** (opcional):
   ```python
   response.record(
       transcribe=True,
       maxLength=3600
   )
   ```

2. **Enviar SMS de confirmación**:
   ```python
   client = Client(account_sid, auth_token)
   client.messages.create(
       to=user_phone,
       from_=twilio_number,
       body="Confirmamos su turno..."
   )
   ```

3. **Horario de atención**:
   - Verificar hora del día
   - Fuera de horario: mensaje diferente

4. **Cola de espera**:
   - Si múltiples llamadas simultáneas
   - Música en espera

---

## 📞 Diferencia con WhatsApp

| Característica | WhatsApp (anterior) | Llamadas de Voz (actual) |
|----------------|---------------------|--------------------------|
| **Tipo** | Mensajes asíncronos | Conversación en tiempo real |
| **Usuario envía** | Texto o nota de voz | Habla en tiempo real |
| **Bot responde** | Solo texto | Voz sintetizada |
| **Experiencia** | Chat | Llamada telefónica |
| **Costo** | ~$0.005/mensaje | ~$0.03/minuto |
| **Mejor para** | Consultas no urgentes | Atención inmediata |

---

## ✅ Checklist de Configuración

- [ ] Código deployado en Render
- [ ] Variables de entorno configuradas
- [ ] Número de Twilio obtenido (prueba o comprado)
- [ ] Tu número verificado (si usas sandbox)
- [ ] Webhook configurado en Twilio
- [ ] Llamada de prueba realizada
- [ ] Bot responde correctamente
- [ ] Conversación fluye bien

---

## 💡 Tips

1. **Hablar claramente**: El reconocimiento de voz funciona mejor con pronunciación clara
2. **Pausas**: El bot espera que termines de hablar (speechTimeout)
3. **Despedirse**: Di "adiós" o "gracias, nada más" para terminar la llamada
4. **Reintentos**: Si no te entiende, habla más despacio
5. **Ruido ambiente**: Llamar desde lugar silencioso para mejor reconocimiento

---

## 🎉 ¡Listo!

Tu sistema de llamadas de voz está configurado. Los pacientes pueden:
- ✅ Llamar a un número de teléfono
- ✅ Hablar naturalmente con el asistente
- ✅ Recibir respuestas con voz
- ✅ Gestionar turnos, consultar info, etc.

**Todo funciona 24/7 automáticamente.**

---

**¿Problemas?** Revisa los logs en Render y Twilio Console.
