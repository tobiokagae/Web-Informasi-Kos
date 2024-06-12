from flask import request, jsonify
from . import bp
from models import db, Gallery, User
from serializers import Serializer

@bp.route('/api/galleries', methods=['GET'])
def get_galleries():
    galleries = Gallery.query.all()
    return jsonify([Serializer.serialize_gallery(gallery) for gallery in galleries])

@bp.route('/api/galleries/<int:id>', methods=['GET'])
def get_gallery(id):
    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404
    return jsonify(Serializer.serialize_gallery(gallery))

@bp.route('/api/galleries', methods=['POST'])
def create_gallery():
    data = request.get_json()
    
    # Memeriksa apakah user_id ada dalam data
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400

    # Memeriksa apakah pengguna dengan user_id tersebut ada
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404


    # Membuat galeri jika pengguna memiliki peran yang sesuai
    gallery_data = {
        'id_kos': data.get('id_kos'),
        'foto_url': data.get('foto_url')
    }
    gallery = Gallery(**gallery_data)
    db.session.add(gallery)
    db.session.commit()
    return jsonify(Serializer.serialize_gallery(gallery)), 201

@bp.route('/api/galleries/<int:id>', methods=['PUT'])
def update_gallery(id):
    data = request.get_json()
    
    # Memeriksa apakah user_id ada dalam data
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400

    # Memeriksa apakah pengguna dengan user_id tersebut ada
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404


    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404

    for key, value in data.items():
        setattr(gallery, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_gallery(gallery))

@bp.route('/api/galleries/<int:id>', methods=['DELETE'])
def delete_gallery(id):
    data = request.get_json()
    
    # Memeriksa apakah user_id ada dalam data
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400

    # Memeriksa apakah pengguna dengan user_id tersebut ada
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404


    gallery = Gallery.query.get(id)
    if gallery is None:
        return jsonify({'message': 'Gallery not found'}), 404
    
    db.session.delete(gallery)
    db.session.commit()
    return jsonify({'message': 'Gallery deleted'}), 200
