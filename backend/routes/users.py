from flask import Blueprint, request, jsonify
from models import User, db
from routes.auth import token_required, admin_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    """Obtener todos los usuarios (solo admin)"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route('', methods=['POST'])
@token_required
@admin_required
def create_user(current_user):
    """Crear un nuevo usuario (solo admin)"""
    data = request.get_json()

    # Validar datos requeridos
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'name, email, and password are required'}), 400

    # Verificar si el email ya existe
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Crear nuevo usuario
    new_user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        phone=data.get('phone', ''),
        user_type=data.get('user_type', 'buyer'),
        is_admin=data.get('is_admin', False)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user': new_user.to_dict()
    }), 201


@users_bp.route('/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200


@users_bp.route('/<id>', methods=['PATCH'])
@token_required
def update_user(current_user, id):
    """Actualizar perfil de usuario (propio o admin editando otros)"""
    # Permitir que admin edite cualquier usuario
    if id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Not authorized'}), 403

    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # No permitir cambios de email por este endpoint
    data.pop('email', None)
    # No permitir cambio de password por PATCH (se haría en endpoint separado)
    data.pop('password', None)
    # Solo admin puede cambiar is_admin
    if not current_user.is_admin:
        data.pop('is_admin', None)

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()

    return jsonify({
        'message': 'Profile updated',
        'user': user.to_dict()
    }), 200

@users_bp.route('/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(current_user, id):
    """Eliminar un usuario (solo admin)"""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Proteger al usuario admin que está eliminando
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot delete yourself'}), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200