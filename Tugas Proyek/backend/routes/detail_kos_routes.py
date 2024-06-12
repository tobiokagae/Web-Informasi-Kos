from flask import request, jsonify
from . import bp
from models import db, DetailKo, User
from serializers import Serializer

@bp.route('/api/detail_kos', methods=['GET'])
def get_detail_kos():
    kos_list = DetailKo.query.all()
    return jsonify([Serializer.serialize_detail_kos(kos) for kos in kos_list])

@bp.route('/api/detail_kos/<int:id>', methods=['GET'])
def get_kos(id):
    kos = DetailKo.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404
    return jsonify(Serializer.serialize_detail_kos(kos))

@bp.route('/api/detail_kos', methods=['POST'])
def create_kos():
    data = request.get_json()

    # Memastikan data yang diterima tidak kosong
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Memeriksa apakah pengguna yang membuat permintaan adalah pengelola kos
    user_id = data.get('user_id')  # Ambil user_id dari JSON request
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404


    # Membuat DetailKo jika pengguna adalah pengelola kos
    kos_data = {
        'id_pengelola_kos': user_id,
        'kos_name': data.get('kos_name'),
        'kos_type': data.get('kos_type'),
        'room_size': data.get('room_size'),
        'price': data.get('price'),
        'address': data.get('address'),
        'shared_facilities': data.get('shared_facilities'),
        'room_facilities': data.get('room_facilities'),
        'available_room': data.get('available_room')
    }
    kos = DetailKo(**kos_data)
    db.session.add(kos)
    db.session.commit()
    return jsonify(Serializer.serialize_detail_kos(kos)), 201

@bp.route('/api/detail_kos/<int:id>', methods=['PUT'])
def update_kos(id):
    data = request.get_json()
    kos = DetailKo.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404
    for key, value in data.items():
        setattr(kos, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_detail_kos(kos))

@bp.route('/api/detail_kos/<int:id>', methods=['DELETE'])
def delete_kos(id):
    kos = DetailKo.query.get(id)
    if kos is None:
        return jsonify({'message': 'Kos not found'}), 404
    db.session.delete(kos)
    db.session.commit()
    return jsonify({'message': 'Kos deleted'}), 200
