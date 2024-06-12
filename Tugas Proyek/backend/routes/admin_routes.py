from flask import request, jsonify
from . import bp
from models import db, Admin
from serializers import Serializer

@bp.route('/api/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([Serializer.serialize_admin(admin) for admin in admins])

@bp.route('/api/admins/<int:id>', methods=['GET'])
def get_admin(id):
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    return jsonify(Serializer.serialize_admin(admin))

@bp.route('/api/admins', methods=['POST'])
def create_admin():
    data = request.get_json()
    admin = Admin(**data)
    db.session.add(admin)
    db.session.commit()
    return jsonify(Serializer.serialize_admin(admin)), 201

@bp.route('/api/admins/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    for key, value in data.items():
        setattr(admin, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_admin(admin))

@bp.route('/api/admins/<int:id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get(id)
    if admin is None:
        return jsonify({'message': 'Admin not found'}), 404
    db.session.delete(admin)
    db.session.commit()
    return jsonify({'message': 'Admin deleted'}), 200
