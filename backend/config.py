import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQLite para desarrollo local, puede cambiar a PostgreSQL en producción
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///dsairsofteam.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
