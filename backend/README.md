# Backend - DSAirsoft Team (Python/Flask)

API REST para la plataforma de bienes raíces construida con Flask + SQLAlchemy + PostgreSQL.

## 🔒 Seguridad

✅ **Protección contra inyección SQL**: SQLAlchemy ORM con consultas parametrizadas
✅ **Protección contra XSS**: Validación y sanitización de inputs con Marshmallow y Bleach
✅ **Autenticación**: JWT (JSON Web Tokens)
✅ **Autorización**: Roles (usuario normal, admin)
✅ **Validación**: Marshmallow schemas para validar todos los inputs

## 📋 Instalación

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env
```

## 🗄️ Configuración de Base de Datos

### Opción 1: Usando PostgreSQL instalado localmente

```bash
# Crear la base de datos
createdb dsairsofteam

# Actualizar .env con tus credenciales si es necesario
```

### Opción 2: Usando Docker

```bash
docker run -d \
  --name postgres-dsairsofteam \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=dsairsofteam \
  -p 5432:5432 \
  postgres:15
```

## 🚀 Ejecutar el Servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Inicializar base de datos (crea tablas y usuario admin)
python init_db.py

# Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:5000`

### Usuario Admin Predeterminado

- **Email**: `admin@dsairsofteam.local`
- **Contraseña**: `Admin123!`
- ⚠️ **Cambia la contraseña en producción**

## 📦 Estructura

```
backend/
├── routes/              # Rutas de la API
│   ├── auth.py         # Autenticación
│   ├── properties.py   # Propiedades
│   ├── users.py        # Usuarios
│   └── operations.py   # Operaciones
├── models.py           # Modelos de datos
├── schemas.py          # Validación y sanitización
├── config.py           # Configuración
├── app.py              # Punto de entrada
├── init_db.py          # Inicialización de BD
├── requirements.txt    # Dependencias
└── .env.example        # Variables de entorno
```

## 🔗 Endpoints de API

### Autenticación
- `POST /api/auth/register` - Registrarse
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual (requiere token)

### Propiedades
- `GET /api/properties` - Listar propiedades
  - Query params: `operationType` (rent/sell), `city`, `type`
- `GET /api/properties/:id` - Obtener detalles
- `POST /api/properties` - Crear propiedad (requiere token)
- `PATCH /api/properties/:id` - Actualizar propiedad (requiere token)
- `DELETE /api/properties/:id` - Eliminar propiedad (requiere token)

### Usuarios
- `GET /api/users/:id` - Obtener perfil
- `PATCH /api/users/:id` - Actualizar perfil (requiere token)

### Operaciones
- `GET /api/operations` - Listar operaciones del usuario (requiere token)
- `GET /api/operations/:id` - Obtener detalles (requiere token)
- `POST /api/operations` - Crear operación (requiere token)
- `PATCH /api/operations/:id` - Actualizar operación (requiere token)
- `DELETE /api/operations/:id` - Eliminar operación (requiere token + admin)

### Admin Only
- `GET /api/operations/admin/all` - Listar todas las operaciones (admin)
- `GET /api/operations/admin/stats` - Estadísticas de operaciones (admin)

## 🔐 Autenticación

La mayoría de los endpoints requieren un token JWT en el header:

```
Authorization: Bearer <token>
```

### Obtener token:

1. Registrarse: `POST /api/auth/register`
2. Iniciar sesión: `POST /api/auth/login`

El response incluye el `token` que se debe usar en los siguientes requests.

## ✅ Validación y Sanitización

Todos los inputs se validan automáticamente:

- **Longitud**: Strings con límites mínimos/máximos
- **Emails**: Validación de formato
- **Números**: Decimales con precisión garantizada
- **Enums**: Solo valores permitidos
- **XSS**: Sanitización con Bleach
- **SQL Injection**: SQLAlchemy ORM parametrizado

## 🧪 Ejemplo de Request

```bash
# Registrarse
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "MyPassword123!",
    "user_type": "buyer"
  }'

# Iniciar sesión
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "MyPassword123!"
  }'

# Crear propiedad (requiere token)
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_aqui>" \
  -d '{
    "title": "Casa en zona céntrica",
    "type": "house",
    "price": 150000,
    "operation_type": "sell",
    "address": "Calle Principal 123",
    "city": "Montevideo"
  }'
```

## 🛠️ Desarrollo

Los cambios en los archivos se detectan automáticamente con Flask en modo debug.

```bash
python app.py
```

## 📊 Variables de Entorno

Ver `.env.example` para todas las variables disponibles:

- `PORT` - Puerto del servidor (default: 5000)
- `DATABASE_URL` - URL de conexión a PostgreSQL
- `JWT_SECRET` - Secreto para firmar tokens JWT
- `JWT_EXPIRE` - Tiempo de expiración de tokens (en segundos)
