from flask import Blueprint, request, jsonify
from models import Operation, Participation, User, db
from routes.auth import token_required, admin_required
from schemas import sanitize_input
from datetime import datetime
from uuid import uuid4
import bleach
import base64

operations_bp = Blueprint('operations', __name__, url_prefix='/api/operations')


def _clean_text(value):
    if value is None:
        return None
    if not isinstance(value, str):
        return value
    return bleach.clean(value, tags=[], strip=True)


def _clean_list(value):
    if value is None:
        return []
    if not isinstance(value, list):
        return []
    cleaned = []
    for item in value:
        if isinstance(item, str):
            text = _clean_text(item).strip()
            if text:
                cleaned.append(text)
    return cleaned


def _validate_and_normalize_image(image_value: str, max_bytes: int = 2 * 1024 * 1024):
    """Valida imagen enviada como data URI (base64) y aplica límite de tamaño.

    - Permite URLs o strings vacíos sin validación de tamaño.
    - Para data URI: valida que sea image/* y que el binario decodificado sea <= max_bytes.
    """
    if not image_value or not isinstance(image_value, str):
        return image_value

    value = image_value.strip()
    if not value:
        return ''

    if not value.startswith('data:'):
        # URL u otro formato: no podemos validar tamaño aquí
        return value

    # data:[<mediatype>][;base64],<data>
    if ',' not in value:
        raise ValueError('Invalid data URI image format')

    header, b64data = value.split(',', 1)
    header_lower = header.lower()
    if not header_lower.startswith('data:image/'):
        raise ValueError('Only image data URIs are allowed')
    if ';base64' not in header_lower:
        raise ValueError('Image data URI must be base64 encoded')

    try:
        raw = base64.b64decode(b64data, validate=True)
    except Exception:
        raise ValueError('Invalid base64 image data')

    if len(raw) > max_bytes:
        raise ValueError(f'Image too large. Max size is {max_bytes} bytes')

    return value


@operations_bp.route('/active', methods=['GET'])
def get_active_operations():
    """Obtener operaciones airsoft activas (público)"""
    today = datetime.utcnow()
    
    operations = Operation.query.filter(
        Operation.is_active == True,
        Operation.start_date >= today
    ).order_by(Operation.start_date.asc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/past', methods=['GET'])
def get_past_operations():
    """Obtener operaciones pasadas (público)"""
    today = datetime.utcnow()
    
    operations = Operation.query.filter(
        Operation.start_date < today
    ).order_by(Operation.start_date.desc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('', methods=['GET'], strict_slashes=False)
def get_all_operations():
    """Obtener todas las operaciones (público) - sin autenticación"""
    operations = Operation.query.filter(
        Operation.is_active == True
    ).order_by(Operation.start_date.asc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/admin', methods=['GET'], strict_slashes=False)
@token_required
@admin_required
def get_all_operations_admin(current_user):
    """Obtener todas las operaciones (admin) - incluye activas e inactivas"""
    operations = Operation.query.order_by(Operation.start_date.asc()).all()
    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/<id>', methods=['GET'])
def get_operation(id):
    """Obtener detalles de una operación (público)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    return jsonify(operation.to_dict(include_participants=True)), 200


@operations_bp.route('', methods=['POST'], strict_slashes=False)
@token_required
@admin_required
def create_operation(current_user):
    """Crear una nueva operación airsoft (admin only)"""
    data = request.get_json()

    # Validar campos requeridos
    required_fields = ['type', 'title', 'start_date', 'price']
    missing = [f for f in required_fields if f not in data or not data[f]]
    if missing:
        return jsonify({'error': 'Missing required fields', 'details': missing}), 400

    # Validar tipo de operación
    valid_types = ['milsim', 'picado', 'especial', 'realista', 'historica', 'semi-milsim']
    if data.get('type') not in valid_types:
        return jsonify({'error': f'Invalid operation type. Must be one of {valid_types}'}), 400

    valid_statuses = ['active', 'completed', 'cancelled']
    if data.get('status') and data.get('status') not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400

    try:
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = None
        if data.get('end_date'):
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))

        image_value = data.get('image', '')
        if image_value:
            try:
                image_value = _validate_and_normalize_image(image_value)
            except ValueError as ve:
                msg = str(ve)
                return jsonify({'error': msg}), (413 if 'too large' in msg.lower() else 400)

        operation = Operation(
            id=str(uuid4()),
            type=data['type'],
            title=_clean_text(data.get('title', '')),
            description=_clean_text(data.get('description', '')),
            lore=_clean_text(data.get('lore', '')),
            requirements=_clean_list(data.get('requirements')),
            rules=_clean_list(data.get('rules')),
            price=float(data.get('price', 0)),
            start_date=start_date,
            end_date=end_date,
            location=_clean_text(data.get('location', '')),
            max_participants=data.get('max_participants'),
            status=data.get('status', 'active'),
            is_active=bool(data.get('is_active', True)),
            notes=_clean_text(data.get('notes', '')),
            image=image_value,
            created_by=current_user.id
        )

        db.session.add(operation)
        db.session.commit()

        return jsonify({
            'message': 'Operation created successfully',
            'operation': operation.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating operation: {str(e)}'}), 500


@operations_bp.route('/<id>', methods=['PUT'])
@token_required
@admin_required
def update_operation(current_user, id):
    """Actualizar una operación (admin only)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    data = request.get_json()

    # Actualizar campos
    if 'type' in data:
        valid_types = ['milsim', 'picado', 'especial', 'realista', 'historica', 'semi-milsim']
        if data['type'] not in valid_types:
            return jsonify({'error': f'Invalid operation type'}), 400
        operation.type = data['type']

    if 'title' in data:
        operation.title = _clean_text(data['title'])
    if 'description' in data:
        operation.description = _clean_text(data['description'])
    if 'lore' in data:
        operation.lore = _clean_text(data['lore'])
    if 'requirements' in data:
        operation.requirements = _clean_list(data['requirements'])
    if 'rules' in data:
        operation.rules = _clean_list(data['rules'])
    if 'price' in data:
        operation.price = float(data['price'])
    if 'location' in data:
        operation.location = _clean_text(data['location'])
    if 'max_participants' in data:
        operation.max_participants = data['max_participants']
    if 'status' in data:
        valid_statuses = ['active', 'completed', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of {valid_statuses}'}), 400
        operation.status = data['status']
    if 'is_active' in data:
        operation.is_active = data['is_active']
    if 'notes' in data:
        operation.notes = _clean_text(data['notes'])
    if 'image' in data:
        try:
            operation.image = _validate_and_normalize_image(data['image'])
        except ValueError as ve:
            msg = str(ve)
            return jsonify({'error': msg}), (413 if 'too large' in msg.lower() else 400)
    if 'start_date' in data:
        operation.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
    if 'end_date' in data:
        operation.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))

    operation.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        return jsonify({
            'message': 'Operation updated successfully',
            'operation': operation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating operation: {str(e)}'}), 500


@operations_bp.route('/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_operation(current_user, id):
    """Eliminar una operación (admin only)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    try:
        db.session.delete(operation)
        db.session.commit()
        return jsonify({'message': 'Operation deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting operation: {str(e)}'}), 500


# ENDPOINTS DE PARTICIPACIÓN (REGISTRO)

@operations_bp.route('/<operation_id>/join', methods=['POST'])
@token_required
def join_operation(current_user, operation_id):
    """Registrarse en una operación (solo usuarios logeados)"""
    operation = Operation.query.get(operation_id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    if not operation.is_active:
        return jsonify({'error': 'Operation is not active'}), 400

    # Verificar si el usuario ya está registrado
    existing = Participation.query.filter_by(
        user_id=current_user.id,
        operation_id=operation_id
    ).first()

    if existing:
        return jsonify({
            'error': 'Ya estás registrado en esta operación',
            'message': 'Already registered in this operation',
            'participation': existing.to_dict()
        }), 409

    data = request.get_json(silent=True) or {}
    if not data.get('accept_rules') or not data.get('accept_requirements'):
        return jsonify({'error': 'You must accept rules and requirements'}), 400

    # Verificar límite de participantes
    if operation.max_participants:
        current_count = Participation.query.filter_by(operation_id=operation_id).count()
        if current_count >= operation.max_participants:
            return jsonify({'error': 'Operation is full'}), 400

    try:
        participation = Participation(
            id=str(uuid4()),
            user_id=current_user.id,
            operation_id=operation_id,
            status='pending',
            joined_at=datetime.utcnow()
        )

        db.session.add(participation)
        db.session.commit()

        return jsonify({
            'message': 'Successfully registered for the operation',
            'participation': participation.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error registering: {str(e)}'}), 500


@operations_bp.route('/<operation_id>/leave', methods=['POST'])
@token_required
def leave_operation(current_user, operation_id):
    """Cancelar registro en una operación"""
    participation = Participation.query.filter_by(
        user_id=current_user.id,
        operation_id=operation_id
    ).first()

    if not participation:
        return jsonify({'error': 'Not registered in this operation'}), 404

    try:
        db.session.delete(participation)
        db.session.commit()

        return jsonify({'message': 'Successfully unregistered from the operation'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error unregistering: {str(e)}'}), 500


@operations_bp.route('/<operation_id>/participants', methods=['GET'])
def get_operation_participants(operation_id):
    """Obtener participantes de una operación (público)"""
    operation = Operation.query.get(operation_id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    participants = Participation.query.filter_by(operation_id=operation_id).all()

    return jsonify([p.to_dict() for p in participants]), 200


@operations_bp.route('/<operation_id>/is-registered', methods=['GET'])
@token_required
def is_user_registered(current_user, operation_id):
    """Verificar si el usuario está registrado en una operación"""
    participation = Participation.query.filter_by(
        user_id=current_user.id,
        operation_id=operation_id
    ).first()

    return jsonify({'is_registered': participation is not None}), 200


@operations_bp.route('/<operation_id>/participants/<participation_id>/attendance', methods=['PATCH'])
@token_required
@admin_required
def update_attendance(current_user, operation_id, participation_id):
    """Actualizar asistencia de un participante (admin only)"""
    participation = Participation.query.get(participation_id)

    if not participation:
        return jsonify({'error': 'Participation not found'}), 404

    if participation.operation_id != operation_id:
        return jsonify({'error': 'Participation does not belong to this operation'}), 400

    data = request.get_json(silent=True) or {}
    new_status = data.get('status')

    # Nuevos estados: pending (neutro), attended, absent.
    # Compatibilidad: registered -> pending, cancelled -> absent.
    allowed = ['pending', 'attended', 'absent', 'registered', 'cancelled']
    if new_status not in allowed:
        return jsonify({'error': 'Invalid status. Must be: pending, attended, or absent'}), 400

    if new_status == 'registered':
        new_status = 'pending'
    elif new_status == 'cancelled':
        new_status = 'absent'

    try:
        participation.status = new_status
        db.session.commit()

        return jsonify({
            'message': 'Attendance updated successfully',
            'participation': participation.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating attendance: {str(e)}'}), 500

