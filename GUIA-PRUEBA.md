# 🚀 Guía de Prueba - Sistema Completo

## 📋 Checklist antes de empezar

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `dsairsofteam` creada
- [ ] Python 3.8+ instalado
- [ ] Node.js (opcional, solo si usas servidor local para frontend)

---

## 1️⃣ Iniciar Backend

```bash
# Ir a la carpeta del backend
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Inicializar base de datos (crea tablas y usuario admin)
python init_db.py

# Ejecutar servidor
python app.py
```

✅ **Backend corriendo en**: `http://localhost:5000`
✅ **Admin**: `admin@dsairsofteam.local` / `Admin123!`

---

## 2️⃣ Probar Frontend

### Opción A: Abrir HTML directamente
```bash
# En la carpeta raíz del proyecto
# Simplemente abre index.html en tu navegador
# o usa un servidor local:

python3 -m http.server 8000
```

Accede a: `http://localhost:8000/index.html`

### Opción B: Usar extensión Live Server en VS Code
- Click derecho en `index.html`
- Selecciona "Open with Live Server"

---

## 🧪 Pruebas Paso a Paso

### Test 1: Verificar que el Backend está corriendo

```bash
# En otra terminal
curl http://localhost:5000/api/health
# Respuesta esperada: {"status": "Backend running"}
```

### Test 2: Crear usuario (Registro)

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Test",
    "email": "juan@test.com",
    "password": "Password123!",
    "user_type": "buyer"
  }'

# Respuesta: Token + datos del usuario
```

### Test 3: Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@test.com",
    "password": "Password123!"
  }'

# Guardar el token para los siguientes requests
```

### Test 4: Crear Operación (como Admin)

```bash
curl -X POST http://localhost:5000/api/operations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_ADMIN>" \
  -d '{
    "property_id": "prop-123",
    "seller_id": "seller-123",
    "buyer_id": "buyer-123",
    "type": "rent",
    "price": 1500,
    "start_date": "2026-03-15T10:00:00",
    "notes": "Operación de prueba",
    "status": "pending"
  }'
```

### Test 5: Activar/Desactivar Operación (solo Admin)

```bash
curl -X PATCH http://localhost:5000/api/operations/<OPERATION_ID>/toggle-active \
  -H "Authorization: Bearer <TOKEN_ADMIN>"

# Respuesta: {"message": "Operación activada/desactivada", "operation": {...}}
```

### Test 6: Ver Operaciones Activas

```bash
curl http://localhost:5000/api/operations/active
# Devuelve operaciones con start_date <= hoy
```

### Test 7: Ver Operaciones Pasadas

```bash
curl http://localhost:5000/api/operations/past
# Devuelve operaciones con start_date < hoy
```

---

## 🎯 Pruebas en Frontend

### Registro
1. Abre `index.html`
2. Haz click en **"Registrarse"**
3. Completa el formulario
4. Verifica que se cree la cuenta y se redirija a `perfil.html`

### Login
1. Abre `index.html`
2. Haz click en **"Iniciar Sesión"**
3. Usa credenciales de prueba
4. Verifica que aparezca tu nombre y botón "Cerrar Sesión"

### Dropdown de Operaciones
1. En el header, pasa el mouse sobre **"Operaciones"**
2. Verifica que el dropdown se abre y se mantiene visible
3. Haz click en "Operaciones Activas"

### Ver Operaciones
1. Scrollea a **"Operaciones Activas"**
2. Verifica que carga las operaciones desde el backend
3. Scrollea a **"Operaciones Pasadas"**
4. Verifica que carga las operaciones pasadas

### Panel Admin
1. Login como admin (`admin@dsairsofteam.local` / `Admin123!`)
2. Accede a `admin-operaciones.html`
3. Verifica que ves una tabla de operaciones
4. Haz click en el botón verde/naranja para activar/desactivar

---

## 🐛 Troubleshooting

### Error: "Error de conexión. Asegúrate que el backend está corriendo"

**Solución:**
```bash
# Verifica que el backend está corriendo
ps aux | grep python

# O inicia el servidor
cd backend
source venv/bin/activate
python app.py
```

### Error: "database dsairsofteam does not exist"

**Solución:**
```bash
# Crear la base de datos
createdb dsairsofteam

# O en psql
psql -U postgres
CREATE DATABASE dsairsofteam;
\q

# Luego ejecutar init_db.py
python init_db.py
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "CORS error" en el navegador

**Solución:**
- El backend tiene CORS habilitado por defecto
- Verifica que estés accediendo desde `http://` (no `https://`)
- Limpia la caché del navegador

### Las operaciones no aparecen

**Solución:**
1. Verifica que existan operaciones en la BD:
```bash
curl http://localhost:5000/api/operations/active
curl http://localhost:5000/api/operations/past
```

2. Si no hay operaciones, crea una usando Admin

---

## 📊 Endpoints Disponibles

### Sin Autenticación
```
GET /api/operations/active          → Operaciones activas
GET /api/operations/past            → Operaciones pasadas
GET /api/properties                 → Listar propiedades
GET /api/properties/:id             → Detalles propiedad
GET /api/users/:id                  → Perfil usuario
```

### Con Autenticación
```
POST /api/auth/register             → Registrarse
POST /api/auth/login                → Iniciar sesión
GET /api/auth/me                    → Usuario actual

GET /api/operations?filter=active   → Operaciones del usuario (activas)
GET /api/operations/:id             → Detalles operación
POST /api/operations                → Crear operación
PATCH /api/operations/:id           → Actualizar operación

POST /api/properties                → Crear propiedad
PATCH /api/properties/:id           → Actualizar propiedad
DELETE /api/properties/:id          → Eliminar propiedad

PATCH /api/users/:id                → Actualizar perfil
```

### Solo Admin
```
DELETE /api/operations/:id          → Eliminar operación
PATCH /api/operations/:id/toggle-active  → Activar/Desactivar
GET /api/operations/admin/all       → Todas las operaciones
GET /api/operations/admin/stats     → Estadísticas
```

---

## 📈 Datos de Prueba

### Usuario Admin (predeterminado)
```
Email: admin@dsairsofteam.local
Password: Admin123!
Role: Admin
```

### Usuario de Prueba
```
Email: test@example.com
Password: Test123!
Name: Usuario Test
Role: Buyer
```

---

## ✅ Verificación Final

Cuando todo está funcionando deberías ver:

✅ Backend en `http://localhost:5000` respondiendo
✅ Frontend cargando sin errores CORS
✅ Operaciones activas y pasadas mostrándose en index.html
✅ Dropdown de operaciones abierto al pasar el mouse
✅ Panel admin accesible para administrador
✅ Botones para activar/desactivar operaciones
✅ Registro y login funcionando

---

## 📝 Notas Importantes

⚠️ **En Producción:**
- Cambiar `JWT_SECRET` en `.env`
- Cambiar contraseña de admin
- Usar HTTPS
- Configurar CORS específicamente
- Usar variables de entorno seguras
- Configurar BD con credenciales fuertes

---

¿Preguntas? Revisa la documentación en `/backend/README.md`
