from flask import request, jsonify
from . import bp
from models import db, Review, User
from serializers import Serializer

@bp.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([Serializer.serialize_review(review) for review in reviews])

@bp.route('/api/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    return jsonify(Serializer.serialize_review(review))

@bp.route('/api/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    
    # Memastikan data yang diterima tidak kosong
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Memeriksa apakah user_id ada dalam data
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400

    # Memeriksa apakah pengguna dengan user_id tersebut ada dan memiliki role PENGUNJUNG
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found or does not have PENGUNJUNG role'}), 404

    # Membuat ulasan jika pengguna memiliki peran yang sesuai
    review_data = {
        'id_pengunjung': user_id,
        'id_kos': data.get('id_kos'),
        'review': data.get('review')
    }
    review = Review(**review_data)
    db.session.add(review)
    db.session.commit()
    return jsonify(Serializer.serialize_review(review)), 201


@bp.route('/api/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    data = request.get_json()
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(Serializer.serialize_review(review))

@bp.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if review is None:
        return jsonify({'message': 'Review not found'}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'}), 200
