from flask import Blueprint, request, jsonify
from models import Operation, Participation, User, db
from routes.auth import token_required, admin_required
from schemas import sanitize_input
from datetime import datetime
from uuid import uuid4

operations_bp = Blueprint('operations', __name__, url_prefix='/api/operations')


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


@operations_bp.route('/', methods=['GET'])
def get_all_operations():
    """Obtener todas las operaciones (público) - sin autenticación"""
    operations = Operation.query.filter(
        Operation.is_active == True
    ).order_by(Operation.start_date.asc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/<id>', methods=['GET'])
def get_operation(id):
    """Obtener detalles de una operación (público)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    return jsonify(operation.to_dict(include_participants=True)), 200


@operations_bp.route('/', methods=['POST'])
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

    try:
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        end_date = None
        if data.get('end_date'):
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))

        operation = Operation(
            id=str(uuid4()),
            type=data['type'],
            title=data.get('title', ''),
            description=data.get('description', ''),
            price=float(data.get('price', 0)),
            start_date=start_date,
            end_date=end_date,
            location=data.get('location', ''),
            max_participants=data.get('max_participants'),
            status=data.get('status', 'active'),
            is_active=True,
            notes=data.get('notes', ''),
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
        operation.title = data['title']
    if 'description' in data:
        operation.description = data['description']
    if 'price' in data:
        operation.price = float(data['price'])
    if 'location' in data:
        operation.location = data['location']
    if 'max_participants' in data:
        operation.max_participants = data['max_participants']
    if 'status' in data:
        operation.status = data['status']
    if 'is_active' in data:
        operation.is_active = data['is_active']
    if 'notes' in data:
        operation.notes = data['notes']
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
        return jsonify({'error': 'Already registered in this operation'}), 409

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
            status='registered',
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
