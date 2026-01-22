# 🔐 Guía de Prueba - Login Funcional

## ✅ Estado del Sistema

El sistema de login está **completamente funcional**. Todos los componentes necesarios están en marcha:

### Servidores Activos
- ✅ **Backend Flask**: Corriendo en `http://localhost:5000`
- ✅ **Servidor Frontend**: Corriendo en `http://localhost:8080`
- ✅ **Base de Datos**: SQLite inicializada en `backend/dsairsofteam.db`

### Base de Datos
Se creó automáticamente un **usuario admin** para que puedas probar:

```
📧 Email:    admin@dsairsofteam.local
🔐 Password: Admin123!
👤 Tipo:     Administrador
```

---

## 🚀 Cómo Probar el Login

### Opción 1: Desde la Interfaz Web
1. Abre el navegador en: **http://localhost:8080/index.html**
2. Haz clic en el botón **"Iniciar Sesión"** (en la esquina superior derecha)
3. Ingresa las credenciales:
   - Email: `admin@dsairsofteam.local`
   - Contraseña: `Admin123!`
4. Haz clic en **"Iniciar Sesión"**
5. ✅ Deberías ser redirigido a `perfil.html` automáticamente

### Opción 2: Con curl (Terminal)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@dsairsofteam.local","password":"Admin123!"}'
```

**Respuesta esperada:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGc...",
  "user": {
    "id": "...",
    "name": "Admin",
    "email": "admin@dsairsofteam.local",
    "is_admin": true,
    "user_type": "buyer",
    "created_at": "2026-01-21T23:31:00.000000"
  }
}
```

---

## 🎨 Mejoras CSS Aplicadas

El dropdown de selección ahora tiene:
- ✅ **Fondo blanco** con bordes verdes (tema consistente)
- ✅ **Opciones seleccionadas** con fondo verde oscuro
- ✅ **Efectos hover** suaves con borde verde
- ✅ **Icono de dropdown** personalizado (SVG)
- ✅ **Comportamiento fijo** al pasar el mouse (CSS `:hover`)
- ✅ **Padding mejorado** para mejor legibilidad
- ✅ **Transiciones suaves** entre estados

**Ejemplo visual:**
- Estado normal: Borde gris claro, fondo blanco
- Hover: Borde verde, fondo blanco (transición suave)
- Seleccionado: Opción con fondo verde (#2d5016)
- Focus: Borde verde + sombra de enfoque


---

## 📋 Flujo de Autenticación

### 1. Registro de Nuevo Usuario
```
POST /api/auth/register
{
  "name": "Tu Nombre",
  "email": "tu@email.com",
  "password": "Password123!",
  "user_type": "buyer|seller|agent"
}
```

### 2. Login
```
POST /api/auth/login
{
  "email": "tu@email.com",
  "password": "Password123!"
}
```
✅ Retorna token JWT que se guarda en `localStorage`

### 3. Rutas Protegidas
Cualquier endpoint que requiera autenticación espera:
```
GET /api/operations/all
Authorization: Bearer <tu_token_aquí>
```

---

## 🔍 Verificación Rápida

### ¿El backend está corriendo?
```bash
curl http://localhost:5000/api/health
# Respuesta: {"status": "Backend running"}
```

### ¿Puedo hacer login?
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@dsairsofteam.local","password":"Admin123!"}'
# Debe retornar un token
```

### ¿Los archivos estáticos se sirven?
```bash
curl http://localhost:8080/index.html
# Debe retornar el HTML completo
```

---

## 🛠️ Comandos Útiles

### Detener servidor Flask
```bash
# Presiona CTRL+C en la terminal del backend
```

### Ver logs de la base de datos
```bash
ls -lh backend/dsairsofteam.db
```

### Reiniciar la base de datos (borra todo)
```bash
rm backend/dsairsofteam.db
cd backend && python init_db.py
```

### Crear usuario adicional para testing
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@dsairsofteam.local",
    "password": "Test123!",
    "user_type": "buyer"
  }'
```

---

## 📝 Notas Importantes

### Tokens JWT
- ⏱️ **Expiración**: 7 días
- 🔑 **Ubicación en el navegador**: `localStorage` bajo la clave `token`
- 👤 **Usuario guardado**: `localStorage` bajo la clave `user`

### Seguridad
- ✅ Contraseñas hasheadas con bcrypt
- ✅ Validación de inputs con Marshmallow
- ✅ Protección XSS con Bleach
- ✅ CORS habilitado para `localhost:8080`

### Base de Datos
- 📁 **Tipo**: SQLite (local, sin instalación necesaria)
- 📍 **Ubicación**: `backend/dsairsofteam.db`
- 🗄️ **Modelos**: User, Property, Operation

---

## ❓ Troubleshooting

### "Error de conexión al backend"
→ Asegúrate que el servidor Flask está corriendo en puerto 5000
```bash
ps aux | grep "python app.py"
```

### "Email already registered"
→ El usuario ya existe. Usa otro email o reinicia la BD

### "Invalid token format"
→ El token debe ir en el header: `Authorization: Bearer <token>`

### "Token has expired"
→ Los tokens expiran después de 7 días. Haz login nuevamente

---

## ✨ Próximos Pasos

1. **Registrar nuevos usuarios** desde `registro.html`
2. **Ver operaciones** desde el dashboard
3. **Admin panel** en `admin-operaciones.html` (requiere `is_admin: true`)
4. **Completar perfil** en `perfil.html`

---

**Sistema listo para usar** ✅
