# 🚀 INICIO RÁPIDO - Death Squad Airsoft

## ✅ Sistema Ya Iniciado

Tu sistema está **corriendo ahora mismo** y accesible públicamente.

---

## 🌍 URL PÚBLICA

```
https://clean-comics-tickle.loca.lt
```

**Esta URL funciona desde CUALQUIER dispositivo en el mundo:**
- 📱 Tu teléfono móvil
- 💻 Otra computadora
- 🖥️ Tablet
- 🌐 Cualquier navegador

---

## 📋 CÓMO PROBAR

### Desde Tu Dispositivo Actual

1. Abre: http://localhost:8080
2. Inicia sesión con:
   - **Email:** admin@dsairsoft.com
   - **Password:** admin123

### Desde OTRO Dispositivo (Teléfono, Otro PC, etc.)

1. Abre en cualquier navegador: **https://clean-comics-tickle.loca.lt**
2. LocalTunnel mostrará una página de advertencia (es normal)
3. Haz clic en **"Click to Continue"** o ingresa tu IP
4. ¡Listo! Verás la aplicación
5. Inicia sesión con las mismas credenciales

---

## ⚙️ GESTIÓN DEL SISTEMA

### Ver Estado
```bash
# Ver procesos activos
ps aux | grep -E "(python.*app.py|python.*proxy|lt)"

# Ver logs en tiempo real
tail -f /tmp/backend.log      # Backend
tail -f /tmp/proxy.log         # Proxy
tail -f /tmp/localtunnel.log   # Túnel público
```

### Detener el Sistema
```bash
# Opción 1: Si iniciaste con el script, presiona Ctrl+C

# Opción 2: Matar procesos manualmente
pkill -f "python app.py"
pkill -f "proxy_server.py"
pkill -f "lt --port"
```

### Reiniciar el Sistema
```bash
# Detener primero
pkill -f "start_localtunnel.sh"
lsof -ti:5000,8080 | xargs kill -9 2>/dev/null

# Iniciar de nuevo
cd /workspaces/dsairsofteam
./start_localtunnel.sh
```

---

## 🧪 FUNCIONALIDADES PARA PROBAR

### 1. Sistema de Autenticación
- ✅ Registro de nuevos usuarios
- ✅ Login/Logout
- ✅ Recuperación de contraseña

### 2. Gestión de Propiedades
- ✅ Ver catálogo de propiedades
- ✅ Filtrar por tipo (compra/alquiler)
- ✅ Ver detalles de cada propiedad
- ✅ Galería de imágenes

### 3. Operaciones (Usuarios Autenticados)
- ✅ Crear nueva operación
- ✅ Subir documentos
- ✅ Generar código QR
- ✅ Ver timeline de operaciones
- ✅ Agregar participantes

### 4. Panel de Administración (Solo Admin)
- ✅ Gestionar todas las operaciones
- ✅ Aprobar/rechazar operaciones
- ✅ Ver estadísticas
- ✅ Gestionar usuarios

---

## 🔐 USUARIOS DE PRUEBA

### Administrador
```
Email: admin@dsairsoft.com
Password: admin123
Permisos: Acceso total
```

### Usuario Regular (si lo creaste)
```
Email: tu_email@example.com
Password: tu_contraseña
Permisos: Operaciones propias
```

---

## 📱 PRUEBA EN MÚLTIPLES DISPOSITIVOS

### Escenario 1: Desde tu móvil
1. Abre la URL pública en tu teléfono
2. Navega por el catálogo
3. Registra un nuevo usuario
4. Crea una operación

### Escenario 2: Compartir con un amigo
1. Envía la URL: https://clean-comics-tickle.loca.lt
2. Tu amigo puede acceder desde cualquier lugar
3. Ambos pueden interactuar simultáneamente

### Escenario 3: Presentación/Demo
1. Proyecta la URL en una pantalla
2. La audiencia puede acceder desde sus dispositivos
3. Todos ven los cambios en tiempo real

---

## ⚠️ IMPORTANTE

### Limitaciones de LocalTunnel (Versión Gratuita)
- ⏱️ La sesión puede expirar después de un tiempo
- 🔄 La URL cambia cada vez que reinicias
- 🐌 Puede ser más lento que ngrok
- ⚠️ Página de advertencia en primera visita

### Seguridad
- 🔓 La URL es pública pero temporal
- 🔐 El sistema tiene autenticación
- ⚠️ Solo para desarrollo/pruebas
- 🚫 NO usar para datos sensibles reales

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### La URL no carga
```bash
# Verificar que localtunnel esté corriendo
ps aux | grep "lt --port"

# Ver logs del túnel
cat /tmp/localtunnel.log

# Reiniciar túnel
pkill -f "lt --port"
nohup lt --port 8080 > /tmp/localtunnel.log 2>&1 &
```

### Error de conexión al backend
```bash
# Verificar backend
curl http://localhost:5000/api/properties

# Ver logs
tail -20 /tmp/backend.log

# Reiniciar backend
cd /workspaces/dsairsofteam/backend
pkill -f "python app.py"
python app.py &
```

### "Cannot connect to server"
```bash
# Verificar proxy
curl http://localhost:8080

# Ver logs del proxy
tail -20 /tmp/proxy.log

# Reiniciar proxy
pkill -f "proxy_server.py"
python /tmp/proxy_server.py &
```

---

## 🎯 PRÓXIMOS PASOS

### Para seguir probando localmente
```bash
# Usar la URL local (más rápida)
http://localhost:8080
```

### Para producción real
Considera migrar a:
- **Vercel** (Frontend)
- **Render/Railway** (Backend)
- **PlanetScale/Supabase** (Base de datos)

### Para mejorar el túnel
```bash
# Opción 1: Registrarse en ngrok (gratis)
# https://dashboard.ngrok.com/signup
# Luego: ngrok config add-authtoken TU_TOKEN

# Opción 2: Usar Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8080
```

---

## 📞 AYUDA ADICIONAL

### Comando Todo-en-Uno
```bash
# Iniciar sistema completo
cd /workspaces/dsairsofteam && ./start_localtunnel.sh
```

### Ver Todo el Estado
```bash
# Un vistazo completo
echo "=== PROCESOS ==="
ps aux | grep -E "(python|lt)" | grep -v grep
echo -e "\n=== PUERTOS ==="
lsof -i :5000,8080
echo -e "\n=== LOGS RECIENTES ==="
echo "Backend:"; tail -5 /tmp/backend.log
echo "Proxy:"; tail -5 /tmp/proxy.log
```

---

## ✅ CHECKLIST DE PRUEBA

- [ ] Abrir URL pública desde tu PC
- [ ] Abrir URL pública desde tu móvil
- [ ] Hacer login con admin
- [ ] Navegar por las propiedades
- [ ] Crear un nuevo usuario
- [ ] Crear una operación
- [ ] Subir un documento
- [ ] Ver el código QR generado
- [ ] Acceder al panel de admin
- [ ] Compartir la URL con otra persona
- [ ] Verificar que ambos puedan acceder simultáneamente

---

**💡 TIP:** Guarda esta URL mientras esté activa:
```
https://clean-comics-tickle.loca.lt
```

**⏰ Recuerda:** Esta URL funciona mientras el script esté corriendo. Para detener, presiona `Ctrl+C` en la terminal donde lo iniciaste.
