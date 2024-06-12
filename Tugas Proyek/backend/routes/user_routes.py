from models import db, User
from serializers import Serializer
from flask import request, jsonify
from . import bp

@bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([Serializer.serialize_user(user) for user in users])

@bp.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(Serializer.serialize_user(user))


@bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400


    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(Serializer.serialize_user(user)), 201

@bp.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404



    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_user(user))



@bp.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

