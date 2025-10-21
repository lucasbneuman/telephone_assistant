# 📞 Guía Rápida: Llamadas Telefónicas (5 minutos)

## ✅ Pre-requisitos
- [ ] Servicio en Render activo y funcionando
- [ ] Cuenta de Twilio creada
- [ ] OpenAI API Key configurada

---

## Paso 1: Comprar Número de Twilio

1. Ir a: https://console.twilio.com/
2. Click **Phone Numbers** → **Manage** → **Buy a number**
3. Seleccionar país: **United States**
4. Marcar: ✅ **Voice**
5. Click **Search**
6. Elegir cualquier número
7. Click **Buy** (gratis en trial)
8. Click **Buy this number**

✅ **Anotar tu número:** `+1234567890`

---

## Paso 2: Configurar el Número para Llamadas

1. En Twilio Console: **Phone Numbers** → **Manage** → **Active numbers**
2. Click en tu número recién comprado
3. Scroll down hasta **Voice Configuration**
4. Configurar:

```
A call comes in: Webhook
URL: https://tu-app.onrender.com/webhook/voice
HTTP Method: POST
```

5. Click **Save Configuration**

---

## Paso 3: Verificar tu Número (Solo Trial Account)

Si estás usando cuenta trial:

1. Twilio Console: **Phone Numbers** → **Manage** → **Verified Caller IDs**
2. Click **Add a new Caller ID**
3. Ingresar TU número de teléfono personal
4. Recibirás una llamada con un código
5. Ingresar el código
6. ✅ Verificado

---

## Paso 4: ¡LLAMAR!

1. **Llamar al número de Twilio** que compraste
2. Si estás en trial, escucharás: *"You have a trial account. Press any key to continue."*
3. **Presiona cualquier tecla**
4. El bot te saludará: *"Buenos días/tardes, Clínica San Rafael, ¿en qué puedo ayudarlo?"*
5. **Habla naturalmente**
6. Para terminar, di: **"Adiós"** o **"Gracias, nada más"**

---

## 🔍 Troubleshooting

### No escucho nada / Error de Twilio

**Verificar webhook:**
```bash
curl https://tu-app.onrender.com/webhook/voice
```
Debe devolver XML (TwiML)

**Verificar logs en Render:**
- Dashboard → Tu servicio → Logs
- Buscar: `INFO - Llamada recibida de...`

### El bot no me escucha / Dice "No pude escucharlo"

- Hablar más fuerte y claro
- Reducir ruido de fondo
- Hablar más despacio

### Error: "Number you dialed is not in service"

- Verificar que el número esté activo en Twilio Console
- Verificar que el webhook esté configurado correctamente

---

## 💰 Costos Trial

- **Número de Twilio:** Gratis en trial
- **Llamadas:** Gastará de tu crédito de $15 USD
- **Costo por llamada:** ~$0.13 por minuto
- **Puedes hacer:** ~115 minutos de prueba

---

## ✅ Checklist Final

- [ ] Número comprado en Twilio
- [ ] Webhook configurado: `https://tu-app.onrender.com/webhook/voice`
- [ ] Tu número personal verificado (si es trial)
- [ ] Llamada al número funciona
- [ ] Bot responde y conversa

---

## 🎉 ¡Listo!

Llama al número de Twilio y habla con tu bot.

**URL del webhook:** `https://tu-app.onrender.com/webhook/voice`

**Eso es todo.** 🚀
