#!/usr/bin/env python3
"""
Script para inicializar la base de datos e crear un usuario admin
"""

from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash


def _ensure_operation_columns():
    """Migración liviana para SQLite sin Alembic."""
    try:
        result = db.session.execute(db.text("PRAGMA table_info(operations)"))
        existing_cols = {row[1] for row in result.fetchall()}

        desired = {
            'lore': "ALTER TABLE operations ADD COLUMN lore TEXT",
            'requirements': "ALTER TABLE operations ADD COLUMN requirements JSON",
            'rules': "ALTER TABLE operations ADD COLUMN rules JSON",
        }

        for col, ddl in desired.items():
            if col not in existing_cols:
                db.session.execute(db.text(ddl))
        db.session.commit()
    except Exception:
        db.session.rollback()
        # Si falla (p.ej. DB distinta), no rompemos init.
        pass

def init_db():
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        _ensure_operation_columns()
        print("✓ Tablas de base de datos creadas")
        
        # Verificar si existe admin
        admin = User.query.filter_by(email='admin@dsairsofteam.local').first()
        
        if not admin:
            # Crear usuario admin
            admin = User(
                name='Admin',
                email='admin@dsairsofteam.local',
                password=generate_password_hash('Admin123!'),
                user_type='agent',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Usuario admin creado")
            print(f"  Email: admin@dsairsofteam.local")
            print(f"  Contraseña: Admin123!")
            print(f"  ⚠️  Cambia la contraseña en producción!")
        else:
            print("✓ Usuario admin ya existe")

if __name__ == '__main__':
    init_db()
