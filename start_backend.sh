#!/bin/bash

# Script para iniciar el servidor backend de Death Squad Airsoft

echo "🚀 Iniciando Death Squad Airsoft - Backend"
echo "=========================================="
echo ""

# Navegar al directorio del backend
cd /workspaces/dsairsofteam/backend

echo "📦 Instalando dependencias..."
python -m pip install -r requirements.txt -q

echo ""
echo "🔧 Inicializando base de datos..."
python init_db.py

echo ""
echo "✅ Backend listo!"
echo ""
echo "═════════════════════════════════════════"
echo "🌐 Servidor disponible en: http://localhost:5000"
echo ""
echo "📊 Admin Panel: http://localhost:8000/admin.html"
echo "🎮 Frontend: http://localhost:8000/index.html"
echo ""
echo "📝 Ver TEST_GUIDE.md para instrucciones completas"
echo "═════════════════════════════════════════"
echo ""

# Iniciar el servidor
python app.py
