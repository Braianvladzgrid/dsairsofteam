from flask import Blueprint, request, jsonify
from models import User, db
from routes.auth import token_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200


@users_bp.route('/<id>', methods=['PATCH'])
@token_required
def update_user(current_user, id):
    if id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403

    user = User.query.get(id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Don't allow email changes via this endpoint
    data.pop('email', None)
    data.pop('password', None)

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()

    return jsonify({
        'message': 'Profile updated',
        'user': user.to_dict()
    }), 200
