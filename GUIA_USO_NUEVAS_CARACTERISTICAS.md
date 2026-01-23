# 🎯 GUÍA DE USO - Nuevas Características

## 1️⃣ EDICIÓN DE OPERACIONES EN DASHBOARD

### Cómo acceder:
1. Ir a: `http://localhost:8080/admin-panel.html`
2. Iniciar sesión (admin@dsairsofteam.local / Admin123!)
3. Hacer click en la pestaña "Operaciones"

### Crear nueva operación:
1. Click en botón azul "+ Nueva Operación"
2. Llenar los 14 campos disponibles:
   - **Básicos**: Título, Tipo, Precio, Descripción
   - **Detalles**: Lore/Escenario, Ubicación
   - **Fechas**: Inicio, Fin
   - **Participantes**: Máximo de participantes
   - **Requisitos**: Requisitos (separados por coma)
   - **Reglas**: Reglas (separadas por coma)
   - **Imagen**: URL de imagen
   - **Estado**: Active/Completada/Cancelada
   - **Público**: Checkbox para mostrar en listado
   - **Notas**: Notas internas

3. Click en "✓ Crear Operación"

### Editar operación existente:
1. En tabla de operaciones, buscar la fila
2. Click en botón ✏️ (edit) del lado derecho
3. El formulario se llena automáticamente
4. Modificar los campos que desees
5. Click en "✓ Actualizar Operación"

### Funciones adicionales:
- **Toggle**: Click en ▼ o ▲ para activar/desactivar
- **Eliminar**: Click en 🗑️ para eliminar (confirmación)

### Campos editables:
| Campo | Obligatorio | Tipo |
|-------|-----------|------|
| Título | ✅ | Texto |
| Tipo | ✅ | Select (6 tipos airsoft) |
| Precio | ✅ | Número |
| Fecha Inicio | ✅ | Fecha/Hora |
| Descripción | ❌ | Texto largo |
| Lore | ❌ | Texto largo |
| Ubicación | ❌ | Texto |
| Fecha Fin | ❌ | Fecha/Hora |
| Máx Participantes | ❌ | Número |
| Requisitos | ❌ | Lista (comas) |
| Reglas | ❌ | Lista (comas) |
| Imagen | ❌ | URL |
| Estado | ❌ | Select |
| Activa | ❌ | Checkbox |

---

## 2️⃣ CÓDIGOS QR ÚNICOS POR USUARIO

### Ver tu código QR:
1. Estar logeado en la plataforma
2. Ir a: `http://localhost:8080/perfil.html`
3. Verás una sección verde con tu código QR
4. El QR está justo debajo del botón "Editar Perfil"
5. Tu ID único se muestra abajo del QR

### Características del QR:
- ✅ **Único**: Cada usuario tiene UN solo QR
- ✅ **Permanente**: No cambia mientras exista tu cuenta
- ✅ **Irrepetible**: No se puede duplicar sin tu ID
- ✅ **Acceso público**: Cualquiera puede escanear

### Compartir tu QR:
1. Tomar screenshot del código QR
2. Compartirlo por WhatsApp, email, etc.
3. Otros pueden escanear con cámara del teléfono
4. Se abre automáticamente tu perfil público

### QR redirige a:
```
http://localhost:8080/perfil-view.html?id={tu_id_usuario}
```

---

## 3️⃣ PERFIL PÚBLICO (ACCESIBLE POR QR)

### Quién puede verlo:
- ✅ Cualquiera que escanee el QR
- ✅ Cualquiera que acceda con URL directa
- ✅ No requiere estar logeado

### Qué información se muestra:
- 👤 Foto/Avatar del usuario
- 📝 Nombre completo
- ✉️ Email
- 📞 Teléfono (si está disponible)
- 🎖️ Tipo (Jugador/Agente/Comprador)
- 👑 Badge si es Admin
- 📅 Fecha de registro

### Qué información NO se muestra:
- ❌ Contraseña
- ❌ Documento/Cédula
- ❌ Dirección completa
- ❌ Datos bancarios
- ❌ Información privada

### Acceso directo sin escanear:
```
http://localhost:8080/perfil-view.html?id=ef262e80-917a-4840-8969-7e3653f5c7e9
```
(Reemplazar el ID con el del usuario)

---

## 4️⃣ VER PARTICIPANTES DE OPERACIÓN

### Cómo ver participantes:
1. Ir a detalle de operación:
   ```
   http://localhost:8080/detalle-operacion.html?id={id_operacion}
   ```

2. Scrollear hacia abajo hasta la sección:
   **"Participantes Inscritos"** 🎖️

3. Verás tarjetas de cada participante con:
   - Foto del participante
   - Nombre completo
   - Email
   - Estado (Registrado/Asistió)
   - Botón "Ver Perfil"

### Información en cada tarjeta:
```
┌─────────────────────┐
│   [FOTO AVATAR]     │
│  Nombre del Usuario │
│ email@ejemplo.com   │
│  [📝 Registrado]    │
│  [👤 Ver Perfil]    │
└─────────────────────┘
```

### Click en "Ver Perfil":
- Abre el perfil público del participante
- Misma información que el QR
- Puedes ver todos sus datos públicos

### Ejemplos de operaciones:
```
http://localhost:8080/detalle-operacion.html?id=0ddd4193-9d11-4044-abe8-0dcdfa2bf1ee
http://localhost:8080/detalle-operacion.html?id=5c3f3159-253a-4316-97ee-c18fc2157ae0
```

---

## 🔐 SEGURIDAD Y PRIVACIDAD

### Códigos QR:
- ✅ Cada QR es único por usuario
- ✅ Basados en ID de usuario (no pueden falsificarse)
- ✅ Solo información pública se comparte
- ✅ Se puede cambiar privacidad en perfil personal

### Participantes:
- ✅ Solo se muestran los inscritos
- ✅ Información pública disponible
- ✅ No hay datos privados expuestos
- ✅ Email visible (para contacto)

---

## 📱 FUNCIONAMIENTO EN MÓVIL

### QR Code Scanner (iOS):
1. Abrir Cámara
2. Apuntar al QR
3. Click en notificación
4. Se abre el perfil automáticamente

### QR Code Scanner (Android):
1. Instalar app "QR Code Scanner"
2. Abrir app
3. Apuntar al QR
4. Click en resultado
5. Se abre el perfil automáticamente

### Acceso directo desde móvil:
- Copiar URL del QR
- Pegar en navegador
- Ver perfil sin escanear

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### El QR no aparece en mi perfil:
1. Verificar que estés logeado
2. Refresh la página (Ctrl+F5)
3. Verificar que JavaScript esté habilitado
4. Intentar en otro navegador

### El QR escanea pero abre página blanca:
1. El ID puede ser inválido
2. El usuario fue eliminado
3. Verificar URL en la notificación

### Los participantes no aparecen:
1. Verificar que hay inscritos en la operación
2. Refresh la página
3. Verificar que la operación existe
4. Abrir consola (F12) para ver errores

### Participante no aparece en lista:
1. Verificar que se inscribió correctamente
2. Puede no haberse confirmado aún
3. Refrescar página de detalle

---

## 💡 TIPS Y TRUCOS

### Para admins:
- Editar rápido: Click en ✏️ en lugar de crear nuevo
- Tipos airsoft: Milsim, Picado, Especial, Realista, Histórica, Semi Milsim
- Requisitos/Reglas: Usar comas para separar items

### Para usuarios:
- Compartir QR es seguro (solo datos públicos)
- El perfil público se actualiza automáticamente
- QR nunca cambia mientras exista la cuenta

### Para operadores:
- Ver participantes antes de iniciar operación
- Copiar emails para enviar recordatorios
- Verificar estados (Registrado vs Asistió)

---

## 📞 CONTACTO Y SOPORTE

Si encuentras problemas:
1. Verificar consola del navegador (F12)
2. Revisar URL y parámetros
3. Verificar que el backend está corriendo (http://localhost:5000)
4. Revisar documentación técnica en IMPLEMENTACION_QR_Y_PARTICIPANTES.md

---

## ✅ CHECKLIST DE FUNCIONALIDAD

- [ ] Puedo editar operaciones
- [ ] Veo mis requisitos y reglas guardados
- [ ] Mi código QR se genera en el perfil
- [ ] El QR se abre en el navegador
- [ ] El perfil público se ve correctamente
- [ ] Puedo ver participantes en operaciones
- [ ] El botón "Ver Perfil" funciona
- [ ] Los datos se muestran correctamente

---

**Para más detalles técnicos, ver:**
- `CAMBIOS_EDICION_OPERACIONES.md`
- `IMPLEMENTACION_QR_Y_PARTICIPANTES.md`
- `RESUMEN_FINAL_SESION.md`
