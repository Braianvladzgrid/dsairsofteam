#!/bin/bash

# Script simplificado para acceso público usando solo backend con ngrok

echo "🌍 Iniciando Death Squad Airsoft - ACCESO PÚBLICO (Versión Simple)"
echo "==================================================================="
echo ""

# Limpiar puertos ocupados
echo "🧹 Limpiando puertos..."
lsof -ti:5000,8080,4040 | xargs -r kill -9 2>/dev/null
pkill -f ngrok 2>/dev/null
sleep 2

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "📥 Instalando ngrok..."
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
        NGROK_ARCH="amd64"
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
        NGROK_ARCH="arm64"
    else
        NGROK_ARCH="386"
    fi
    
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-${NGROK_ARCH}.tgz -O /tmp/ngrok.tgz
    tar -xzf /tmp/ngrok.tgz -C /tmp/
    sudo mv /tmp/ngrok /usr/local/bin/
    rm /tmp/ngrok.tgz
    echo "✅ ngrok instalado"
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

if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Error al iniciar backend"
    cat /tmp/backend.log
    exit 1
fi
echo "✅ Backend iniciado (PID: $BACKEND_PID)"

# Crear servidor proxy simple que sirva frontend y proxy al backend
cd /workspaces/dsairsofteam
cat > /tmp/proxy_server.py << 'PROXY_EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.error
import json
from urllib.parse import urlparse, parse_qs
from urllib.parse import urlsplit

PORT = 8080
BACKEND_URL = "http://localhost:5000"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Si es una ruta de API, hacer proxy al backend
        path_only = urlsplit(self.path).path
        if path_only.startswith('/api'):
            self.proxy_request('GET')
        else:
            # Servir archivos estáticos
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
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def proxy_request(self, method):
        try:
            # Leer el body si existe
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Construir URL completa
            url = f"{BACKEND_URL}{self.path}"
            
            # Crear request
            headers = {
                'Content-Type': self.headers.get('Content-Type', 'application/json'),
            }
            if 'Authorization' in self.headers:
                headers['Authorization'] = self.headers['Authorization']
            
            req = urllib.request.Request(url, data=body, headers=headers, method=method)
            
            # Hacer request al backend
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                
                # Copiar headers
                for key, value in response.headers.items():
                    if key.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(key, value)
                
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Copiar body
                self.wfile.write(response.read())
        
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = json.dumps({'error': str(e)}).encode()
            self.wfile.write(error_response)

if __name__ == '__main__':
    class _ThreadingServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with _ThreadingServer(("", PORT), ProxyHandler) as httpd:
        print(f"Proxy server running on port {PORT}")
        httpd.serve_forever()
PROXY_EOF

echo "🌐 Iniciando Servidor Proxy con Frontend (Puerto 8080)..."
cd /workspaces/dsairsofteam
nohup python /tmp/proxy_server.py > /tmp/proxy.log 2>&1 &
PROXY_PID=$!
sleep 3

if ! ps -p $PROXY_PID > /dev/null; then
    echo "❌ Error al iniciar proxy"
    cat /tmp/proxy.log
    exit 1
fi
echo "✅ Proxy iniciado (PID: $PROXY_PID)"

# Crear archivo de configuración para que el frontend use URLs relativas
cat > /workspaces/dsairsofteam/config.js << 'EOF'
// Configuración para acceso público
// El proxy maneja las llamadas a /api/*
const API_URL = window.location.origin;
console.log('🌍 Modo público: API URL =', API_URL);
EOF

# Iniciar túnel ngrok para el proxy
echo "🌐 Creando túnel público..."
nohup ngrok http 8080 --log=stdout > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
sleep 6

# Obtener URL pública
PUBLIC_URL=""
for i in {1..10}; do
    PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'] if data.get('tunnels') else '')" 2>/dev/null)
    if [ -n "$PUBLIC_URL" ]; then
        break
    fi
    echo "   Esperando túnel ngrok... ($i/10)"
    sleep 2
done

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ Error: No se pudo obtener la URL pública"
    echo "Verifica los logs: cat /tmp/ngrok.log"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║             🎉 SISTEMA INICIADO CON ÉXITO                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📡 URL PÚBLICA (compartible con cualquier dispositivo):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🌍 Aplicación: $PUBLIC_URL"
echo ""
echo "📱 URL LOCAL (solo en tu red):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   🌍 Aplicación: http://localhost:8080"
echo ""
echo "📊 Panel de ngrok: http://localhost:4040"
echo ""
echo "💡 CÓMO USAR:"
echo "   1. Abre $PUBLIC_URL en CUALQUIER dispositivo"
echo "   2. Comparte esta URL con quien quieras"
echo "   3. Funciona en móviles, tablets, otras PCs, etc."
echo ""
echo "📝 Credenciales de prueba:"
echo "   Email: admin@dsairsoft.com"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - La URL funciona mientras este script esté activo"
echo "   - Para detener: presiona Ctrl+C"
echo "   - La URL cambia cada vez que reinicias (versión gratis)"
echo ""
echo "📝 PIDs de procesos:"
echo "   Backend: $BACKEND_PID"
echo "   Proxy: $PROXY_PID"
echo "   Ngrok: $NGROK_PID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $PROXY_PID $NGROK_PID 2>/dev/null
    pkill -f ngrok 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener el script vivo
echo "📡 Sistema funcionando. Monitorea en http://localhost:4040"
echo ""

while true; do
    sleep 10
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo "⚠️  Backend se detuvo"
        cat /tmp/backend.log | tail -20
        cleanup
    fi
    if ! ps -p $PROXY_PID > /dev/null; then
        echo "⚠️  Proxy se detuvo"
        cat /tmp/proxy.log | tail -20
        cleanup
    fi
done
