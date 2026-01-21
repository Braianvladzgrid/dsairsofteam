from flask import Blueprint, request, jsonify
from models import Operation, db
from routes.auth import token_required, admin_required
from schemas import sanitize_input, OperationSchema, OperationUpdateSchema
from sqlalchemy import or_
from datetime import datetime

operations_bp = Blueprint('operations', __name__, url_prefix='/api/operations')


@operations_bp.route('/active', methods=['GET'])
def get_active_operations():
    """Obtener operaciones activas (hasta la fecha actual)"""
    today = datetime.utcnow().date()
    
    operations = Operation.query.filter(
        Operation.is_active == True,
        Operation.start_date <= datetime.combine(today, datetime.max.time())
    ).order_by(Operation.start_date.desc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/past', methods=['GET'])
def get_past_operations():
    """Obtener operaciones pasadas (fechas anteriores)"""
    today = datetime.utcnow().date()
    
    operations = Operation.query.filter(
        Operation.start_date < datetime.combine(today, datetime.min.time())
    ).order_by(Operation.start_date.desc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/', methods=['GET'])
@token_required
def get_operations(current_user):
    """Obtener operaciones del usuario (o todas si es admin)"""
    filter_type = request.args.get('filter', 'all')  # all, active, past
    today = datetime.utcnow().date()

    base_query = Operation.query

    # Filtrar por tipo
    if filter_type == 'active':
        base_query = base_query.filter(
            Operation.is_active == True,
            Operation.start_date <= datetime.combine(today, datetime.max.time())
        )
    elif filter_type == 'past':
        base_query = base_query.filter(
            Operation.start_date < datetime.combine(today, datetime.min.time())
        )

    # Filtrar por usuario si no es admin
    if current_user.is_admin:
        operations = base_query.order_by(Operation.start_date.desc()).all()
    else:
        operations = base_query.filter(
            or_(
                Operation.buyer_id == current_user.id,
                Operation.seller_id == current_user.id
            )
        ).order_by(Operation.start_date.desc()).all()

    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/<id>', methods=['GET'])
@token_required
def get_operation(current_user, id):
    """Obtener detalles de una operación"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    if not current_user.is_admin and operation.buyer_id != current_user.id and operation.seller_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    return jsonify(operation.to_dict()), 200


@operations_bp.route('/', methods=['POST'])
@token_required
def create_operation(current_user):
    """Crear una operación (usuario normal) o para otros (admin)"""
    data = request.get_json()
    
    # Validar y sanitizar
    validated_data, errors = sanitize_input(data, OperationSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    # Si no es admin, el buyer_id debe ser el usuario actual
    if not current_user.is_admin:
        validated_data['buyer_id'] = current_user.id

    # start_date es requerido
    if not validated_data.get('start_date'):
        return jsonify({'error': 'start_date es requerido'}), 400

    operation = Operation(
        property_id=validated_data['property_id'],
        buyer_id=validated_data['buyer_id'],
        seller_id=validated_data['seller_id'],
        type=validated_data['type'],
        price=validated_data['price'],
        start_date=validated_data['start_date'],
        end_date=validated_data.get('end_date'),
        notes=validated_data.get('notes'),
        status='pending',
        is_active=True
    )

    db.session.add(operation)
    db.session.commit()

    return jsonify(operation.to_dict()), 201


@operations_bp.route('/<id>', methods=['PATCH'])
@token_required
def update_operation(current_user, id):
    """Actualizar una operación"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    # Solo admin o los involucrados pueden actualizar
    if not current_user.is_admin and operation.buyer_id != current_user.id and operation.seller_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    data = request.get_json()
    
    # Validar y sanitizar
    validated_data, errors = sanitize_input(data, OperationUpdateSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    if 'status' in validated_data:
        operation.status = validated_data['status']
    if 'notes' in validated_data:
        operation.notes = validated_data['notes']

    db.session.commit()

    return jsonify(operation.to_dict()), 200


@operations_bp.route('/<id>/toggle-active', methods=['PATCH'])
@token_required
@admin_required
def toggle_operation_active(current_user, id):
    """Activar/Desactivar una operación (solo admin)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    operation.is_active = not operation.is_active
    db.session.commit()

    return jsonify({
        'message': f"Operación {'activada' if operation.is_active else 'desactivada'}",
        'operation': operation.to_dict()
    }), 200


@operations_bp.route('/<id>', methods=['DELETE'])
@token_required
@admin_required
def delete_operation(current_user, id):
    """Eliminar una operación (solo admin)"""
    operation = Operation.query.get(id)

    if not operation:
        return jsonify({'error': 'Operation not found'}), 404

    db.session.delete(operation)
    db.session.commit()

    return jsonify({'message': 'Operation deleted'}), 200


@operations_bp.route('/admin/all', methods=['GET'])
@token_required
@admin_required
def get_all_operations(current_user):
    """Obtener TODAS las operaciones (solo admin)"""
    filter_type = request.args.get('filter', 'all')  # all, active, past
    today = datetime.utcnow().date()

    query = Operation.query

    if filter_type == 'active':
        query = query.filter(
            Operation.is_active == True,
            Operation.start_date <= datetime.combine(today, datetime.max.time())
        )
    elif filter_type == 'past':
        query = query.filter(
            Operation.start_date < datetime.combine(today, datetime.min.time())
        )

    operations = query.order_by(Operation.start_date.desc()).all()
    return jsonify([o.to_dict() for o in operations]), 200


@operations_bp.route('/admin/stats', methods=['GET'])
@token_required
@admin_required
def get_operations_stats(current_user):
    """Obtener estadísticas de operaciones (solo admin)"""
    today = datetime.utcnow().date()
    
    total = Operation.query.count()
    active = Operation.query.filter(Operation.is_active == True).count()
    inactive = Operation.query.filter(Operation.is_active == False).count()
    
    by_status = {
        'pending': Operation.query.filter_by(status='pending').count(),
        'in-progress': Operation.query.filter_by(status='in-progress').count(),
        'completed': Operation.query.filter_by(status='completed').count(),
        'cancelled': Operation.query.filter_by(status='cancelled').count(),
    }
    
    return jsonify({
        'total': total,
        'active': active,
        'inactive': inactive,
        'by_status': by_status
    }), 200

