#!/bin/bash

# Script para iniciar el sistema con acceso público usando ngrok

echo "🌍 Iniciando Death Squad Airsoft - ACCESO PÚBLICO"
echo "=================================================="
echo ""

# Limpiar puertos ocupados
echo "🧹 Limpiando puertos..."
lsof -ti:5000,8000,4040,4041 | xargs -r kill -9 2>/dev/null
pkill -f ngrok 2>/dev/null
sleep 2

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "📥 Instalando ngrok..."
    
    # Detectar arquitectura
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
        NGROK_ARCH="amd64"
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
        NGROK_ARCH="arm64"
    else
        NGROK_ARCH="386"
    fi
    
    # Descargar ngrok
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-${NGROK_ARCH}.tgz -O /tmp/ngrok.tgz
    tar -xzf /tmp/ngrok.tgz -C /tmp/
    sudo mv /tmp/ngrok /usr/local/bin/
    rm /tmp/ngrok.tgz
    
    echo "✅ ngrok instalado"
fi

# Verificar si ngrok está configurado con authtoken
echo "🔐 Verificando configuración de ngrok..."
if [ ! -f ~/.ngrok2/ngrok.yml ]; then
    echo ""
    echo "⚠️  IMPORTANTE: Para usar múltiples túneles necesitas registrarte en ngrok"
    echo "   1. Visita: https://dashboard.ngrok.com/signup"
    echo "   2. Copia tu authtoken"
    echo "   3. Ejecuta: ngrok config add-authtoken TU_TOKEN"
    echo ""
    echo "   💡 Por ahora usaremos una configuración alternativa..."
    echo ""
fi

# Navegar al backend
cd /workspaces/dsairsofteam/backend

# Instalar dependencias
echo "📦 Instalando dependencias..."
python -m pip install -q -r requirements.txt

# Inicializar base de datos
echo "🔧 Inicializando base de datos..."
python init_db.py

echo ""
echo "🚀 Iniciando Backend (Puerto 5000)..."
nohup python app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 4

# Verificar que el backend esté corriendo
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Error al iniciar backend"
    cat /tmp/backend.log
    exit 1
fi

echo "✅ Backend iniciado (PID: $BACKEND_PID)"

# Iniciar túnel ngrok para backend
echo "🌐 Creando túnel público para Backend..."
nohup ngrok http 5000 --log=stdout > /tmp/ngrok_backend.log 2>&1 &
NGROK_BACKEND_PID=$!
sleep 5

# Obtener URL pública del backend
BACKEND_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)

if [ -z "$BACKEND_URL" ]; then
    echo "❌ Error: No se pudo obtener la URL pública del backend"
    echo "Verifica que ngrok esté funcionando correctamente"
    cat /tmp/ngrok_backend.log
    exit 1
fi

echo "✅ Backend público en: $BACKEND_URL"

# Crear archivo de configuración para el frontend
cat > /workspaces/dsairsofteam/config.js << EOF
// Configuración automática generada
const API_URL = '${BACKEND_URL}';
console.log('🌍 API URL configurada:', API_URL);
EOF

# Iniciar frontend
cd /workspaces/dsairsofteam
echo "🌐 Iniciando Frontend (Puerto 8000)..."
nohup python -m http.server 8000 > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 3

if ! ps -p $FRONTEND_PID > /dev/null; then
    echo "❌ Error al iniciar frontend"
    cat /tmp/frontend.log
    exit 1
fi

echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"

# Iniciar túnel ngrok para frontend en puerto diferente
echo "🌐 Creando túnel público para Frontend..."
nohup ngrok http 8000 --log=stdout > /tmp/ngrok_frontend.log 2>&1 &
NGROK_FRONTEND_PID=$!
sleep 5

# Obtener URL pública del frontend
FRONTEND_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print([t['public_url'] for t in data.get('tunnels', []) if '8000' in t['config']['addr']][0] if data.get('tunnels') else '')" 2>/dev/null)

if [ -z "$FRONTEND_URL" ]; then
    # Método alternativo
    FRONTEND_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); tunnels=data.get('tunnels', []); print(tunnels[1]['public_url'] if len(tunnels) > 1 else tunnels[0]['public_url'] if tunnels else '')" 2>/dev/null)
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  🎉 SISTEMA INICIADO CON ÉXITO               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📡 URLs PÚBLICAS (compartibles con cualquier dispositivo):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🌐 Frontend: $FRONTEND_URL"
echo "   🔌 Backend:  $BACKEND_URL"
echo ""
echo "📱 URLs LOCALES (solo en tu red):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🌐 Frontend: http://localhost:8000"
echo "   🔌 Backend:  http://localhost:5000"
echo ""
echo "📊 Panel de ngrok: http://localhost:4040"
echo ""
echo "💡 CÓMO USAR:"
echo "   1. Abre $FRONTEND_URL en cualquier dispositivo"
echo "   2. El frontend automáticamente se conectará al backend"
echo "   3. Comparte la URL del frontend con otros dispositivos"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Las URLs públicas funcionan mientras este script esté activo"
echo "   - Para detener: presiona Ctrl+C"
echo "   - Las URLs de ngrok gratis cambian cada vez que reinicias"
echo ""
echo "📝 PIDs de procesos:"
echo "   Backend: $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo "   Ngrok Backend: $NGROK_BACKEND_PID"
echo "   Ngrok Frontend: $NGROK_FRONTEND_PID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID $NGROK_BACKEND_PID $NGROK_FRONTEND_PID 2>/dev/null
    pkill -f ngrok 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener el script vivo y mostrar logs
echo "📡 Monitoreando servicios (ver logs en /tmp/*.log)..."
echo ""

while true; do
    sleep 10
    # Verificar que los servicios sigan corriendo
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo "⚠️  Backend se detuvo inesperadamente"
        cat /tmp/backend.log | tail -20
        cleanup
    fi
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo "⚠️  Frontend se detuvo inesperadamente"
        cleanup
    fi
done
