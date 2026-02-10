#!/bin/bash

# Script para acceso público usando LocalTunnel (sin registro requerido)

echo "🌍 Iniciando Death Squad Airsoft - ACCESO PÚBLICO"
echo "================================================="
echo ""

# Limpiar puertos ocupados
echo "🧹 Limpiando puertos..."
lsof -ti:5000,8080 | xargs -r kill -9 2>/dev/null
pkill -f "lt --port" 2>/dev/null
sleep 2

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "📥 Instalando Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Verificar si localtunnel está instalado
if ! command -v lt &> /dev/null; then
    echo "📥 Instalando localtunnel..."
    sudo npm install -g localtunnel
fi

# Navegar al backend
cd /workspaces/dsairsofteam/backend

# Instalar dependencias
echo "📦 Instalando dependencias Python..."
python -m pip install -q -r requirements.txt

# Inicializar base de datos
echo "🔧 Inicializando base de datos..."
python init_db.py

echo ""
echo "🚀 Iniciando Backend (Puerto 5000)..."
nohup python app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 4

if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Error al iniciar backend"
    cat /tmp/backend.log
    exit 1
fi
echo "✅ Backend iniciado (PID: $BACKEND_PID)"

# Crear servidor proxy simple
cd /workspaces/dsairsofteam
cat > /tmp/proxy_server.py << 'PROXY_EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
from urllib.parse import urlsplit

PORT = 8080
BACKEND_URL = "http://localhost:5000"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/workspaces/dsairsofteam", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_GET(self):
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('GET')
        else:
            super().do_GET()
    
    def do_POST(self):
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('POST')
        else:
            self.send_error(405)
    
    def do_PUT(self):
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('PUT')
        else:
            self.send_error(405)
    
    def do_DELETE(self):
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('DELETE')
        else:
            self.send_error(405)
    
    def do_PATCH(self):
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('PATCH')
        else:
            self.send_error(405)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def proxy_request(self, method):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            url = f"{BACKEND_URL}{self.path}"
            
            headers = {}
            if 'Content-Type' in self.headers:
                headers['Content-Type'] = self.headers['Content-Type']
            if 'Authorization' in self.headers:
                headers['Authorization'] = self.headers['Authorization']
            
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(key, value)
                self.end_headers()
                self.wfile.write(response.read())
        
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({'error': str(e)}).encode()
            self.wfile.write(error_response)

if __name__ == '__main__':
    class _ThreadingServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with _ThreadingServer(("", PORT), ProxyHandler) as httpd:
        print(f"Servidor corriendo en puerto {PORT}")
        httpd.serve_forever()
PROXY_EOF

echo "🌐 Iniciando Servidor Proxy (Puerto 8080)..."
nohup python /tmp/proxy_server.py > /tmp/proxy.log 2>&1 &
PROXY_PID=$!
sleep 3

if ! ps -p $PROXY_PID > /dev/null; then
    echo "❌ Error al iniciar proxy"
    cat /tmp/proxy.log
    exit 1
fi
echo "✅ Proxy iniciado (PID: $PROXY_PID)"

# Crear archivo de configuración
cat > /workspaces/dsairsofteam/config.js << 'EOF'
const API_URL = window.location.origin;
console.log('🌍 API configurada:', API_URL);
EOF

# Iniciar túnel con localtunnel
echo "🌐 Creando túnel público con LocalTunnel..."
nohup lt --port 8080 > /tmp/localtunnel.log 2>&1 &
LT_PID=$!
sleep 8

# Obtener URL del log
PUBLIC_URL=""
for i in {1..15}; do
    PUBLIC_URL=$(grep -oP 'https://[a-z0-9-]+\.loca\.lt' /tmp/localtunnel.log | head -1)
    if [ -n "$PUBLIC_URL" ]; then
        break
    fi
    echo "   Esperando túnel... ($i/15)"
    sleep 2
done

if [ -z "$PUBLIC_URL" ]; then
    echo "⚠️  Intentando método alternativo..."
    PUBLIC_URL=$(cat /tmp/localtunnel.log | grep -i "url is" | grep -oP 'https://[^ ]+' | head -1)
fi

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ No se pudo obtener URL pública"
    echo "Logs de localtunnel:"
    cat /tmp/localtunnel.log
    echo ""
    echo "💡 Pero el sistema está corriendo localmente en:"
    echo "   http://localhost:8080"
    PUBLIC_URL="http://localhost:8080 (solo local)"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║             🎉 SISTEMA INICIADO CON ÉXITO                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📡 URL PÚBLICA (compartible con cualquier dispositivo):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🌍 $PUBLIC_URL"
echo ""
echo "📱 URL LOCAL:"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🏠 http://localhost:8080"
echo ""
echo "💡 CÓMO USAR:"
echo "   1. Abre la URL pública en CUALQUIER navegador/dispositivo"
echo "   2. La primera vez puede pedir un código de verificación"
echo "   3. Haz clic en 'Click to Continue' en la página del túnel"
echo "   4. ¡Listo! Ya puedes usar la aplicación"
echo ""
echo "📝 Credenciales de prueba:"
echo "   📧 Email: admin@dsairsoft.com"
echo "   🔑 Password: admin123"
echo ""
echo "⚠️  NOTAS:"
echo "   - LocalTunnel puede mostrar una página de advertencia primero"
echo "   - Solo haz clic en 'Continue' para acceder"
echo "   - La URL funciona mientras este script esté activo"
echo "   - Para detener: Ctrl+C"
echo ""
echo "📝 PIDs:"
echo "   Backend: $BACKEND_PID | Proxy: $PROXY_PID | Túnel: $LT_PID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Función de limpieza
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $PROXY_PID $LT_PID 2>/dev/null
    pkill -f "lt --port" 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener vivo
echo "📡 Sistema activo. Ver logs:"
echo "   Backend: tail -f /tmp/backend.log"
echo "   Proxy: tail -f /tmp/proxy.log"
echo "   Túnel: tail -f /tmp/localtunnel.log"
echo ""

while true; do
    sleep 10
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo "⚠️  Backend detenido"
        cleanup
    fi
    if ! ps -p $PROXY_PID > /dev/null; then
        echo "⚠️  Proxy detenido"
        cleanup
    fi
done
