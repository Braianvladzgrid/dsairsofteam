#!/bin/bash
# startup.sh - Script de inicio rápido para Death Squad Airsoft

echo "🚀 Iniciando Death Squad Airsoft..."
echo ""

# Cambiar a directorio de proyecto
cd /workspaces/dsairsofteam

# Verificar si el backend está corriendo
echo "📊 Verificando backend..."
if nc -z localhost 5000 2>/dev/null; then
    echo "✅ Backend ya está corriendo en puerto 5000"
else
    echo "🔄 Iniciando backend en puerto 5000..."
    python backend/app.py &
    sleep 2
    echo "✅ Backend iniciado"
fi

# Verificar si el frontend está corriendo
echo ""
echo "🌐 Verificando frontend..."
if nc -z localhost 8080 2>/dev/null; then
    echo "✅ Frontend ya está corriendo en puerto 8080"
else
    echo "🔄 Iniciando frontend en puerto 8080..."
    python -m http.server 8080 &
    sleep 1
    echo "✅ Frontend iniciado"
fi

echo ""
echo "=================================================="
echo "✨ ¡Sistema Death Squad Airsoft Iniciado!"
echo "=================================================="
echo ""
echo "📍 URLS:"
echo "   Frontend:  http://localhost:8080"
echo "   Backend:   http://localhost:5000"
echo ""
echo "👤 USUARIOS DE PRUEBA:"
echo "   Admin:  admin@dsairsofteam.local / Admin123!"
echo "   User:   user@example.com / password123"
echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "   1. Abre http://localhost:8080 en tu navegador"
echo "   2. Click 'Iniciar Sesión'"
echo "   3. Usa credenciales de admin"
echo "   4. Ve a Dashboard → Gestión de Operaciones"
echo "   5. Crea una nueva operación con imagen"
echo "   6. ¡Vuelve al inicio para ver tu operación!"
echo ""
echo "📚 DOCUMENTACIÓN:"
echo "   - PRUEBA_SISTEMA_COMPLETO.md (Guía completa)"
echo "   - SOLUCION_ADMIN_OPERACIONES.md (Cambios técnicos)"
echo ""
echo "=================================================="
