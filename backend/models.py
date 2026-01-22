from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    photo = db.Column(db.Text)  # Base64 encoded image
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    user_type = db.Column(db.String(20), default='buyer')  # buyer, seller, agent
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    properties = db.relationship('Property', backref='owner', lazy=True, foreign_keys='Property.user_id')
    operations_as_buyer = db.relationship('Operation', foreign_keys='Operation.buyer_id', backref='buyer')
    operations_as_seller = db.relationship('Operation', foreign_keys='Operation.seller_id', backref='seller')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'photo': self.photo,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'user_type': self.user_type,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
        }


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50), nullable=False)  # house, apartment, land, commercial
    price = db.Column(db.Numeric(15, 2), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Numeric(10, 2))
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    operation_type = db.Column(db.String(20), nullable=False)  # rent, sell
    status = db.Column(db.String(20), default='available')  # available, sold, rented, pending
    images = db.Column(db.JSON, default=[])
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'price': float(self.price),
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': float(self.area) if self.area else None,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'operation_type': self.operation_type,
            'status': self.status,
            'images': self.images,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
        }


class Operation(db.Model):
    __tablename__ = 'operations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    property_id = db.Column(db.String(36), db.ForeignKey('properties.id'), nullable=False)
    buyer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # rent, sell
    price = db.Column(db.Numeric(15, 2), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, in-progress, completed, cancelled
    is_active = db.Column(db.Boolean, default=True)  # Activa o desactivada
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = db.relationship('Property', backref='operations')

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'type': self.type,
            'price': float(self.price),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'is_active': self.is_active,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
        }
