from utils.db import db
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from engine.engine import session
from sqlalchemy.exc import IntegrityError

# Clase User SQLArchemist
class User(db.Model):

    __tablename__ = 'users'

    idUsu = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    email = db.Column(db.String(250), unique = True)
    admin = db.Column(db.Boolean)
    email_verify = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime)
    actualizado_en = db.Column(db.DateTime)
    # Relaciones con Cube y TiemposCuboUser
    cubos_saved = db.relationship('Cube', cascade='all, delete', back_populates='usuario')
    tiempos_cubo = db.relationship('TiemposCuboUser', cascade='all, delete', back_populates='usuario')

    #Init para el objeto
    def __init__(
        self,
        data
    ):
        self.idUsu = None
        self.name = data['name']
        self.password = generate_password_hash(data['password'])
        self.email = data['email']
        self.admin = False
        self.email_verify = None,
        self.creado_en=datetime.now()
        self.actualizado_en=datetime.now()
    #Metodo para verificar la contraseña
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.password, contraseña)


    #Metodo para generar un token con sus datos más importantes
    def generar_token_de_acceso(self):
        #expiracion = datetime.utcnow() + timedelta(days=10)
        payload = {
            'idUsu': self.idUsu,
            'name': self.name,
            'password': self.password
        }
        
        token = jwt.encode(payload, 'secretRubik', algorithm='HS256')
        return token

    #Metodo crear Usuario
    def crearUsuario(self, data):
        try:
        # agrega el nuevo usuario a la sesión y hace commit
            new_user = User(data)
            session.add(new_user)
            session.commit()
            session.close()
            return True

        except IntegrityError as e:
            #Deshace los cambios
            array_response = []
            session.rollback()
            session.close()
            # maneja el error de violación de la restricción unique
            error_message = str(e)
            #Detecta errores y los retorna
            if "Duplicate entry" in error_message:
                key = error_message.split("for key '")[1].split("'")[0]
                if key == 'name':
                    array_response.append('Error: El nombre de usuario ya existe')
            usuario_existente = User.query.filter_by(email=data['email']).first()
            if usuario_existente != None:
                array_response.append('Error: El correo electrónico ya existe')
            print(error_message)
            return array_response
            