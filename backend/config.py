import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQLite para desarrollo local, puede cambiar a PostgreSQL en producción
    _raw_database_url = os.getenv('DATABASE_URL', 'sqlite:///dsairsofteam.db')
    # Algunos proveedores (Render/Heroku) usan el esquema legacy `postgres://`
    # SQLAlchemy espera `postgresql://`
    if _raw_database_url.startswith('postgres://'):
        _raw_database_url = _raw_database_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = _raw_database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ayuda a evitar conexiones stale en DBs hosteadas
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', '300')),
    }
    JWT_SECRET = os.getenv('JWT_SECRET', 'tu_super_secret_key_aqui_cambiar_en_produccion')
    JWT_EXPIRE = int(os.getenv('JWT_EXPIRE', 604800))  # 7 days

    # Límite de payload (protege de uploads/base64 gigantes)
    # 2MB binario en base64 ≈ 2.7MB + JSON overhead; dejamos margen.
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5MB

    # Evitar revelar detalles innecesarios
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
