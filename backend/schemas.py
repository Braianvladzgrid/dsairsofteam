from marshmallow import Schema, fields, validate, ValidationError
import bleach

ALLOWED_TAGS = []
ALLOWED_ATTRS = {}

class UserRegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    user_type = fields.String(validate=validate.OneOf(['buyer', 'seller', 'agent']))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=2, max=255))
    phone = fields.String(validate=validate.Length(max=20))
    address = fields.String(validate=validate.Length(max=255))
    city = fields.String(validate=validate.Length(max=100))
    state = fields.String(validate=validate.Length(max=100))
    zipcode = fields.String(validate=validate.Length(max=20))

class PropertySchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=3, max=255))
    description = fields.String(validate=validate.Length(max=5000))
    type = fields.String(required=True, validate=validate.OneOf(['house', 'apartment', 'land', 'commercial']))
    price = fields.Decimal(required=True, places=2)
    bedrooms = fields.Integer()
    bathrooms = fields.Integer()
    area = fields.Decimal(places=2)
    address = fields.String(required=True, validate=validate.Length(max=255))
    city = fields.String(required=True, validate=validate.Length(max=100))
    state = fields.String(validate=validate.Length(max=100))
    zipcode = fields.String(validate=validate.Length(max=20))
    latitude = fields.Decimal(places=8)
    longitude = fields.Decimal(places=8)
    operation_type = fields.String(required=True, validate=validate.OneOf(['rent', 'sell']))
    status = fields.String(validate=validate.OneOf(['available', 'sold', 'rented', 'pending']))
    images = fields.List(fields.String())

class OperationSchema(Schema):
    property_id = fields.String(required=True)
    seller_id = fields.String(required=True)
    buyer_id = fields.String()
    type = fields.String(required=True, validate=validate.OneOf(['rent', 'sell']))
    price = fields.Decimal(required=True, places=2)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    status = fields.String(validate=validate.OneOf(['pending', 'in-progress', 'completed', 'cancelled']))
    notes = fields.String(validate=validate.Length(max=5000))

class OperationUpdateSchema(Schema):
    status = fields.String(validate=validate.OneOf(['pending', 'in-progress', 'completed', 'cancelled']))
    notes = fields.String(validate=validate.Length(max=5000))

def sanitize_string(value):
    """Sanitizar string contra XSS"""
    if not isinstance(value, str):
        return value
    return bleach.clean(value, tags=ALLOWED_TAGS, strip=True)

def sanitize_input(data, schema_class):
    """Validar y sanitizar datos de entrada"""
    schema = schema_class()
    try:
        validated_data = schema.load(data)
        # Sanitizar strings
        for key, value in validated_data.items():
            if isinstance(value, str):
                validated_data[key] = sanitize_string(value)
        return validated_data, None
    except ValidationError as err:
        return None, err.messages
