# 🚀 Guía de Deployment - Render + Twilio WhatsApp

Esta guía te llevará de 0 a tener tu bot funcionando en producción.

## Paso 1: Preparar el Código

### 1.1 Clonar/Subir a GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <tu-repo-url>
git push -u origin main
```

## Paso 2: Configurar Twilio (WhatsApp)

### 2.1 Crear cuenta Twilio

1. Ir a https://www.twilio.com/try-twilio
2. Registrarte (gratis)
3. Verificar email y teléfono

### 2.2 Obtener credenciales

En https://console.twilio.com/:

1. Copiar **Account SID**
2. Copiar **Auth Token**
3. Guardar ambos, los usarás después

### 2.3 Activar WhatsApp Sandbox

1. Ir a **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Escanear código QR con WhatsApp
3. Enviar el código que te muestra (ej: "join <palabra>")
4. Verás confirmación en WhatsApp

### 2.4 Anotar número de WhatsApp

El número será algo como: `whatsapp:+14155238886`

## Paso 3: Deploy en Render

### 3.1 Crear cuenta Render

1. Ir a https://render.com/
2. Sign up (gratis)
3. Conectar con GitHub

### 3.2 Crear Web Service

1. Click **New +** → **Web Service**
2. Conectar tu repositorio de GitHub
3. Seleccionar el repositorio `telephone_assistant`
4. Render detectará automáticamente la configuración

### 3.3 Configurar

- **Name**: `asistente-telefonico` (o tu nombre)
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app.whatsapp_bot:app`
- **Instance Type**: Free (para empezar)

### 3.4 Variables de Entorno

Click en **Environment** y agregar:

```
OPENAI_API_KEY = sk-proj-tu-api-key-aqui
OPENAI_MODEL = gpt-4o-mini
TWILIO_ACCOUNT_SID = tu-account-sid-aqui
TWILIO_AUTH_TOKEN = tu-auth-token-aqui
TWILIO_WHATSAPP_NUMBER = whatsapp:+14155238886
PORT = 10000
```

### 3.5 Deploy

1. Click **Create Web Service**
2. Esperar 2-3 minutos
3. Obtendrás una URL: `https://asistente-telefonico.onrender.com`

## Paso 4: Conectar Twilio con Render

### 4.1 Configurar Webhook

1. Volver a Twilio Console
2. Ir a **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
3. En **"When a message comes in"**:
   ```
   https://asistente-telefonico.onrender.com/webhook/whatsapp
   ```
4. Method: **POST**
5. **Save**

## Paso 5: ¡Probar!

### 5.1 Enviar mensaje de prueba

Desde tu WhatsApp (el que conectaste al sandbox):

```
Hola
```

El bot debería responder:

```
Buenos días/tardes, Clínica San Rafael, ¿en qué puedo ayudarlo?
```

### 5.2 Probar con voz

Graba una nota de voz diciendo:
```
"Quiero un turno para cardiología"
```

El bot debería transcribir y responder.

## 🎯 Verificación

### ✅ Checklist

- [ ] Repositorio en GitHub
- [ ] Cuenta Twilio creada y verificada
- [ ] WhatsApp Sandbox activado
- [ ] Cuenta Render creada
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas
- [ ] Webhook configurado en Twilio
- [ ] Bot responde a mensajes de texto
- [ ] Bot responde a notas de voz

## 🔍 Troubleshooting

### Bot no responde

1. **Verificar logs en Render:**
   - Ir al dashboard de Render
   - Click en "Logs"
   - Buscar errores

2. **Verificar webhook:**
   ```bash
   curl https://tu-url.onrender.com/health
   ```
   Debe responder: `{"status":"ok"}`

3. **Verificar variables de entorno:**
   - En Render, ir a Environment
   - Verificar que todas las keys estén configuradas
   - No debe haber espacios extra

### Error: "OPENAI_API_KEY no encontrada"

Verificar en Render → Environment que `OPENAI_API_KEY` esté configurada correctamente.

### Error: Twilio Unauthorized

1. Verificar `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN`
2. Copiar nuevamente desde Twilio Console
3. Actualizar en Render y hacer redeploy

### Audio no se transcribe

1. Verificar que enviaste una nota de voz (no un archivo de audio)
2. Ver logs en Render para detalles del error
3. Twilio debe tener permisos para enviar media

## 💰 Costos

### Desarrollo (GRATIS)

- Render Free Plan
- Twilio WhatsApp Sandbox (gratis, 1 número de prueba)
- OpenAI (~$0.0015 por conversación)

### Producción

- **Render:** $7/mes (Starter) o Free (con limitaciones)
- **Twilio:** ~$0.005 USD por mensaje
- **OpenAI:** ~$1.50 por 1000 conversaciones

## 📱 Producción WhatsApp (Opcional)

Para usar un número propio de WhatsApp (no sandbox):

1. Solicitar aprobación en Twilio
2. Proporcionar Business Profile
3. Comprar número de teléfono Twilio
4. Enviar plantillas de mensajes para aprobación de Meta
5. Costo: ~$0.005 por mensaje + costo del número

## 🔄 Actualizar el Bot

Cuando hagas cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

Render se redesplegará automáticamente.

## 📊 Monitoreo

### Ver logs en tiempo real

En Render Dashboard:
- Click en tu servicio
- Click en "Logs"
- Ver logs en tiempo real

### Métricas

- **Render:** Dashboard muestra CPU, memoria, requests
- **Twilio:** Console muestra mensajes enviados/recibidos
- **OpenAI:** Dashboard muestra uso de tokens

## 🎉 ¡Listo!

Tu asistente telefónico está en producción y funcionando 24/7.

### Próximos pasos:

1. Personalizar `config/datos_clinica.py` con tus datos reales
2. Ajustar `config/prompts.py` según tu tono deseado
3. Monitorear logs y mejorar respuestas
4. Escalar a plan pago si necesitas más recursos

---

**¿Problemas?** Revisa los logs en Render o contacta soporte.
