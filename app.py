from flask import Flask, request
from routes.usuarios import usuarios
from routes.algoritmos import algoritmos
from routes.saveCube import cubeSave
from routes.tiemposCuboUsers import tiempoCubo
from utils.db import db
from flask_marshmallow import Marshmallow
from flask_cors import CORS


# Creamos la app de Flask
app = Flask(__name__)
# configuracion de SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root@localhost/rubiktrainerdatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# Inicializamos el objeto db
db.init_app(app)
ma = Marshmallow(app)
CORS(app, supports_credentials=True)
#para reconocer el blueprint
app.register_blueprint(tiempoCubo)
app.register_blueprint(cubeSave)
app.register_blueprint(usuarios)
app.register_blueprint(algoritmos)
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = (
#             "idUsu",
#             "password",
#             "name",
#             "email",
#             "admin",
#             "dinero",
#             "remember_token",
#             "email_verify",
#             "creado_en",
#             "actualizado_en",
#         )


# user_schema = UserSchema()
# users_schema = UserSchema(many=True)