from utils.db import db
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import json

# Clase algoritmos
class Algoritmo(db.Model):
    
    __tablename__ = 'algoritmos'

    idAlg = db.Column(db.String(255))
    nombreAlg = db.Column(db.String(255), unique=True, primary_key=True)
    algoritmo = db.Column(db.String(255))
    algoritmosPosibles = db.Column(db.String(255))
    #Metodo todict para crear el objeto
    def to_dict(self):
        return {
            'idAlg': self.idAlg,
            'nombreAlg': self.nombreAlg,
            'algoritmo': self.algoritmo,
            'algoritmosPosibles': json.loads(self.algoritmosPosibles) if self.algoritmosPosibles else None
        }
            