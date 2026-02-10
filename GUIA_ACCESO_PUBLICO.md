# 🌍 Guía de Acceso Público - Death Squad Airsoft

## 🎯 Objetivo
Permitir que el sistema sea accesible desde **cualquier dispositivo en cualquier lugar del mundo**, no solo desde tu red local.

## 📋 Requisitos
- Linux/macOS/WSL
- Docker/DevContainer (opcional pero recomendado)
- Conexión a internet

## 🚀 Inicio Rápido

### Opción 1: Cloudflare Tunnel (Recomendado)
```bash
chmod +x start_cloudflare.sh
./start_cloudflare.sh
```

Este script:
- ✅ Inicia el backend (puerto 5000)
- ✅ Inicia un servidor/proxy (puerto 8080) que sirve el frontend y proxyea `/api/*` al backend
- ✅ Publica TODO con **una sola URL** HTTPS (Cloudflare `trycloudflare.com`)
- ✅ No requiere registro y normalmente no muestra página de verificación

💡 Importante: el frontend de este proyecto usa `window.location.origin` + `/api` para llamar a la API.
Por eso, el enfoque más estable es **exponer una única URL** que sirva frontend + `/api` (vía proxy).

---

### Opción 2: LocalTunnel (Alternativa)
```bash
chmod +x start_localtunnel.sh
./start_localtunnel.sh
```

---

### Opción 3: ngrok (Versión simple, una sola URL)
```bash
chmod +x start_simple.sh
./start_simple.sh
```

---

### Nota sobre `start_public.sh` (Legacy)
`start_public.sh` crea 2 URLs (frontend + backend) y reescribe `config.js`, pero varias páginas calculan la API con el origen actual.
Para pruebas públicas completas, es preferible `start_cloudflare.sh`, `start_localtunnel.sh` o `start_simple.sh`.

### Opción 2: Configuración Manual con ngrok

#### Paso 1: Instalar ngrok
```bash
# Descargar ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

#### Paso 2: Registrarse en ngrok (Opcional pero recomendado)
1. Visita https://ngrok.com y crea una cuenta gratis
2. Obtén tu authtoken
3. Configura ngrok:
```bash
ngrok config add-authtoken TU_AUTHTOKEN_AQUI
```

**Beneficios de registrarse:**
- Sesiones más largas
- Más túneles simultáneos
- URLs personalizadas (planes pagos)

#### Paso 3: Iniciar servicios manualmente
```bash
# Terminal 1 - Backend
cd /workspaces/dsairsofteam/backend
python app.py

# Terminal 2 - Frontend
cd /workspaces/dsairsofteam
python -m http.server 8000

# Terminal 3 - Túnel Backend
ngrok http 5000

# Terminal 4 - Túnel Frontend
ngrok http 8000
```

## 🌐 Alternativas / Opciones

### LocalTunnel
```bash
# Instalar
npm install -g localtunnel

# Usar
lt --port 5000 --subdomain dsairsoft-backend
lt --port 8000 --subdomain dsairsoft-frontend
```

### Serveo (SSH tunneling)
```bash
# Backend
ssh -R 80:localhost:5000 serveo.net

# Frontend
ssh -R 80:localhost:8000 serveo.net
```

### Cloudflare Tunnel (Anteriormente Argo)
```bash
# Instalar
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# Usar
cloudflared tunnel --url http://localhost:8080
```

## 📱 Cómo Usar las URLs Públicas

Una vez que el script `start_cloudflare.sh` / `start_localtunnel.sh` / `start_simple.sh` esté corriendo, verás algo como:

```
📡 URL PÚBLICA (compartible con cualquier dispositivo):
   🌍 https://xxxxx.trycloudflare.com
```

### Para probar desde otro dispositivo:

1. **Desde tu teléfono móvil:**
   - Abre el navegador
   - Ingresa la URL pública que muestra el script
   - ¡Listo! El sistema funcionará completamente

2. **Desde otra computadora:**
   - Abre cualquier navegador
   - Ingresa la URL del Frontend
   - Comparte con tus compañeros de equipo

3. **Compartir con otros:**
   - Envía la URL del Frontend por WhatsApp, email, etc.
   - No necesitan instalar nada
   - Funciona en cualquier navegador moderno

## 🔒 Seguridad

### Consideraciones Importantes:

⚠️ **Con ngrok gratuito:**
- Las URLs son públicas y temporales
- Cualquiera con la URL puede acceder
- Las URLs cambian cada vez que reinicias

🛡️ **Recomendaciones:**

1. **Solo para desarrollo/pruebas:**
   - No uses para producción sin configuración adicional
   - No expongas datos sensibles reales

2. **Autenticación:**
   - El sistema ya tiene login/registro
   - Asegúrate de usar contraseñas fuertes

3. **ngrok con autenticación (cuenta registrada):**
   ```bash
   ngrok http 8000 --basic-auth="usuario:contraseña"
   ```

4. **Para producción:**
   - Usa un servicio de hosting (Vercel, Render, etc.)
   - Configura HTTPS correctamente
   - Usa variables de entorno para secretos

## 🐛 Solución de Problemas

### Error: "ngrok not found"
```bash
# Reinstalar ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

### Error: "Port already in use"
```bash
# Limpiar puertos
lsof -ti:5000,8000 | xargs kill -9
pkill -f ngrok
```

### Error: "Failed to connect to ngrok API"
```bash
# Verificar conexión a internet
ping -c 3 ngrok.com

# Reiniciar ngrok
pkill -f ngrok
./start_public.sh
```

### El frontend no se conecta al backend
1. Verifica que ambas URLs estén activas
2. Abre la consola del navegador (F12) y busca errores
3. Verifica que el backend esté respondiendo:
   ```bash
   curl https://tu-backend-url.ngrok.io/api/health
   ```

### Errores de CORS
El backend ya está configurado para aceptar requests de cualquier origen cuando usa ngrok. Si ves errores CORS:

1. Verifica que el backend esté corriendo
2. Revisa los logs: `cat /tmp/backend.log`
3. Reinicia ambos servicios

## 📊 Monitoreo

### Panel de ngrok
- URL: http://localhost:4040
- Muestra todas las requests en tiempo real
- Útil para debugging

### Ver logs
```bash
# Backend
tail -f /tmp/backend.log

# Frontend
tail -f /tmp/frontend.log

# ngrok
tail -f /tmp/ngrok_backend.log
tail -f /tmp/ngrok_frontend.log
```

### Verificar servicios activos
```bash
# Ver procesos
ps aux | grep python
ps aux | grep ngrok

# Ver puertos abiertos
lsof -i :5000
lsof -i :8000
lsof -i :4040
```

## 🎓 Casos de Uso

### 1. Demostración a Cliente
```bash
./start_public.sh
# Compartir URL del frontend con el cliente
# Cliente puede probar en tiempo real
```

### 2. Desarrollo Colaborativo
```bash
./start_public.sh
# Compartir URLs con equipo de desarrollo
# Hacer cambios y que todos los vean
```

### 3. Testing en Dispositivos Reales
```bash
./start_public.sh
# Probar en iPhone, Android, tablets
# Verificar responsive design
```

### 4. Presentación/Demo
```bash
./start_public.sh
# Proyectar URL en presentación
# Audiencia puede acceder simultáneamente
```

## 💡 Tips Profesionales

1. **URLs Personalizadas (ngrok Pro):**
   ```bash
   ngrok http 8000 --subdomain=dsairsoft-demo
   # URL fija: https://dsairsoft-demo.ngrok.io
   ```

2. **Configuración persistente:**
   Crea `~/.ngrok2/ngrok.yml`:
   ```yaml
   version: "2"
   authtoken: TU_TOKEN_AQUI
   tunnels:
     backend:
       proto: http
       addr: 5000
     frontend:
       proto: http
       addr: 8000
   ```
   
   Luego: `ngrok start --all`

3. **Webhook para notificar cambios de URL:**
   ```bash
   ngrok http 8000 --log=stdout | grep -o 'https://[^"]*'
   ```

## 🔄 Actualización de URLs en Archivos

Si las URLs de ngrok cambian y necesitas actualizar los archivos HTML:

```bash
python update_api_urls.py https://nueva-url-backend.ngrok.io
```

## 📞 Soporte

- Documentación ngrok: https://ngrok.com/docs
- Testing: Abre http://localhost:4040 para ver requests
- Logs: `/tmp/backend.log` y `/tmp/frontend.log`

## ✅ Checklist Pre-Demo

- [ ] Iniciar servicios con `./start_public.sh`
- [ ] Verificar que ambas URLs estén activas
- [ ] Probar login desde un dispositivo externo
- [ ] Verificar que las operaciones funcionen
- [ ] Tener el panel de ngrok abierto (localhost:4040)
- [ ] Preparar datos de prueba (usuarios de demo)

---

**¡Importante!** Las URLs públicas funcionan mientras el script esté corriendo. Para detenerlo, presiona `Ctrl+C`.
