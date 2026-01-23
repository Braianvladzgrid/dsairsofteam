# Implementación: Listado de Participantes y Códigos QR Únicos

## Resumen General
Se han implementado dos características principales:
1. **Lista de Participantes en Operaciones** - Muestra quién se ha inscrito en cada operación
2. **Códigos QR Únicos por Usuario** - Cada usuario tiene un QR único que lo redirige a su perfil

## Cambios Implementados

### 1. Archivo: perfil.html
**Propósito**: Agregar sección de código QR único para cada usuario logeado

#### Cambios realizados:
- ✅ Agregada librería QR: `qrcode.js` v1.5.3 desde CDN
- ✅ Agregado CSS para la sección QR:
  - Estilos para contenedor `.qr-section`
  - Estilos para contenedor `.qr-container`
  - Estilos para información de ID `.qr-id-info`
  
- ✅ Agregada nueva sección HTML con:
  - Contenedor `#qrCode` para renderizar el QR
  - Etiqueta para mostrar el ID único del usuario
  - Información descriptiva

- ✅ Implementada función `generateUserQR(userId)`:
  - Genera QR que redirige a `perfil-view.html?id={userId}`
  - URL única e irrepetible por usuario
  - Código QR con alta corrección de errores (nivel H)
  - Colores personalizados (verde del sitio)
  - Tamaño: 250x250px

- ✅ Integración en `loadProfile()`:
  - Genera automáticamente el QR al cargar el perfil
  - Se ejecuta después de cargar datos del usuario

**Ubicación del QR**: Abajo del botón "Editar Perfil", en una sección destacada con fondo verde

### 2. Archivo: perfil-view.html (NUEVO)
**Propósito**: Mostrar el perfil público de un usuario accedido mediante QR

#### Características:
- ✅ Página responsiva que muestra datos públicos del usuario:
  - Avatar/Foto de perfil
  - Nombre completo
  - Tipo de usuario (Admin/Jugador)
  - Email
  - Teléfono (si está disponible)
  - Tipo de usuario (Jugador/Agente/Comprador)
  - Fecha de registro

- ✅ Obtiene el ID de usuario del parámetro URL:
  - Formato: `perfil-view.html?id={userId}`
  - Valida que el ID sea válido

- ✅ Manejo de errores:
  - Si el ID es inválido, muestra error
  - Si el usuario no existe, muestra error
  - Botón para volver al inicio

- ✅ Seguridad:
  - Solo muestra datos públicos
  - No permite edición desde esta vista
  - No requiere autenticación

### 3. Archivo: detalle-operacion.html
**Propósito**: Mostrar lista de participantes inscritos en cada operación

#### Cambios realizados:

**HTML:**
- ✅ Agregada nueva sección "Participantes Inscritos"
- ✅ Contenedor con grid responsivo `#participantes-lista`
- ✅ Ubicada después del estado de inscripción y antes de historia/lore

**CSS:**
- ✅ Estilos para tarjeta de participante:
  - `.participante-card` - Tarjeta principal
  - `.participante-avatar` - Avatar circular (80x80px)
  - `.participante-name` - Nombre del participante
  - `.participante-email` - Email del participante
  - `.participante-status` - Estado (Registrado/Asistió)
  - `.participante-qr-btn` - Botón para ver perfil
  
- ✅ Efectos visuales:
  - Hover effect (levanta la tarjeta)
  - Animaciones suaves
  - Grid responsivo: 1 columna (móvil) → 2-3 columnas (desktop)

**JavaScript:**
- ✅ Nueva función `cargarParticipantes(operationId)`:
  - Fetch a endpoint `/api/operations/{id}/participants`
  - Procesa datos de cada participante
  - Renderiza tarjetas con información

- ✅ Nueva función `abrirPerfilParticipante(userId)`:
  - Redirige a `perfil-view.html?id={userId}`
  - Permite ver perfil completo del participante

- ✅ Integración en `cargarOperacion()`:
  - Llama a `cargarParticipantes()` después de cargar datos
  - Genera lista automáticamente

**Ubicación**: Sección completa entre "Estado de Inscripción" y "Historia/Lore"

## Endpoints Utilizados

### Backend (Ya existentes):
1. **GET `/api/operations/{id}/participants`**
   - Retorna lista de participantes de una operación
   - Incluye: user_id, user_name, user_email, status, joined_at

2. **GET `/api/users/{id}`**
   - Obtiene datos públicos del usuario
   - Retorna: name, email, phone, user_type, is_admin, created_at, photo, etc.

## Flujo de Usuario

### Obtener Código QR (Perfil):
1. Usuario logeado va a "Mi Perfil"
2. Ve su código QR único debajo del botón "Editar Perfil"
3. El QR se genera automáticamente con su ID de usuario
4. El QR es único e irrepetible (basado en el ID del usuario)

### Escanear Código QR:
1. Alguien escanea el QR (con app de cámara o app de QR)
2. Se abre `perfil-view.html?id={userId}`
3. Se carga el perfil público del usuario
4. Se muestra información general (nombre, email, teléfono, tipo)
5. Opción para volver al inicio

### Ver Participantes:
1. Usuario entra a detalle de operación
2. Ve sección "Participantes Inscritos"
3. Se muestran tarjetas de cada participante inscrito
4. Puede hacer click en "Ver Perfil" para acceder a `perfil-view.html`
5. Ve el perfil público del participante

## Características de Seguridad

✅ **Códigos QR Únicos**:
- Cada usuario tiene UN solo QR
- Basado en su ID de usuario único
- No se pueden falsificar sin el ID
- Permanente (no cambia mientras existe el usuario)

✅ **Acceso Restringido**:
- Solo muestra datos públicos en `perfil-view.html`
- No permite edición desde la vista pública
- Perfil de usuario logeado sigue siendo privado

✅ **Validación**:
- Verifica que el usuario exista antes de mostrar datos
- Manejo de errores si el ID es inválido

## Archivos Modificados

1. **perfil.html** - Agregado: librería QR, CSS, sección QR, función generateUserQR()
2. **detalle-operacion.html** - Agregado: sección participantes, CSS, funciones cargarParticipantes() y abrirPerfilParticipante()

## Archivos Creados

1. **perfil-view.html** - Nueva página para ver perfiles públicos de usuarios

## Testing

### Test 1: Ver código QR en perfil
```
1. Ir a http://localhost:8080/perfil.html
2. Iniciar sesión
3. Ver código QR abajo del botón "Editar Perfil"
4. El QR debe contener: http://localhost:8080/perfil-view.html?id={tu_id}
```

### Test 2: Acceder a perfil por QR
```
1. Escanear código QR (o acceder manualmente a: http://localhost:8080/perfil-view.html?id={id_usuario})
2. Ver perfil público del usuario
3. Ver información: nombre, email, teléfono, tipo, badge de admin
4. Botón "Volver al Inicio" funciona
```

### Test 3: Ver participantes en operación
```
1. Ir a detalle de operación: http://localhost:8080/detalle-operacion.html?id={op_id}
2. Scrollear hasta "Participantes Inscritos"
3. Ver tarjetas de cada participante inscrito
4. Información debe incluir: avatar, nombre, email, estado
5. Click en "Ver Perfil" abre perfil-view.html del participante
```

## URL de Operaciones de Prueba

```
http://localhost:8080/detalle-operacion.html?id=baaadb08-d674-4621-9aac-d2b0392dc734
http://localhost:8080/detalle-operacion.html?id=0ddd4193-9d11-4044-abe8-0dcdfa2bf1ee
http://localhost:8080/detalle-operacion.html?id=5c3f3159-253a-4316-97ee-c18fc2157ae0
```

## Notas Técnicas

- Librería QRCode.js genera QR en canvas (soportado en navegadores modernos)
- Los datos del usuario se cargan desde localStorage si está logeado
- Los participantes se cargan automáticamente sin requerir autenticación
- El endpoint de participantes es público (no requiere token)
- Los QR se generan con nivel de corrección H (puede recuperarse con 30% de daño)

## Estado: ✅ COMPLETADO

Ambas características han sido implementadas exitosamente:
1. ✅ Códigos QR únicos e irrepetibles por usuario
2. ✅ Lista de participantes en operaciones
3. ✅ Perfil público accesible mediante QR
4. ✅ Integración con interfaz existente
