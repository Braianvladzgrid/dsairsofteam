# 🎮 Death Squad Airsoft - Sistema Completo

## 🚀 Inicio Rápido

### 1. Iniciar el Sistema

```bash
./start_all.sh
```

Este script:
- Limpia los puertos 5000 y 8000
- Instala dependencias
- Inicializa la base de datos
- Inicia el backend (puerto 5000)
- Inicia el frontend (puerto 8000)

### 2. Probar el Sistema

```bash
python test_system.py
```

Este script crea datos de ejemplo y verifica que todo funcione.

## 🌐 URLs

- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000
- **Admin Panel**: http://localhost:8000/admin-operaciones.html
- **Panel Operaciones**: http://localhost:8000/admin-panel.html

## 👤 Credenciales Admin

```
Email:    admin@dsairsofteam.local
Password: Admin123!
```

## 📝 Logs

Ver logs en tiempo real:

```bash
# Backend
tail -f /tmp/backend.log

# Frontend
tail -f /tmp/frontend.log
```

## 🛑 Detener el Sistema

```bash
pkill -f 'python.*app.py'
pkill -f 'python.*http.server'
```

O simplemente:

```bash
lsof -ti:5000,8000 | xargs kill -9
```

## 🧪 Pruebas

### Verificar Salud del Backend

```bash
curl http://localhost:5000/api/health
```

Respuesta esperada:
```json
{"status": "Backend running"}
```

### Probar Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@dsairsofteam.local", "password": "Admin123!"}'
```

### Ver Operaciones

```bash
curl http://localhost:5000/api/operations
```

## 🏗️ Estructura del Proyecto

```
dsairsofteam/
├── backend/
│   ├── app.py              # Aplicación Flask principal
│   ├── models.py           # Modelos de base de datos
│   ├── config.py           # Configuración
│   ├── init_db.py          # Script de inicialización
│   ├── requirements.txt    # Dependencias Python
│   └── routes/
│       ├── auth.py         # Rutas de autenticación
│       ├── operations.py   # Rutas de operaciones
│       ├── properties.py   # Rutas de propiedades
│       └── users.py        # Rutas de usuarios
├── admin-operaciones.html  # Panel admin de operaciones
├── admin-panel.html        # Panel admin general
├── index.html              # Página principal
├── perfil.html             # Perfil de usuario
├── style.css               # Estilos globales
├── start_all.sh            # Script de inicio
└── test_system.py          # Script de pruebas
```

## 🔧 Solución de Problemas

### Error: "Port already in use"

```bash
lsof -ti:5000,8000 | xargs kill -9
./start_all.sh
```

### Error: "Backend no responde"

1. Verificar que el backend esté corriendo:
```bash
ps aux | grep "python.*app.py"
```

2. Ver los logs:
```bash
tail -f /tmp/backend.log
```

3. Reiniciar:
```bash
./start_all.sh
```

### Error: "CORS" en el navegador

El CORS ya está configurado para los puertos 5000 y 8000. Si usas otro puerto, edita `backend/app.py` y agrega tu puerto en la lista de `origins`.

### Base de datos corrupta

```bash
cd backend
rm -f instance/database.db
python init_db.py
```

## 📋 Funcionalidades

### Frontend (Usuario)
- ✅ Registro e inicio de sesión
- ✅ Ver operaciones disponibles
- ✅ Perfil de usuario
- ✅ Sistema de reservas

### Admin Panel
- ✅ Gestión de operaciones (CRUD completo)
- ✅ Ver participantes
- ✅ Activar/desactivar operaciones
- ✅ Subir imágenes (URL o Base64)
- ✅ Gestión de usuarios

### API Endpoints

#### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

#### Operaciones
- `GET /api/operations` - Listar operaciones activas
- `GET /api/operations/<id>` - Ver operación específica
- `POST /api/operations` - Crear operación (admin)
- `PUT /api/operations/<id>` - Editar operación (admin)
- `DELETE /api/operations/<id>` - Eliminar operación (admin)

#### Participaciones
- `POST /api/operations/<id>/participate` - Unirse a operación
- `DELETE /api/operations/<id>/participate` - Cancelar participación

## 🎯 Próximos Pasos

1. Implementar sistema de pagos
2. Agregar notificaciones por email
3. Crear sistema de equipos
4. Implementar chat en vivo
5. Agregar galería de fotos de operaciones pasadas

## 📞 Soporte

Para problemas o preguntas, revisa los logs en `/tmp/backend.log` y `/tmp/frontend.log`.
