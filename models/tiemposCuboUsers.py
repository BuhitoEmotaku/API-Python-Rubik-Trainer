from utils.db import db
from sqlalchemy import Column, Integer, String, UniqueConstraint,Index
from sqlalchemy.exc import IntegrityError
from models.usuario import User
import json
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Clase TiempoCuboUser
class TiemposCuboUser(db.Model):

    __tablename__ = 'tiemposCuboUser'

    idTiempo = db.Column(db.Integer, primary_key=True)
    idUsu = db.Column(db.Integer, db.ForeignKey('users.idUsu'))
    tiempo = db.Column(db.String(255))
    mezcla = db.Column(db.String(255))
    tiempoMilisegundos = db.Column(db.Integer)
    # Relacion con User
    usuario = db.relationship('User', back_populates='tiempos_cubo')

    # __table_args__ = (
    #     UniqueConstraint('cubeState', 'idUsu', name='_mezcla_uc'),
    # )
    #Creamos el obejto inicial
    def __init__(
        self,
        data,userData
    ):
        self.idTiempo = None
        self.idUsu = userData['idUsu'],
        self.tiempo = data['tiempo'],
        self.mezcla = data['mezcla'],
        self.tiempoMilisegundos = data['tiempoMilisegundos']

    # Metodo dict para crear el objeto con sus datos
    def to_dict(self):
        return {
            'idTiempo': self.idTiempo,
            'idUsu': self.idUsu,
            'tiempo': self.tiempo,
            'mezcla': self.mezcla,
            'tiempoMilisegundos': self.tiempoMilisegundos
        }
            