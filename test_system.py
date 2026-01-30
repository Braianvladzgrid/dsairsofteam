#!/usr/bin/env python3
"""
Script para probar el sistema creando datos de ejemplo
"""

import requests
import json
from datetime import datetime, timedelta

API_BASE = 'http://localhost:5000/api'

def login(email: str, password: str, label: str = ""):
    """Login y obtención de token"""
    prefix = f" ({label})" if label else ""
    print(f"[login] Probando login{prefix}...")
    response = requests.post(
        f'{API_BASE}/auth/login',
        json={'email': email, 'password': password},
        timeout=10,
    )

    if response.status_code == 200:
        data = response.json()
        print(f"[ok] Login exitoso: {data['user']['email']}")
        return data['token'], data['user']

    print(f"❌ Error en login: {response.status_code} {response.text}")
    return None, None


def ensure_test_user(email: str, password: str):
    token, user = login(email, password, label="usuario")
    if token:
        return token, user

    print("[register] Intentando registrar usuario de prueba...")
    response = requests.post(
        f'{API_BASE}/auth/register',
        json={
            'name': 'Usuario Prueba',
            'email': email,
            'password': password,
            'phone': '000000000',
            'user_type': 'player'
        },
        timeout=10,
    )

    if response.status_code in (200, 201):
        data = response.json()
        print(f"[ok] Usuario registrado: {data['user']['email']}")
        return data['token'], data['user']

    # Si ya existe, reintentar login
    if response.status_code == 409:
        print("[info] Usuario ya existía. Reintentando login...")
        return login(email, password, label="usuario")

    print(f"❌ No se pudo registrar usuario: {response.status_code} {response.text}")
    return None, None

def test_create_operation(token):
    """Crear operación de prueba"""
    print("\n[operation] Creando operación de ejemplo...")
    
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(hours=6)
    
    operation_data = {
        'type': 'milsim',
        'title': 'Operación Tormenta Roja',
        'description': 'Milsim ambientada en la Guerra Fría. Dos equipos enfrentados en un escenario táctico realista.',
        'lore': 'Año 1987. Un convoy desaparece y el equipo debe infiltrar la zona para recuperar inteligencia.',
        'requirements': [
            'Protección ocular obligatoria (goggles certificados)',
            'Réplica funcional y crono al ingreso',
            'Botella de agua / hidratación'
        ],
        'rules': [
            'Código de honor: canta impactos y respeta al staff',
            'Prohibido disparar a corta distancia sin identificar',
            'Alcohol 0 durante el evento'
        ],
        'price': 50.00,
        'location': 'Campo Táctico Los Pinos',
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'max_participants': 40,
        'image': 'https://images.unsplash.com/photo-1526772662000-3f88f10405ff?w=400',
        'is_active': True
    }
    
    response = requests.post(
        f'{API_BASE}/operations',
        json=operation_data,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code == 201:
        print("[ok] Operación creada exitosamente")
        return response.json()
    else:
        print(f"❌ Error creando operación: {response.status_code}")
        print(response.text)
        return None

def test_get_operations():
    """Obtener todas las operaciones"""
    print("\n[operations] Obteniendo operaciones...")
    response = requests.get(f'{API_BASE}/operations')
    
    if response.status_code == 200:
        ops = response.json()
        print(f"[ok] Operaciones encontradas: {len(ops)}")
        for op in ops:
            print(f"   - {op['title']} ({op['type']}) - ${op['price']}")
        return ops
    else:
        print(f"❌ Error obteniendo operaciones: {response.text}")
        return []


def test_registration_flow(operation_id: str, user_token: str):
    """Probar is-registered / join / join idempotente / leave"""
    print("\n[registration] Probando inscripción a operación...")

    headers = {'Authorization': f'Bearer {user_token}', 'Accept': 'application/json'}

    r0 = requests.get(f'{API_BASE}/operations/{operation_id}/is-registered', headers=headers, timeout=10)
    if r0.status_code == 200:
        print(f"ℹ️  is-registered inicial: {r0.json().get('registered')}")
    else:
        print(f"❌ Error is-registered inicial: {r0.status_code} {r0.text}")
        return

    join_body = {'accept_requirements': True, 'accept_rules': True}
    r1 = requests.post(f'{API_BASE}/operations/{operation_id}/join', headers=headers, json=join_body, timeout=10)
    if r1.status_code in (200, 201):
        print(f"[ok] Join OK (status {r1.status_code})")
    else:
        print(f"❌ Error join: {r1.status_code} {r1.text}")
        return

    # Join idempotente
    r2 = requests.post(f'{API_BASE}/operations/{operation_id}/join', headers=headers, json=join_body, timeout=10)
    if r2.status_code in (200, 201):
        print(f"[ok] Join idempotente OK (status {r2.status_code})")
    else:
        print(f"❌ Error join idempotente: {r2.status_code} {r2.text}")

    r3 = requests.get(f'{API_BASE}/operations/{operation_id}/is-registered', headers=headers, timeout=10)
    if r3.status_code == 200:
        print(f"ℹ️  is-registered luego de join: {r3.json().get('registered')}")
    else:
        print(f"❌ Error is-registered luego de join: {r3.status_code} {r3.text}")

    r4 = requests.post(f'{API_BASE}/operations/{operation_id}/leave', headers=headers, timeout=10)
    if r4.status_code in (200, 204):
        print("[ok] Leave OK")
    else:
        print(f"❌ Error leave: {r4.status_code} {r4.text}")

    r5 = requests.get(f'{API_BASE}/operations/{operation_id}/is-registered', headers=headers, timeout=10)
    if r5.status_code == 200:
        print(f"ℹ️  is-registered final: {r5.json().get('registered')}")
    else:
        print(f"❌ Error is-registered final: {r5.status_code} {r5.text}")

def test_health():
    """Verificar salud del backend"""
    print("[health] Verificando salud del backend...")
    try:
        response = requests.get(f'{API_BASE}/health', timeout=5)
        if response.status_code == 200:
            print("[ok] Backend está funcionando correctamente")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo conectar al backend: {e}")
        return False

def main():
    print("=" * 50)
    print("TEST DEL SISTEMA DEATH SQUAD AIRSOFT")
    print("=" * 50)
    print()
    
    # 1. Verificar backend
    if not test_health():
        print("\n⚠️  Asegúrate de que el backend esté corriendo en http://localhost:5000")
        return
    
    # 2. Login admin
    admin_token, admin_user = login('admin@dsairsofteam.local', 'Admin123!', label='admin')
    if not admin_token:
        return

    # 2b. Login / registro usuario normal
    user_token, user = ensure_test_user('test@test.com', 'test123')
    if not user_token:
        return
    
    # 3. Crear operación de ejemplo
    operation = test_create_operation(admin_token)
    if operation and operation.get('id'):
        test_registration_flow(str(operation['id']), user_token)
    
    # 4. Listar operaciones
    operations = test_get_operations()
    
    print()
    print("=" * 50)
    print("PRUEBAS COMPLETADAS")
    print("=" * 50)
    print()
    print("Ahora puedes abrir:")
    print("   Frontend: http://localhost:8000")
    print("   Admin:    http://localhost:8000/admin-operaciones.html")
    print()

if __name__ == '__main__':
    main()
