# Guía Completa de Prueba - Death Squad Airsoft

## 🚀 Inicio Rápido

### Paso 1: Iniciar el Backend

```bash
cd /workspaces/dsairsofteam/backend
python -m pip install -r requirements.txt
python app.py
```

El backend estará disponible en: **http://localhost:5000**

### Paso 2: Acceder al Panel de Administrador

Una vez que el backend esté corriendo, abre en tu navegador:

**http://localhost:8000/admin.html** (o la URL de tu servidor local)

El sistema automáticamente:
- ✓ Creará un usuario administrador (admin@example.com / admin123)
- ✓ Conectará con el backend
- ✓ Mostrará el dashboard

### Paso 3: Probar el Sistema

## 📋 Características Disponibles

### En el Admin Panel (`admin.html`)

#### 1. **Dashboard**
- Ver estadísticas de operaciones
- Estado del servidor backend
- Últimas operaciones creadas

#### 2. **Gestión de Operaciones**
- **Listar** todas las operaciones con tabla completa
- **Editar** operaciones existentes
- **Eliminar** operaciones
- **Crear** nuevas operaciones

#### 3. **Crear Nueva Operación**
Desde la sección "Nueva Operación" puedes:
- Título de la operación
- Tipo (milsim, picado, especial, realista, histórica, semi-milsim)
- Descripción
- Precio
- Ubicación
- Fecha de inicio y fin
- Máximo de participantes
- **IMAGEN** (Base64 o URL) ⭐
- Estado (activa/inactiva)

#### 4. **Probar Login**
- Botón para crear usuarios de prueba
- Modal de login funcional
- Prueba con usuario común y admin
- Credenciales mostradas en el modal

### En el Frontend (`index.html`)

#### 1. **Ver Operaciones**
- Las operaciones aparecen con:
  - ✓ Imagen (si está disponible)
  - ✓ Título
  - ✓ Tipo de operación
  - ✓ Descripción
  - ✓ Fecha
  - ✓ Precio
  - ✓ Ubicación
  - ✓ Número de participantes

#### 2. **Login Popup**
- Click en "Iniciar Sesión"
- Se abre un modal profesional
- Ingresa credenciales de prueba
- Automáticamente actualiza la interfaz

#### 3. **Perfil de Usuario**
- Después del login aparece nombre de usuario
- Si es admin, se muestra badge [ADMIN]
- Acceso directo al panel admin

## 🔐 Usuarios de Prueba

### Usuario Común
```
Email: user@example.com
Contraseña: password123
Rol: Comprador
```

### Administrador
```
Email: admin@example.com
Contraseña: admin123
Rol: Administrador (puede crear/editar operaciones)
```

## 🎯 Workflow Completo de Prueba

### 1. **Crear Operaciones** (Como Admin)
1. Ir a Admin Panel → Nueva Operación
2. Llenar formulario:
   - Título: "Milsim CQB en Warehouse"
   - Tipo: "milsim"
   - Precio: "150"
   - Fecha: Seleccionar fecha futura
   - Imagen: Pega una URL de imagen o base64
3. Click en "Guardar Operación"
4. Aparecerá en el dashboard

### 2. **Verificar Imágenes en Frontend**
1. Ir a Frontend (index.html)
2. Scroll a "Operaciones Activas"
3. Las operaciones creadas aparecerán con imagen

### 3. **Probar Login**
1. Click en "Iniciar Sesión"
2. Usa `user@example.com / password123`
3. Verás un popup de bienvenida
4. Tu nombre aparecerá en la navegación

### 4. **Probar Admin Login**
1. Logout (si estabas logueado)
2. Click en "Iniciar Sesión"
3. Usa `admin@example.com / admin123`
4. Aparecerá badge [ADMIN]
5. Podrás acceder al Dashboard Admin

### 5. **Editar Operaciones**
1. En Admin Panel → Operaciones
2. Click en "Editar" en cualquier operación
3. Modal se abre con todos los datos
4. Cambia imagen, precio, ubicación, etc.
5. Guardas cambios

### 6. **Eliminar Operaciones**
1. En Admin Panel → Operaciones → Editar
2. Click en botón "Eliminar" (rojo)
3. Confirma eliminación
4. Desaparece de la lista

## 📸 Agregar Imágenes

### Opción 1: Usar URL
```
https://via.placeholder.com/400x300?text=Milsim+Operation
```

### Opción 2: Usar Base64
1. Abre una imagen con convertidor Base64 online
2. Copia el resultado que empieza con `data:image/...`
3. Pega en el campo "Imagen"

## ✅ Checklist de Verificación

- [ ] Backend está corriendo en `http://localhost:5000`
- [ ] Admin Panel carga correctamente
- [ ] Admin se autentica automáticamente
- [ ] Puedo crear una operación
- [ ] Puedo agregar imagen a operación
- [ ] Operación aparece en frontend con imagen
- [ ] Puedo editar operación
- [ ] Puedo eliminar operación
- [ ] Login popup funciona
- [ ] Login usuario común funciona
- [ ] Login admin funciona
- [ ] Panel admin solo accesible para admins
- [ ] Operaciones muestran datos correctamente

## 🔧 Endpoints de API

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Operaciones (Públicas)
- `GET /api/operations` - Listar operaciones activas
- `GET /api/operations/active` - Operaciones futuras
- `GET /api/operations/past` - Operaciones pasadas
- `GET /api/operations/<id>` - Detalle de operación

### Operaciones (Admin Only)
- `POST /api/operations` - Crear operación
- `PUT /api/operations/<id>` - Actualizar operación
- `DELETE /api/operations/<id>` - Eliminar operación

### Participaciones
- `POST /api/operations/<id>/join` - Registrarse en operación
- `POST /api/operations/<id>/leave` - Cancelar registro
- `GET /api/operations/<id>/participants` - Listar participantes

## 🐛 Troubleshooting

### Backend no inicia
```
Error: Port 5000 in use
Solución: Cambia el puerto en backend/config.py
```

### CORS Error
```
Error: Access to XMLHttpRequest blocked
Solución: Asegúrate que CORS está habilitado en app.py
```

### Imágenes no cargan
```
Solución: Verifica que sea URL válida o base64 correcto
```

### Modal de login no abre
```
Solución: Abre consola (F12) y revisa errores JavaScript
```

## 📝 Notas Importantes

- Las operaciones se guardan en SQLite (instancia/airsoft.db)
- Los tokens JWT expiran después de 7 días
- Solo admins pueden crear/editar/eliminar operaciones
- Las imágenes se guardan como texto (base64 o URL)
- El sistema es totalmente funcional en desarrollo local

## 🎓 Siguiente Paso

Una vez verificado todo:
1. Desplegar a servidor de producción
2. Conectar base de datos real
3. Implementar validaciones adicionales
4. Agregar más funcionalidades (galería, comentarios, etc.)

---

**¡Disfruta probando tu sistema completo!** 🎯
