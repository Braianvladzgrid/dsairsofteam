from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import User, AdminNote, Participation, Operation, db
from routes.auth import token_required, admin_required
from datetime import datetime
from schemas import sanitize_input, sanitize_string, UserRegisterSchema, UserUpdateSchema

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
    data = request.get_json(silent=True) or {}

    validated_data, errors = sanitize_input(data, UserRegisterSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    # Verificar si el email ya existe
    if User.query.filter_by(email=validated_data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Crear nuevo usuario
    new_user = User(
        name=validated_data.get('name'),
        email=validated_data.get('email'),
        password=generate_password_hash(validated_data.get('password')),
        phone=validated_data.get('phone', ''),
        user_type=validated_data.get('user_type', 'buyer'),
        is_admin=bool(data.get('is_admin', False))
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

    data = request.get_json(silent=True) or {}

    # Validar + sanitizar solo campos permitidos (anti-mass-assignment)
    validated_data, errors = sanitize_input(data, UserUpdateSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    allowed_fields = {'name', 'phone', 'address', 'city', 'state', 'zipcode'}
    for key, value in validated_data.items():
        if key in allowed_fields:
            setattr(user, key, value)

    db.session.commit()

    return jsonify({
        'message': 'Profile updated',
        'user': user.to_dict()
    }), 200

@users_bp.route('/<id>/toggle-admin', methods=['POST'])
@token_required
@admin_required
def toggle_admin(current_user, id):
    """Otorgar o revocar permisos de admin a un usuario"""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Proteger al usuario admin que está modificando
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot change your own admin status'}), 400

    user.is_admin = not user.is_admin
    db.session.commit()

    return jsonify({
        'message': f'User is now {"admin" if user.is_admin else "regular user"}',
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


@users_bp.route('/<id>/stats', methods=['GET'])
@token_required
@admin_required
def get_user_stats(current_user, id):
    """Obtener estadísticas de participación de un usuario (solo admin)"""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Obtener todas las participaciones del usuario
    participations = Participation.query.filter_by(user_id=id).all()
    
    # Contar por estado
    total_registered = len(participations)
    total_attended = len([p for p in participations if p.status == 'attended'])
    # Compat: cancelled (legacy) cuenta como absent
    total_absent = len([p for p in participations if p.status in ('absent', 'cancelled')])
    total_pending = len([p for p in participations if p.status in ('pending', 'registered')])

    # Métricas globales (solo operaciones pasadas): participó vs no participó
    now = datetime.utcnow()
    total_past_operations = Operation.query.filter(Operation.start_date < now).count()
    past_attended = (
        Participation.query.join(Operation, Participation.operation_id == Operation.id)
        .filter(Participation.user_id == id, Operation.start_date < now, Participation.status == 'attended')
        .count()
    )
    past_not_participated = max(0, total_past_operations - past_attended)

    return jsonify({
        'user_id': id,
        'user_name': user.name,
        'total_registered': total_registered,
        'total_attended': total_attended,
        'total_pending': total_pending,
        'total_absent': total_absent,
        'past_operations_total': total_past_operations,
        'past_participated': past_attended,
        'past_not_participated': past_not_participated,
        'participation_rate': round((total_attended / total_registered * 100) if total_registered > 0 else 0, 2)
    }), 200


@users_bp.route('/<id>/admin-notes', methods=['GET'])
@token_required
@admin_required
def get_admin_notes(current_user, id):
    """Obtener notas privadas de admin sobre un usuario (solo admin)"""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    notes = AdminNote.query.filter_by(user_id=id).order_by(AdminNote.created_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes]), 200


@users_bp.route('/<id>/admin-notes', methods=['POST'])
@token_required
@admin_required
def create_admin_note(current_user, id):
    """Crear una nota privada de admin sobre un usuario (solo admin)"""
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json(silent=True) or {}
    
    if not data.get('note'):
        return jsonify({'error': 'Note text is required'}), 400

    note_text = sanitize_string(data.get('note'))

    if not note_text.strip():
        return jsonify({'error': 'Note text is required'}), 400

    note = AdminNote(
        user_id=id,
        admin_id=current_user.id,
        note=note_text
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        'message': 'Admin note created',
        'note': note.to_dict()
    }), 201


@users_bp.route('/<user_id>/admin-notes/<note_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_admin_note(current_user, user_id, note_id):
    """Eliminar una nota privada de admin (solo admin que la creó)"""
    note = AdminNote.query.get(note_id)

    if not note:
        return jsonify({'error': 'Note not found'}), 404

    if note.user_id != user_id:
        return jsonify({'error': 'Note does not belong to this user'}), 400

    # Solo el admin que creó la nota puede eliminarla (o cualquier admin)
    # if note.admin_id != current_user.id and not current_user.is_admin:
    #     return jsonify({'error': 'Not authorized'}), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Admin note deleted'}), 200