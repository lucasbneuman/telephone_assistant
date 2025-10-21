# 🚀 Guía Completa de Deployment - Asistente Telefónico con IA

## 📋 Tabla de Contenidos

1. [Visión General del Sistema](#visión-general-del-sistema)
2. [Prerequisitos](#prerequisitos)
3. [Configuración Inicial](#configuración-inicial)
4. [Deploy en Render](#deploy-en-render)
5. [Configuración de WhatsApp](#configuración-de-whatsapp)
6. [Configuración de Llamadas Telefónicas](#configuración-de-llamadas-telefónicas)
7. [Pruebas y Validación](#pruebas-y-validación)
8. [Troubleshooting](#troubleshooting)
9. [Costos](#costos)
10. [Mantenimiento](#mantenimiento)

---

## 📱 Visión General del Sistema

### ¿Qué hace este bot?

Tu asistente telefónico con IA puede:

- ✅ **Recibir llamadas telefónicas** y conversar por voz en tiempo real
- ✅ **Responder mensajes de WhatsApp** (texto y notas de voz)
- ✅ **Gestionar turnos médicos** automáticamente
- ✅ **Responder preguntas** sobre especialidades, coberturas y horarios
- ✅ **Mantener contexto** durante toda la conversación
- ✅ **Funcionar 24/7** sin intervención humana

### Arquitectura del Sistema

```
┌─────────────────┐
│   Paciente      │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Twilio  │ (Recibe llamadas/mensajes)
    └────┬─────┘
         │
    ┌────▼─────────────────────┐
    │  Render (Flask App)      │
    │  - Webhook Voice         │
    │  - Webhook WhatsApp      │
    │  - AI Assistant          │
    └────┬─────────────────────┘
         │
    ┌────▼─────┐
    │ OpenAI   │ (GPT-4 para respuestas)
    └──────────┘
```

### Flujo de una Llamada Telefónica

```
1. Paciente llama al número Twilio
   ↓
2. Twilio envía request a /webhook/voice
   ↓
3. Bot saluda y activa reconocimiento de voz
   ↓
4. Usuario habla → Twilio transcribe a texto
   ↓
5. Bot procesa con OpenAI
   ↓
6. Bot responde con voz sintetizada (Amazon Polly)
   ↓
7. Se repite el ciclo hasta que el usuario se despide
   ↓
8. Bot cuelga y guarda resumen
```

### Flujo de Mensaje de WhatsApp

```
1. Paciente envía mensaje/nota de voz
   ↓
2. Twilio envía request a /webhook/whatsapp
   ↓
3. Si es audio: descarga y transcribe con Google STT
   ↓
4. Bot procesa con OpenAI
   ↓
5. Bot responde por texto
   ↓
6. Se repite hasta despedida
```

---

## 🔧 Prerequisitos

### Cuentas Necesarias

- [x] **GitHub** - Para alojar el código
- [x] **Render** - Para hosting (plan gratuito disponible)
- [x] **Twilio** - Para telefonía y WhatsApp ($15 USD gratis)
- [x] **OpenAI** - Para IA conversacional (~$5 USD inicial)

### Conocimientos Básicos

- Uso básico de Git
- Manejo de línea de comandos
- Conceptos de variables de entorno
- (Opcional) Python básico

---

## 📦 Configuración Inicial

### Paso 1: Preparar el Repositorio

Si aún no lo has hecho:

```bash
# Clonar o inicializar repositorio
git init
git add .
git commit -m "Initial commit - Asistente telefónico con IA"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/telephone_assistant.git
git branch -M master
git push -u origin master
```

### Paso 2: Obtener API Key de OpenAI

1. Ir a https://platform.openai.com/
2. Sign up o login
3. Ir a **API Keys** → **Create new secret key**
4. Copiar la key (empieza con `sk-proj-...`)
5. ⚠️ **IMPORTANTE**: Guardarla en lugar seguro, no se puede ver después

**Costo estimado:** ~$0.002 por conversación con GPT-4o-mini

### Paso 3: Crear Cuenta en Twilio

1. Ir a https://www.twilio.com/try-twilio
2. Registrarte con email
3. Verificar teléfono
4. Recibirás **$15 USD de crédito gratis** 🎉

### Paso 4: Obtener Credenciales de Twilio

En https://console.twilio.com/:

1. En el dashboard verás:
   - **Account SID**: `ACxxxxxxxxxxxx`
   - **Auth Token**: Click "Show" para revelar
2. Copiar ambos y guardarlos

---

## 🌐 Deploy en Render

### Paso 1: Crear Cuenta en Render

1. Ir a https://render.com/
2. Click **Get Started** o **Sign Up**
3. Conectar con GitHub
4. Autorizar acceso a tus repositorios

### Paso 2: Crear Web Service

1. En dashboard de Render, click **New +**
2. Seleccionar **Web Service**
3. Buscar tu repositorio `telephone_assistant`
4. Click **Connect**

### Paso 3: Configurar el Servicio

Completar los campos:

| Campo | Valor |
|-------|-------|
| **Name** | `asistente-telefonico-clinica` (o tu nombre preferido) |
| **Region** | Oregon (US West) - más cercano |
| **Branch** | `master` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app.whatsapp_bot:app` |
| **Instance Type** | Free |

### Paso 4: Configurar Variables de Entorno

En la sección **Environment**, agregar una por una:

```bash
# OpenAI (REQUERIDO)
OPENAI_API_KEY=sk-proj-tu-key-aqui-completa
OPENAI_MODEL=gpt-4o-mini

# Twilio (REQUERIDO)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu-auth-token-aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Flask (REQUERIDO)
SECRET_KEY=genera-una-clave-random-segura-aqui

# Twilio Phone (OPCIONAL - solo si usarás llamadas)
TWILIO_PHONE_NUMBER=+1234567890
```

**⚠️ IMPORTANTE:**
- **NO configures la variable `PORT`** - Render la asigna automáticamente
- No dejes espacios antes o después del `=`
- Las keys son sensibles a mayúsculas/minúsculas
- No uses comillas alrededor de los valores
- `TWILIO_PHONE_NUMBER` es opcional, solo si vas a usar llamadas telefónicas

### Paso 5: Deploy Inicial

1. Click **Create Web Service**
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar Python 3.13
   - Instalar dependencias (`requirements.txt`)
   - Ejecutar `gunicorn`
3. Espera 3-5 minutos
4. Verás el estado: ✅ **Live**
5. Tu URL será: `https://asistente-telefonico-clinica.onrender.com`

### Paso 6: Verificar que Funciona

Abre en tu navegador:

```
https://tu-app.onrender.com/health
```

Debe responder:
```json
{"status": "ok", "service": "telephone_assistant"}
```

Si ves esto, ¡el backend está funcionando! ✅

---

## 💬 Configuración de WhatsApp

### Paso 1: Activar WhatsApp Sandbox

1. Ir a Twilio Console: https://console.twilio.com/
2. Menú lateral: **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Verás un código QR y un mensaje como:
   ```
   join [palabra-aleatoria]
   ```
4. Desde tu WhatsApp personal:
   - Escanear el código QR, O
   - Agregar el número a contactos y enviar el mensaje `join [palabra]`
5. Recibirás confirmación: *"Twilio Sandbox: ✅ You are all set!"*

### Paso 2: Configurar Webhook de WhatsApp

1. En Twilio Console, ir a:
   **Messaging** → **Settings** → **WhatsApp Sandbox Settings**

2. En **"When a message comes in"**:
   ```
   https://tu-app.onrender.com/webhook/whatsapp
   ```

3. Method: **HTTP POST**

4. Click **Save**

### Paso 3: Probar WhatsApp

Desde tu WhatsApp (el que conectaste):

**Prueba 1 - Mensaje de texto:**
```
Hola
```

**Respuesta esperada:**
```
Buenos días/tardes, Clínica San Rafael, ¿en qué puedo ayudarlo?
```

**Prueba 2 - Nota de voz:**
Graba una nota de voz diciendo:
```
"Quiero sacar un turno para cardiología"
```

El bot debería transcribir y responder apropiadamente.

**Prueba 3 - Comandos especiales:**
```
/ayuda
```

---

## ☎️ Configuración de Llamadas Telefónicas

### Paso 1: Obtener un Número de Teléfono

#### Opción A: Trial Account (GRATIS - para testing)

1. En Twilio Console: **Phone Numbers** → **Manage** → **Buy a number**
2. Seleccionar país (ej: United States)
3. Filtros:
   - ✅ Voice
   - ✅ SMS (opcional)
4. Click **Search**
5. Seleccionar un número que te guste
6. Click **Buy** (gratis en trial)

**⚠️ Limitaciones del Trial:**
- Solo puedes llamar desde números verificados
- Necesitas verificar números en: **Phone Numbers** → **Verified Caller IDs**
- Las llamadas tienen un mensaje inicial: "You have a trial account..."

#### Opción B: Upgrade Account (Para producción)

Si quieres aceptar llamadas de cualquier número:
1. **Account** → **Upgrade**
2. Agregar método de pago
3. Ya no habrá restricciones

### Paso 2: Configurar el Número para Llamadas

1. En Twilio Console: **Phone Numbers** → **Manage** → **Active numbers**
2. Click en tu número comprado
3. Scroll down a **Voice Configuration**

Configurar así:

| Campo | Valor |
|-------|-------|
| **Accept Incoming** | Voice Calls |
| **Configure with** | Webhooks, TwiML Bins, Functions, Studio, or Proxy |
| **A call comes in** | Webhook |
| **URL** | `https://tu-app.onrender.com/webhook/voice` |
| **HTTP Method** | HTTP POST |
| **Status Callback URL** | `https://tu-app.onrender.com/webhook/voice/status` |
| **HTTP Method** | HTTP POST |

4. Click **Save Configuration**

### Paso 3: Actualizar Variable de Entorno

En Render, agregar/actualizar:

```bash
TWILIO_PHONE_NUMBER=+12345678900
```

(Usar el número que compraste sin espacios)

Luego hacer **Manual Deploy** para que tome el cambio.

### Paso 4: Probar Llamada Telefónica

**Desde un número verificado** (si estás en trial):

1. Llamar al número de Twilio
2. Escucharás:
   ```
   "You have a trial account. Press any key to continue."
   ```
3. Presiona cualquier tecla
4. Escucharás el saludo del bot:
   ```
   "Buenos días/tardes, Clínica San Rafael, ¿en qué puedo ayudarlo?"
   ```
5. Habla naturalmente, por ejemplo:
   ```
   "Quiero sacar un turno para odontología"
   ```
6. El bot te responderá y seguirá la conversación
7. Para terminar, di:
   ```
   "Gracias, nada más" o "Adiós"
   ```

### Paso 5: Verificar en Logs

En Render → Logs, deberías ver:

```
INFO - Llamada recibida de +1234567890, CallSid: CAxxxxxxxxxx
INFO - Nueva sesión de llamada creada para CAxxxxxxxxxx
INFO - Respuesta de llamada CAxxxxxxxxxx: quiero sacar un turno
INFO - Respuesta enviada en llamada CAxxxxxxxxxx: Perfecto...
```

---

## ✅ Pruebas y Validación

### Checklist de Verificación

**Infraestructura:**
- [ ] Repositorio en GitHub actualizado
- [ ] Deploy en Render exitoso (estado: Live)
- [ ] URL de Render responde en `/health`
- [ ] Todas las variables de entorno configuradas

**WhatsApp:**
- [ ] Sandbox activado y número conectado
- [ ] Webhook configurado correctamente
- [ ] Bot responde a mensajes de texto
- [ ] Bot transcribe y responde notas de voz
- [ ] Comandos especiales funcionan (`/ayuda`, `/reiniciar`)

**Llamadas Telefónicas:**
- [ ] Número de Twilio comprado
- [ ] Webhook de voz configurado
- [ ] Número verificado (si estás en trial)
- [ ] Bot responde a llamadas
- [ ] Reconocimiento de voz funciona
- [ ] Conversación fluida
- [ ] Despedida y cuelgue funcionan

**Funcionalidad:**
- [ ] IA responde coherentemente
- [ ] Mantiene contexto de conversación
- [ ] Datos de clínica son correctos
- [ ] Maneja errores gracefully

### Casos de Prueba Recomendados

#### 1. Solicitar Turno (Llamada)

```
Usuario: "Quiero sacar un turno para cardiología"
Bot: "Claro, para cardiología tenemos disponibilidad..."
Usuario: "El miércoles a las 10"
Bot: "Perfecto. ¿Me puede dar su nombre completo?"
Usuario: "Juan Pérez"
Bot: "¿Y su número de documento?"
Usuario: "12345678"
Bot: "Excelente, su turno está confirmado..."
```

#### 2. Consultar Coberturas (WhatsApp)

```
Usuario: ¿Trabajan con OSDE?
Bot: Sí, trabajamos con OSDE. También aceptamos [lista de obras sociales]
```

#### 3. Preguntar por Especialidades (Llamada)

```
Usuario: "¿Qué especialidades tienen?"
Bot: "Contamos con las siguientes especialidades: Cardiología, Traumatología..."
```

#### 4. Consultar Horarios (WhatsApp)

```
Usuario: ¿A qué hora abren?
Bot: Nuestro horario de atención es de lunes a viernes de 8:00 a 20:00...
```

---

## 🔍 Troubleshooting

### Problema 1: Bot no responde en WhatsApp

**Síntomas:**
- Envías mensaje y no hay respuesta
- WhatsApp muestra "✓" (enviado) pero sin respuesta

**Solución:**

1. **Verificar webhook en Twilio:**
   - Ir a Twilio Console → Messaging → WhatsApp Sandbox Settings
   - Verificar URL: debe ser `https://tu-app.onrender.com/webhook/whatsapp`
   - Verificar que sea POST

2. **Verificar logs en Render:**
   ```
   Render Dashboard → Tu servicio → Logs
   ```
   Buscar líneas como:
   ```
   INFO - Mensaje recibido de whatsapp:+123...
   ```

3. **Probar endpoint manualmente:**
   ```bash
   curl -X POST https://tu-app.onrender.com/webhook/whatsapp \
     -d "Body=Hola" \
     -d "From=whatsapp:+1234567890"
   ```

4. **Verificar variables de entorno:**
   - Render → Environment
   - Verificar que `OPENAI_API_KEY` esté configurada
   - No debe tener espacios extra

### Problema 2: Llamadas no entran

**Síntomas:**
- Al llamar al número escuchas mensaje de error
- "The number you have dialed is not in service"

**Solución:**

1. **Verificar número comprado:**
   - Twilio Console → Phone Numbers → Active numbers
   - Verificar que el número esté activo

2. **Verificar configuración de voz:**
   - Click en el número
   - Voice Configuration debe tener:
     - URL: `https://tu-app.onrender.com/webhook/voice`
     - Method: POST

3. **Si estás en Trial:**
   - Verificar que tu número está en Verified Caller IDs
   - Twilio Console → Phone Numbers → Verified Caller IDs
   - Si no está, agrégalo

4. **Probar endpoint:**
   ```bash
   curl https://tu-app.onrender.com/webhook/voice
   ```
   Debe devolver TwiML (XML)

### Problema 3: Voz no se reconoce

**Síntomas:**
- Bot responde: "No pude escucharlo"
- La conversación no avanza

**Posibles causas y soluciones:**

1. **Audio muy bajo o con ruido:**
   - Hablar más cerca del teléfono
   - Reducir ruido de fondo
   - Hablar más despacio y claro

2. **Timeout muy corto:**
   En `app/whatsapp_bot.py` línea ~214:
   ```python
   timeout=5,  # Aumentar a 8 o 10
   ```

3. **Idioma incorrecto:**
   Verificar que esté configurado `language='es-MX'`

### Problema 4: Error "OPENAI_API_KEY not found"

**Síntomas:**
- Logs muestran: `Error: OPENAI_API_KEY no encontrada`
- Bot responde con error genérico

**Solución:**

1. Verificar en Render → Environment:
   ```bash
   OPENAI_API_KEY=sk-proj-...tu-key-completa...
   ```

2. Verificar que no haya espacios:
   - ❌ `OPENAI_API_KEY = sk-proj-...` (con espacios)
   - ✅ `OPENAI_API_KEY=sk-proj-...` (sin espacios)

3. Hacer **Manual Deploy** después de cambiar

4. Verificar que la key sea válida:
   - Ir a https://platform.openai.com/api-keys
   - Verificar que no esté revocada

### Problema 5: Deploy falla en Render

**Síntomas:**
- Deploy con status: ❌ Failed
- Logs muestran error de instalación

**Solución:**

1. **Error: "ModuleNotFoundError":**
   - Verificar que el módulo esté en `requirements.txt`
   - Ejemplo: si falta `pyttsx3`, agregarlo (aunque ya está opcional)

2. **Error: "Python version":**
   - Render usa Python 3.13 por defecto
   - Esto está bien para este proyecto

3. **Error: "Build failed":**
   - Ver logs completos en Render
   - Buscar la primera línea de error (ERROR o FAILED)
   - Copiar y buscar en Google si no es claro

4. **Reintentar deploy:**
   - Manual Deploy → Deploy latest commit

### Problema 6: Bot responde lento

**Posibles causas:**

1. **Free tier de Render:**
   - El servicio "se duerme" después de 15 min sin actividad
   - Primera request tarda ~30 segundos en despertar
   - **Solución:** Upgrade a plan pago ($7/mes) para mantenerlo activo

2. **OpenAI lento:**
   - GPT-4 es más lento que GPT-4o-mini
   - **Solución:** Usar `OPENAI_MODEL=gpt-4o-mini` (ya configurado)

3. **Muchos mensajes en contexto:**
   - El bot guarda historial completo
   - **Solución:** Limitar a últimos 10 mensajes (modificar código si es necesario)

### Problema 7: Costos inesperados

**Síntomas:**
- Cargo en Twilio mayor al esperado
- Cargo en OpenAI mayor al esperado

**Prevención:**

1. **Monitorear uso en Twilio:**
   - Console → Usage → Calls/Messages
   - Configurar alertas de billing

2. **Monitorear uso en OpenAI:**
   - Dashboard → Usage
   - Establecer límite mensual: Settings → Billing → Usage limits

3. **Configurar alertas:**
   - Twilio: Console → Billing → Alerts → Crear alerta a $10
   - OpenAI: Billing → Usage limits → Set limit a $10

### Comandos Útiles de Diagnóstico

```bash
# Probar health check
curl https://tu-app.onrender.com/health

# Probar webhook de WhatsApp (simulado)
curl -X POST https://tu-app.onrender.com/webhook/whatsapp \
  -d "Body=Hola&From=whatsapp:+1234567890"

# Ver versión de Python en Render (desde logs)
python --version

# Verificar que gunicorn esté corriendo
ps aux | grep gunicorn
```

---

## 💰 Costos Detallados

### Fase 1: Desarrollo y Validación (GRATIS hasta ~$15)

| Servicio | Costo | Duración | Detalles |
|----------|-------|----------|----------|
| **Render Free Plan** | $0 | Ilimitado | 750 horas/mes gratis |
| **Twilio Trial** | $0 (incluye $15) | Hasta agotar crédito | ~300 min de llamadas + 3000 mensajes WhatsApp |
| **OpenAI** | ~$5 iniciales | ~2500 conversaciones | $0.002 por conversación con gpt-4o-mini |
| **GitHub** | $0 | Ilimitado | Repos públicos gratis |

**Total para validar:** ~$5 USD (solo OpenAI)

**Tiempo de validación:** ~300 minutos de llamadas + miles de mensajes

### Fase 2: Producción (Uso real)

#### Costos Mensuales Estimados

**Escenario: Clínica pequeña**
- 100 llamadas/mes (promedio 3 min cada una)
- 500 mensajes WhatsApp/mes
- Disponibilidad 24/7

| Servicio | Cálculo | Costo Mensual |
|----------|---------|---------------|
| **Render Starter** | Plan fijo | $7.00 |
| **Twilio - Llamadas** | 100 llamadas × 3 min × $0.013/min | $3.90 |
| **Twilio - WhatsApp** | 500 mensajes × $0.005 | $2.50 |
| **Twilio - Número** | Fijo mensual | $1.15 |
| **OpenAI** | 600 conversaciones × $0.002 | $1.20 |
| **Total** | | **~$15.75/mes** |

**Escenario: Clínica mediana**
- 500 llamadas/mes (promedio 4 min)
- 2000 mensajes WhatsApp/mes

| Servicio | Cálculo | Costo Mensual |
|----------|---------|---------------|
| **Render Standard** | Plan fijo | $25.00 |
| **Twilio - Llamadas** | 500 × 4 min × $0.013/min | $26.00 |
| **Twilio - WhatsApp** | 2000 × $0.005 | $10.00 |
| **Twilio - Número** | Fijo | $1.15 |
| **OpenAI** | 2500 conversaciones × $0.002 | $5.00 |
| **Total** | | **~$67.15/mes** |

### Comparación con Alternativas

| Solución | Costo Mensual | Pros | Contras |
|----------|---------------|------|---------|
| **Este Bot (IA)** | $15-70 | Totalmente automatizado, 24/7, aprende | Requiere setup técnico |
| **Recepcionista Humano** | $1500-3000 | Empatía humana | Caro, horarios limitados |
| **IVR Tradicional** | $50-200 | Probado | No inteligente, frustrante |
| **Servicio Tercerizado** | $300-1000 | Sin mantenimiento | Caro, menos control |

### Optimización de Costos

**Tips para reducir gastos:**

1. **Usar Render Free Plan inicialmente:**
   - Gratis pero se duerme después de 15 min
   - Bueno para validación

2. **Limitar mensajes de prueba:**
   - Cada test cuesta $0.002 en OpenAI
   - Usar comandos `/reiniciar` en lugar de crear nueva conversación

3. **Optimizar prompts:**
   - Prompts más cortos = menos tokens = menos costo
   - Ya optimizado en este proyecto

4. **Monitorear y alertar:**
   - Configurar alertas en $10 USD
   - Revisar semanalmente

5. **Escalar gradualmente:**
   - Empezar en Free tier
   - Subir a Starter cuando valides
   - Subir a Standard solo si necesitas

---

## 🔄 Mantenimiento y Actualizaciones

### Actualizar el Bot

Cuando hagas cambios en el código:

```bash
# 1. Hacer cambios en archivos locales
# 2. Guardar cambios
git add .
git commit -m "Descripción clara del cambio"
git push origin master

# 3. Render se redesplegará automáticamente
```

**Tiempo de redeploy:** ~2-3 minutos

### Monitoreo en Producción

#### 1. Logs en Tiempo Real

En Render Dashboard:
- Click en tu servicio
- Tab **Logs**
- Ver logs en tiempo real (últimos 1000 mensajes)

**Qué buscar:**
- ✅ `INFO - Llamada recibida de...`
- ✅ `INFO - Respuesta enviada...`
- ❌ `ERROR -...` (investigar inmediatamente)

#### 2. Métricas de Render

Dashboard muestra:
- **CPU Usage:** Debe estar bajo 50%
- **Memory:** Debe estar bajo 512 MB
- **Response Time:** Debe ser < 2 segundos
- **HTTP Requests:** Cantidad de llamadas al bot

#### 3. Uso de Twilio

En Twilio Console:
- **Monitor** → **Logs** → **Calls**: Ver todas las llamadas
- **Monitor** → **Logs** → **Messages**: Ver mensajes
- **Usage**: Gráficos de uso y costos

#### 4. Uso de OpenAI

En OpenAI Platform:
- **Usage**: Tokens consumidos
- **Costs**: Costo acumulado del mes

### Mantenimiento Semanal (5 minutos)

**Checklist:**
- [ ] Revisar logs de Render (buscar errores)
- [ ] Verificar costos de Twilio
- [ ] Verificar costos de OpenAI
- [ ] Probar una llamada de test
- [ ] Probar un mensaje de WhatsApp

### Actualizaciones Recomendadas

#### Cada 2 semanas:
- Revisar y mejorar prompts en `config/prompts.py`
- Actualizar datos en `config/datos_clinica.py`
- Revisar conversaciones guardadas en logs

#### Cada mes:
- Actualizar dependencias:
  ```bash
  pip list --outdated
  pip install --upgrade openai twilio flask gunicorn
  pip freeze > requirements.txt
  git commit -am "Update dependencies"
  git push
  ```

#### Cada 3 meses:
- Revisar roadmap de OpenAI (nuevos modelos)
- Revisar roadmap de Twilio (nuevas features)
- Considerar migraciones o mejoras

### Backup y Recuperación

#### Backup de Conversaciones

Los logs se guardan automáticamente en:
- Render: Últimos 7 días (Free) o 30 días (Paid)
- Local: `logs/llamada_YYYYMMDD_HHMMSS.log` si ejecutas localmente

**Recomendación:** Configurar backup externo si necesitas historiales largos

#### Recuperación ante Desastres

Si algo sale mal:

1. **El bot no responde:**
   - Redeploy en Render: Manual Deploy → Deploy latest commit

2. **Código roto:**
   - Rollback a commit anterior:
     ```bash
     git log --oneline  # Ver commits
     git revert <commit-hash>
     git push
     ```

3. **Render caído:**
   - Render tiene 99.9% uptime
   - Si cae, esperar (usualmente < 5 min)
   - Alternativamente: Deploy en Railway, Fly.io, Heroku

### Personalización Avanzada

#### Cambiar Voz del Bot

En `app/whatsapp_bot.py`, línea ~223:

```python
# Cambiar de Polly.Mia a otra voz
voice='Polly.Lupe'  # Más formal
voice='Polly.Miguel'  # Voz masculina
```

Voces disponibles: https://docs.aws.amazon.com/polly/latest/dg/voicelist.html

#### Ajustar Timeouts

En `app/whatsapp_bot.py`, línea ~217:

```python
timeout=5,  # Tiempo para empezar a hablar (aumentar si usuarios lentos)
speech_timeout='auto',  # Twilio detecta silencio automático
```

#### Cambiar Idioma

En `app/whatsapp_bot.py`, línea ~216:

```python
language='es-MX',  # Español de México
# Otras opciones:
# 'es-ES'  # Español de España
# 'es-AR'  # Español de Argentina
```

---

## 🎉 ¡Listo para Producción!

### Checklist Final

- [ ] ✅ Bot desplegado en Render
- [ ] ✅ Responde mensajes de WhatsApp
- [ ] ✅ Responde llamadas telefónicas
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Webhooks de Twilio configurados
- [ ] ✅ Alertas de billing configuradas
- [ ] ✅ Datos de clínica personalizados
- [ ] ✅ Prompts ajustados al tono deseado
- [ ] ✅ Testeado en producción

### Próximos Pasos Recomendados

1. **Semana 1:** Validar con usuarios reales limitados
2. **Semana 2-3:** Recopilar feedback y mejorar
3. **Mes 1:** Optimizar prompts basándose en conversaciones reales
4. **Mes 2:** Considerar upgrade a plan pago si valida
5. **Mes 3+:** Agregar features avanzadas (calendarios, pagos, etc.)

### Soporte y Recursos

**Documentación:**
- Twilio Voice: https://www.twilio.com/docs/voice
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp
- OpenAI API: https://platform.openai.com/docs
- Render: https://render.com/docs

**Problemas:**
- Revisar sección [Troubleshooting](#troubleshooting)
- Logs de Render para debugging
- Twilio Console → Monitor → Logs

---

**¿Dudas o problemas?** Revisa los logs, la sección de troubleshooting, o consulta la documentación oficial de cada servicio.

**¡Tu asistente telefónico con IA está listo para funcionar 24/7!** 🚀🎉
