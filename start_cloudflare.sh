#!/bin/bash

# Script para acceso público usando Cloudflare Tunnel (sin verificaciones)

echo "🌍 Iniciando Death Squad Airsoft - CLOUDFLARE TUNNEL"
echo "===================================================="
echo ""

# Limpiar procesos anteriores
echo "🧹 Limpiando servicios anteriores..."
pkill -f "lt --port" 2>/dev/null
pkill -f "start_localtunnel" 2>/dev/null
pkill -f "cloudflared" 2>/dev/null
lsof -ti:5000,8080 | xargs -r kill -9 2>/dev/null
sleep 2

# Verificar si cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo "📥 Instalando Cloudflare Tunnel..."
    wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /tmp/cloudflared
    chmod +x /tmp/cloudflared
    sudo mv /tmp/cloudflared /usr/local/bin/cloudflared
    echo "✅ Cloudflare Tunnel instalado"
fi

# Iniciar backend
cd /workspaces/dsairsofteam/backend
echo "📦 Instalando dependencias..."
python -m pip install -q -r requirements.txt

echo "🔧 Inicializando base de datos..."
python init_db.py

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

# Crear servidor proxy
cd /workspaces/dsairsofteam
cat > /tmp/proxy_server.py << 'PROXY_EOF'
#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import urllib.error
import json
from urllib.parse import urlsplit

PORT = 8080
BACKEND_URL = "http://localhost:5000"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/workspaces/dsairsofteam", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
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

# Iniciar Cloudflare Tunnel
echo "🌐 Creando túnel público con Cloudflare..."
echo "   (Esto puede tardar unos segundos...)"
nohup cloudflared tunnel --url http://localhost:8080 > /tmp/cloudflared.log 2>&1 &
CF_PID=$!
sleep 8

# Obtener URL del log
PUBLIC_URL=""
for i in {1..20}; do
    PUBLIC_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cloudflared.log | head -1)
    if [ -n "$PUBLIC_URL" ]; then
        break
    fi
    echo "   Esperando túnel... ($i/20)"
    sleep 2
done

if [ -z "$PUBLIC_URL" ]; then
    echo "⚠️  Intentando método alternativo..."
    PUBLIC_URL=$(cat /tmp/cloudflared.log | grep -i "https://" | grep -oP 'https://[^ ]+' | head -1)
fi

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ No se pudo obtener URL pública"
    echo "Logs de cloudflared:"
    cat /tmp/cloudflared.log
    echo ""
    echo "💡 Sistema corriendo localmente en: http://localhost:8080"
    PUBLIC_URL="http://localhost:8080 (solo local)"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          🎉 SISTEMA INICIADO CON ÉXITO                       ║"
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
echo "💡 VENTAJAS DE CLOUDFLARE TUNNEL:"
echo "   ✅ SIN página de verificación"
echo "   ✅ SIN contraseña requerida"
echo "   ✅ Acceso directo e inmediato"
echo "   ✅ HTTPS incluido automáticamente"
echo ""
echo "🚀 CÓMO USAR:"
echo "   1. Abre la URL pública en CUALQUIER dispositivo"
echo "   2. ¡Listo! Acceso directo a la aplicación"
echo "   3. Inicia sesión con las credenciales"
echo ""
echo "📝 Credenciales de prueba:"
echo "   📧 Email: admin@dsairsoft.com"
echo "   🔑 Password: admin123"
echo ""
echo "⚠️  NOTAS:"
echo "   - La URL funciona mientras este script esté activo"
echo "   - Para detener: Ctrl+C"
echo "   - La URL cambia cada vez que reinicias"
echo ""
echo "📝 PIDs:"
echo "   Backend: $BACKEND_PID | Proxy: $PROXY_PID | Tunnel: $CF_PID"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Presiona Ctrl+C para detener todos los servicios"
echo ""

# Función de limpieza
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $PROXY_PID $CF_PID 2>/dev/null
    pkill -f cloudflared 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Mantener vivo
echo "📡 Sistema activo. Ver logs:"
echo "   Backend: tail -f /tmp/backend.log"
echo "   Proxy: tail -f /tmp/proxy.log"
echo "   Túnel: tail -f /tmp/cloudflared.log"
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
