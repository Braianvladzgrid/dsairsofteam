"""
Script para insertar datos de prueba (propiedades) en la base de datos
"""
from models import db, Property, User
from app import create_app

def insert_sample_data():
    app = create_app()
    
    with app.app_context():
        # Verificar si ya hay propiedades
        if Property.query.count() > 0:
            print("Ya existen propiedades en la base de datos")
            print(f"Total: {Property.query.count()} propiedades")
            return
        
        print("Insertando datos de prueba...")
        
        # Obtener un usuario admin para asignar las propiedades
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            admin_user = User.query.first()
        
        if not admin_user:
            print("❌ No hay usuarios en la base de datos. Ejecuta init_db.py primero")
            return
        
        print(f"Usando usuario: {admin_user.email}")
        
        # Propiedades de ejemplo
        properties = [
            {
                "title": "Casa Moderna en Zona Norte",
                "description": "Hermosa casa de 3 dormitorios con jardín y piscina. Ideal para familias.",
                "type": "house",
                "operation_type": "sell",
                "price": 250000.00,
                "address": "Av. Principal 1234",
                "city": "Ciudad",
                "state": "Zona Norte",
                "bedrooms": 3,
                "bathrooms": 2,
                "area": 180.5,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1568605114967-8130f3a36994"]
            },
            {
                "title": "Departamento Centro",
                "description": "Departamento moderno de 2 ambientes en pleno centro. Listo para habitar.",
                "type": "apartment",
                "operation_type": "sell",
                "price": 150000.00,
                "address": "Calle Centro 567",
                "city": "Ciudad",
                "state": "Centro",
                "bedrooms": 2,
                "bathrooms": 1,
                "area": 65.0,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1545324418-cc1a3fa10c00"]
            },
            {
                "title": "Casa en Alquiler - Barrio Residencial",
                "description": "Amplia casa de 4 dormitorios en barrio tranquilo. Jardín y garage.",
                "type": "house",
                "operation_type": "rent",
                "price": 1500.00,
                "address": "Los Alamos 890",
                "city": "Ciudad",
                "state": "Barrio Los Alamos",
                "bedrooms": 4,
                "bathrooms": 3,
                "area": 220.0,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6"]
            },
            {
                "title": "Oficina Comercial",
                "description": "Oficina en edificio corporativo. 100m2, 2 baños, excelente ubicación.",
                "type": "commercial",
                "operation_type": "rent",
                "price": 2000.00,
                "address": "Distrito Financiero 456",
                "city": "Ciudad",
                "state": "Distrito Financiero",
                "bedrooms": 0,
                "bathrooms": 2,
                "area": 100.0,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1497366216548-37526070297c"]
            },
            {
                "title": "Terreno con Vista al Mar",
                "description": "Terreno de 500m2 con vista panorámica al mar. Ideal para inversión.",
                "type": "land",
                "operation_type": "sell",
                "price": 180000.00,
                "address": "Costa del Sol s/n",
                "city": "Costa",
                "state": "Costa del Sol",
                "bedrooms": 0,
                "bathrooms": 0,
                "area": 500.0,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1500382017468-9049fed747ef"]
            },
            {
                "title": "Loft Moderno",
                "description": "Loft tipo industrial totalmente renovado. 1 dormitorio, 1 baño.",
                "type": "apartment",
                "operation_type": "rent",
                "price": 1200.00,
                "address": "Barrio Palermo 234",
                "city": "Ciudad",
                "state": "Palermo",
                "bedrooms": 1,
                "bathrooms": 1,
                "area": 75.0,
                "user_id": admin_user.id,
                "images": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"]
            },
        ]
        
        # Agregar propiedades
        for prop_data in properties:
            prop = Property(**prop_data)
            db.session.add(prop)
        
        db.session.commit()
        
        print(f"✅ {len(properties)} propiedades insertadas exitosamente")
        print(f"📊 Total en base de datos: {Property.query.count()}")

if __name__ == '__main__':
    insert_sample_data()
