# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from enum import Enum


db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))



class DetailKo(db.Model):
    __tablename__ = 'detail_kos'

    id = db.Column(db.Integer, primary_key=True)
    id_pengelola_kos = db.Column(db.ForeignKey('user.id'))
    kos_name = db.Column(db.String(100))
    kos_type = db.Column(db.String(20))
    room_size = db.Column(db.String(20))    
    price = db.Column(db.Integer)
    address = db.Column(db.String(200))
    shared_facilities = db.Column(db.String(200))
    room_facilities = db.Column(db.String(200))
    available_room = db.Column(db.Integer)

    user = db.relationship('User', primaryjoin='DetailKo.id_pengelola_kos == User.id', backref='detail_koes')



class Gallery(db.Model):
    __tablename__ = 'gallery'

    id = db.Column(db.Integer, primary_key=True)
    id_kos = db.Column(db.ForeignKey('detail_kos.id'))
    foto_url = db.Column(db.String(200))

    detail_ko = db.relationship('DetailKo', primaryjoin='Gallery.id_kos == DetailKo.id', backref='galleries')



class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    id_pengunjung = db.Column(db.ForeignKey('user.id'))
    id_kos = db.Column(db.ForeignKey('detail_kos.id'))
    review = db.Column(db.String(500))

    user = db.relationship('User', primaryjoin='Review.id_pengunjung == User.id', backref='reviews')
    detail_ko = db.relationship('DetailKo', primaryjoin='Review.id_kos == DetailKo.id', backref='reviews')





class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(50))
    profile_picture = db.Column(db.String(100))

