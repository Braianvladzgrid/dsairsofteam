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
    created_operations = db.relationship(
        'Operation',
        back_populates='creator',
        lazy=True,
        foreign_keys='Operation.created_by'
    )

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
    type = db.Column(db.String(50), nullable=False)  # milsim, picado, especial, realista, historica, semi-milsim
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    lore = db.Column(db.Text)
    requirements = db.Column(db.JSON, default=list)
    rules = db.Column(db.JSON, default=list)
    price = db.Column(db.Numeric(15, 2), nullable=False, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    max_participants = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    image = db.Column(db.Text)  # Base64 encoded image
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship(
        'User',
        back_populates='created_operations',
        foreign_keys=[created_by]
    )
    participations = db.relationship('Participation', backref='operation', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_participants=False):
        data = {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'lore': self.lore,
            'requirements': self.requirements or [],
            'rules': self.rules or [],
            'price': float(self.price),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'max_participants': self.max_participants,
            'status': self.status,
            'is_active': self.is_active,
            'notes': self.notes,
            'image': self.image,
            'created_by': self.created_by,
            'participant_count': len(self.participations),
            'created_at': self.created_at.isoformat(),
        }
        if include_participants:
            data['participants'] = [p.to_dict() for p in self.participations]
        return data


class Participation(db.Model):
    __tablename__ = 'participations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    operation_id = db.Column(db.String(36), db.ForeignKey('operations.id'), nullable=False)
    # Estado de asistencia (admin): pending (neutro), attended, absent.
    # Compatibilidad histórica: 'registered' -> pending, 'cancelled' -> absent.
    status = db.Column(db.String(20), default='pending')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='user_participations')

    def to_dict(self):
        status = self.status
        if status == 'registered':
            status = 'pending'
        elif status == 'cancelled':
            status = 'absent'
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'user_email': self.user.email,
            'operation_id': self.operation_id,
            'status': status,
            'joined_at': self.joined_at.isoformat(),
        }


class AdminNote(db.Model):
    __tablename__ = 'admin_notes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Usuario sobre el que se escribe la nota
    admin_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Admin que escribe la nota
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id], backref='notes_about_user')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='notes_by_admin')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin_id': self.admin_id,
            'admin_name': self.admin.name,
            'note': self.note,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
