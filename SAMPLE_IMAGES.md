# Imágenes de Prueba para Operaciones

## URLs de Prueba (Placeholder Images)

Puedes usar estas URLs directamente en el campo de imagen:

### Imágenes Genéricas
```
https://via.placeholder.com/400x300?text=Milsim+Operation
https://via.placeholder.com/400x300?text=Picado+Event
https://via.placeholder.com/400x300?text=Airsoft+Competition
https://via.placeholder.com/400x300?text=Tactical+Combat
```

### Imágenes Airsoft (Real Images)
```
https://images.unsplash.com/photo-1579546475815-839f5eb8e8f9?w=400&h=300&fit=crop
https://images.unsplash.com/photo-1579546475815-839f5eb8e8f9?w=400&h=300&fit=crop
https://images.unsplash.com/photo-1580541029353-17b5ccb59f92?w=400&h=300&fit=crop
```

## Cómo Copiar URLs

1. Ve a admin.html
2. Crea una nueva operación
3. En el campo "Imagen (Base64 o URL)"
4. Pega una de las URLs de arriba
5. Verás el preview de la imagen
6. Haz click en "Guardar Operación"

## Base64 Mínimo de Prueba

Si quieres probar con un pequeño PNG rojo:
```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg==
```

## Recomendación

**Usa URLs en lugar de Base64** para desarrollo local porque:
- ✓ Más fácil de copiar/pegar
- ✓ Carga rápida
- ✓ No depende de conversiones
- ✓ Se ve igual en el frontend

## Ejemplo Completo

Al crear una operación:
```
Título: Milsim Warehouse CQB
Tipo: milsim
Precio: 150
Ubicación: Buenos Aires, Argentina
Fecha: 2026-02-28
Imagen: https://via.placeholder.com/400x300?text=Milsim+Operation
```

Resultado: ✓ Operación creada con imagen visible
