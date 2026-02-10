#!/usr/bin/env python3
"""
Script para actualizar las URLs de la API en todos los archivos HTML
"""
import os
import re
import sys

def update_api_url_in_file(filepath, new_api_url):
    """Actualiza la URL de la API en un archivo HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Patrones para encontrar y reemplazar la API URL
        patterns = [
            (r"const API_URL\s*=\s*['\"]https?://[^'\"]+['\"]",
             f"const API_URL = '{new_api_url}'"),
            (r"const API_BASE\s*=\s*['\"]https?://[^'\"]+['\"]",
             f"const API_BASE = '{new_api_url}'"),
            (r"const BASE_URL\s*=\s*['\"]https?://[^'\"]+['\"]",
             f"const BASE_URL = '{new_api_url}'"),
            (r"let API_URL\s*=\s*['\"]https?://[^'\"]+['\"]",
             f"let API_URL = '{new_api_url}'"),
            (r'fetch\([\'"]http://localhost:5000/',
             f"fetch('{new_api_url}/"),
            (r'fetch\([\'"]http://127\.0\.0\.1:5000/',
             f"fetch('{new_api_url}/"),
        ]
        
        changes_made = False
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
        
        # Si se hicieron cambios, guardar el archivo
        if changes_made and content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python update_api_urls.py <nueva_url_api>")
        print("Ejemplo: python update_api_urls.py https://abc123.ngrok.io")
        sys.exit(1)
    
    new_api_url = sys.argv[1].rstrip('/')
    workspace_dir = '/workspaces/dsairsofteam'
    
    print(f"🔄 Actualizando URLs de API a: {new_api_url}")
    print("━" * 60)
    
    # Buscar todos los archivos HTML
    html_files = []
    for root, dirs, files in os.walk(workspace_dir):
        # Ignorar carpetas específicas
        dirs[:] = [d for d in dirs if d not in ['backend', 'instance', '.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    updated_count = 0
    for filepath in html_files:
        if update_api_url_in_file(filepath, new_api_url):
            print(f"✅ Actualizado: {os.path.basename(filepath)}")
            updated_count += 1
        else:
            print(f"⏭️  Sin cambios: {os.path.basename(filepath)}")
    
    print("━" * 60)
    print(f"✨ Proceso completado: {updated_count} archivos actualizados")

if __name__ == '__main__':
    main()
