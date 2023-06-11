from utils.db import db
from sqlalchemy import Column, Integer, String, UniqueConstraint,Index
from sqlalchemy.exc import IntegrityError
from models.usuario import User
import json
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Clase Cubo
class Cube(db.Model):

    __tablename__ = 'cubessaved'

    idCube = db.Column(db.Integer, primary_key=True)
    idUsu = db.Column(db.Integer, db.ForeignKey('users.idUsu'))
    cubeState = db.Column(db.String(255))
    # Relacion con User
    usuario = db.relationship('User', back_populates='cubos_saved')
    #Unique restriction
    __table_args__ = (
        UniqueConstraint('cubeState', 'idUsu', name='_cube_state_user_uc'),
    )
    # Iniciamos el objeto así por defecto
    def __init__(
        self,
        data,userData
    ):
        self.idCube = None
        self.idUsu = userData['idUsu'],
        self.cubeState = data['cubeColor']

    def to_dict(self):
        return {
            'idCube': self.idCube,
            'idUsu': self.idUsu,
            'cubeState': self.cubeState,
        }
            