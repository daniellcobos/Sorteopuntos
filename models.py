from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db= SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
  
 
class puntosModel(db.Model):
    __tablename__ = 'Puntos'

    manzana = db.Column(db.String, primary_key=True)
    ciudad = db.Column(db.String())
    personas = db.Column(db.String())
    latitud = db.Column(db.Numeric())
    longitud = db.Column(db.Numeric())
    bajo = db.Column(db.Integer())
    medio = db.Column(db.Integer())
    alto = db.Column(db.Integer())

    def __init__(self,manzana, ciudad, personas):
        self.manzana = manzana
        self.ciudad = ciudad
        self.personas = personas