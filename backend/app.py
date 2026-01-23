from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from config import config
from routes.auth import auth_bp
from routes.properties import properties_bp
from routes.users import users_bp
from routes.operations import operations_bp
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    
    # Configurar CORS correctamente para todas las rutas
    CORS(app, 
         resources={r"/api/*": {
             "origins": ["http://localhost:8080", "http://localhost:8000", "http://localhost:5000", "http://127.0.0.1:8080", "http://127.0.0.1:8000", "http://127.0.0.1:5000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(operations_bp)

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'Backend running'}), 200

    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f'✅ Server running on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)
