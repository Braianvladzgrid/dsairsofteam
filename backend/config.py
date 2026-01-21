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

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
