#!/bin/bash

# Script para iniciar todo el sistema Death Squad Airsoft

echo "🚀 Iniciando Death Squad Airsoft System"
echo "========================================"
echo ""

# Limpiar puertos ocupados
echo "🧹 Limpiando puertos..."
lsof -ti:5000,8000 | xargs -r kill -9 2>/dev/null
sleep 1

# Navegar al backend
cd /workspaces/dsairsofteam/backend

# Verificar dependencias
echo "📦 Verificando dependencias..."
python -m pip install -q -r requirements.txt

# Inicializar base de datos
echo "🔧 Inicializando base de datos..."
python init_db.py

echo ""
echo "🚀 Iniciando Backend (Puerto 5000)..."
nohup python app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

# Verificar que el backend esté corriendo
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend iniciado (PID: $BACKEND_PID)"
else
    echo "❌ Error al iniciar backend"
    cat /tmp/backend.log
    exit 1
fi

# Iniciar frontend
cd /workspaces/dsairsofteam
echo "🌐 Iniciando Frontend (Puerto 8000)..."
nohup python -m http.server 8000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 2

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"
else
    echo "❌ Error al iniciar frontend"
    exit 1
fi

echo ""
echo "════════════════════════════════════════"
echo "✅ Sistema iniciado correctamente!"
echo ""
echo "🌐 URLs:"
echo "   Frontend: http://localhost:8000"
echo "   Backend:  http://localhost:5000"
echo "   Admin:    http://localhost:8000/admin-operaciones.html"
echo ""
echo "👤 Usuario admin por defecto:"
echo "   Email:    admin@dsairsofteam.local"
echo "   Password: Admin123!"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo "🛑 Para detener: pkill -f 'python.*app.py'; pkill -f 'python.*http.server'"
echo "════════════════════════════════════════"
