from flask import Blueprint, request, jsonify
from models import Property, db
from routes.auth import token_required
from schemas import sanitize_input, PropertySchema
from sqlalchemy import or_

properties_bp = Blueprint('properties', __name__, url_prefix='/api/properties')


@properties_bp.route('/', methods=['GET'])
def get_properties():
    operation_type = request.args.get('operationType')
    city = request.args.get('city')
    prop_type = request.args.get('type')

    query = Property.query

    if operation_type:
        query = query.filter_by(operation_type=operation_type)
    if city:
        query = query.filter_by(city=city)
    if prop_type:
        query = query.filter_by(type=prop_type)

    properties = query.order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict() for p in properties]), 200


@properties_bp.route('/<id>', methods=['GET'])
def get_property(id):
    property = Property.query.get(id)

    if not property:
        return jsonify({'error': 'Property not found'}), 404

    return jsonify(property.to_dict()), 200


@properties_bp.route('/', methods=['POST'])
@token_required
def create_property(current_user):
    data = request.get_json()
    
    # Validar y sanitizar
    validated_data, errors = sanitize_input(data, PropertySchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    property = Property(
        title=validated_data['title'],
        description=validated_data.get('description'),
        type=validated_data['type'],
        price=validated_data['price'],
        bedrooms=validated_data.get('bedrooms'),
        bathrooms=validated_data.get('bathrooms'),
        area=validated_data.get('area'),
        address=validated_data.get('address'),
        city=validated_data.get('city'),
        state=validated_data.get('state'),
        zipcode=validated_data.get('zipcode'),
        latitude=validated_data.get('latitude'),
        longitude=validated_data.get('longitude'),
        operation_type=validated_data['operation_type'],
        status=validated_data.get('status', 'available'),
        images=validated_data.get('images', []),
        user_id=current_user.id
    )

    db.session.add(property)
    db.session.commit()

    return jsonify(property.to_dict()), 201


@properties_bp.route('/<id>', methods=['PATCH'])
@token_required
def update_property(current_user, id):
    property = Property.query.get(id)

    if not property:
        return jsonify({'error': 'Property not found'}), 404

    if property.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    data = request.get_json()
    
    # Validar y sanitizar (permitir campos parciales)
    validated_data, errors = sanitize_input(data, PropertySchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    for key, value in validated_data.items():
        if hasattr(property, key):
            setattr(property, key, value)

    db.session.commit()
    return jsonify(property.to_dict()), 200


@properties_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_property(current_user, id):
    property = Property.query.get(id)

    if not property:
        return jsonify({'error': 'Property not found'}), 404

    if property.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    db.session.delete(property)
    db.session.commit()

    return jsonify({'message': 'Property deleted'}), 200
