# 💬 Guía Rápida: Bot de Voz por WhatsApp (2 minutos)

## ✅ Lo que necesitas
- [ ] Servicio en Render activo: https://tu-app.onrender.com
- [ ] Cuenta de Twilio (gratis)

---

## Paso 1: Activar WhatsApp Sandbox (1 minuto)

1. Ir a: https://console.twilio.com/
2. En el menú: **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Verás un **código QR** y un mensaje como:
   ```
   join [palabra-aleatoria]
   ```
4. Desde tu WhatsApp:
   - **Escanear el código QR**, O
   - Agregar el número a contactos y enviar: `join palabra-aleatoria`
5. Recibirás: ✅ *"Twilio Sandbox: You are all set!"*

---

## Paso 2: Configurar Webhook (30 segundos)

1. En la misma página de Twilio Sandbox
2. En **"When a message comes in"**:
   ```
   https://tu-app.onrender.com/webhook/whatsapp
   ```
3. Method: **POST**
4. Click **Save**

---

## Paso 3: ¡USAR EL BOT! 🎉

### Enviar Audio de Voz:

1. Abre WhatsApp
2. Busca la conversación con el número de Twilio
3. **Mantén presionado el botón de micrófono** 🎤
4. Habla: *"Hola, quiero sacar un turno para cardiología"*
5. Suelta para enviar
6. **El bot transcribe tu audio y responde por texto** ✅

### También funciona con texto:

Puedes escribir:
```
Hola, quiero un turno
```

Y el bot responde igual.

---

## 💡 Cómo Funciona

```
Tú → Audio de voz 🎤
       ↓
Bot → Transcribe a texto (Google STT)
       ↓
Bot → Procesa con IA (OpenAI)
       ↓
Bot → Responde por TEXTO 💬
```

**Es como una llamada, pero por WhatsApp**

---

## 🎯 Ejemplos de Uso

**Audio 1:** *"Hola, ¿tienen turnos disponibles?"*
→ Bot responde: "Sí, ¿para qué especialidad necesita el turno?"

**Audio 2:** *"Para traumatología"*
→ Bot responde: "Perfecto, ¿qué día le viene bien?"

**Audio 3:** *"El miércoles"*
→ Bot responde: "Excelente, ¿me puede dar su nombre completo?"

**Texto:** "Juan Pérez"
→ Bot responde: "¿Y su número de documento?"

---

## 🔍 Troubleshooting

### Bot no responde

1. Verificar webhook en Twilio:
   ```bash
   curl https://tu-app.onrender.com/health
   ```
   Debe responder: `{"status": "ok"}`

2. Verificar logs en Render:
   - Dashboard → Logs
   - Buscar: `INFO - Mensaje recibido de whatsapp:+...`

### Audio no se transcribe

- **Hablar más claro y despacio**
- **Reducir ruido de fondo**
- El audio debe ser en **español**
- Probar enviar mensaje de texto primero para verificar que el bot responde

### "Disculpe, no pude entender el audio"

- Grabar audio más largo (mínimo 2 segundos)
- Hablar más fuerte
- Verificar que el audio se escuche bien antes de enviar

---

## ✅ Checklist Final

- [ ] WhatsApp Sandbox activado
- [ ] Mensaje `join palabra` enviado
- [ ] Confirmación recibida de Twilio
- [ ] Webhook configurado: `https://tu-app.onrender.com/webhook/whatsapp`
- [ ] Audio de prueba enviado
- [ ] Bot responde

---

## 💰 Costos

- **WhatsApp Sandbox:** GRATIS (ilimitado)
- **Transcripción de audio:** GRATIS (Google)
- **OpenAI respuestas:** ~$0.002 por conversación
- **Total:** Prácticamente GRATIS

**Diferencia con llamadas telefónicas:**
- ❌ Llamadas: $0.13/minuto (~$8 por hora)
- ✅ WhatsApp: $0.002 por conversación (~$2 por 1000 conversaciones)

---

## 🎉 ¡Listo!

**Envía un audio de voz por WhatsApp y habla con tu bot.**

Es exactamente igual que una llamada, pero:
- ✅ GRATIS
- ✅ Sin restricciones geográficas
- ✅ Funciona desde cualquier país
- ✅ No necesitas upgrade de Twilio

**Webhook:** `https://tu-app.onrender.com/webhook/whatsapp`

🚀 **Eso es todo.**
