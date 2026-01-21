from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import User, db
from config import config
from schemas import sanitize_input, UserRegisterSchema, UserLoginSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
cfg = config['default']

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, cfg.JWT_SECRET, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validar y sanitizar
    validated_data, errors = sanitize_input(data, UserRegisterSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    if User.query.filter_by(email=validated_data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        name=validated_data['name'],
        email=validated_data['email'],
        password=generate_password_hash(validated_data['password']),
        user_type=validated_data.get('user_type', 'buyer'),
        is_admin=False
    )

    db.session.add(user)
    db.session.commit()

    token = jwt.encode(
        {
            'user_id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,
            'exp': datetime.utcnow() + timedelta(seconds=cfg.JWT_EXPIRE)
        },
        cfg.JWT_SECRET,
        algorithm='HS256'
    )

    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validar y sanitizar
    validated_data, errors = sanitize_input(data, UserLoginSchema)
    if errors:
        return jsonify({'error': 'Validation error', 'details': errors}), 400

    user = User.query.filter_by(email=validated_data['email']).first()

    if not user or not check_password_hash(user.password, validated_data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = jwt.encode(
        {
            'user_id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,
            'exp': datetime.utcnow() + timedelta(seconds=cfg.JWT_EXPIRE)
        },
        cfg.JWT_SECRET,
        algorithm='HS256'
    )

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify(current_user.to_dict()), 200

