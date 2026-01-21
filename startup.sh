#!/bin/bash
# Script de inicio rápido - DSAirsoft Team

echo "🚀 DSAirsoft Team - Quick Start"
echo "================================"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo -e "${BLUE}📦 Verificando Python...${NC}"
python3 --version || { echo "❌ Python 3 no instalado"; exit 1; }

# 2. Crear entorno virtual
echo -e "${BLUE}📁 Creando entorno virtual...${NC}"
cd backend
python3 -m venv venv || { echo "❌ Error creando venv"; exit 1; }

# 3. Activar entorno
echo -e "${BLUE}✅ Activando entorno...${NC}"
source venv/bin/activate || source venv/Scripts/activate

# 4. Instalar dependencias
echo -e "${BLUE}📚 Instalando dependencias...${NC}"
pip install -r requirements.txt || { echo "❌ Error instalando dependencias"; exit 1; }

# 5. Inicializar BD
echo -e "${BLUE}🗄️  Inicializando base de datos...${NC}"
python init_db.py || echo "⚠️  Error en BD (verifica que PostgreSQL está corriendo)"

# 6. Iniciar servidor
echo ""
echo -e "${GREEN}✅ ¡Backend listo!${NC}"
echo -e "${YELLOW}🚀 Iniciando servidor en http://localhost:5000${NC}"
echo ""
echo -e "Credenciales Admin:"
echo -e "${BLUE}Email: admin@dsairsofteam.local${NC}"
echo -e "${BLUE}Password: Admin123!${NC}"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "================================"
echo ""

# Iniciar servidor
python app.py
