from flask import Blueprint, request, jsonify
from models.tiemposCuboUsers import TiemposCuboUser
from models.usuario import check_password_hash
import jwt
from flask_cors import cross_origin
from engine.engine import session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

# para no usar app.route si no que lo modificamos a cada endpoint
tiempoCubo = Blueprint("tiemposCuboUsers", __name__)

#Ruta para guardar el tiempo del cubo
@tiempoCubo.route("/saveTiempoCubo", methods=["POST"])
def saveTiempoCubo():
    print("g")
    data = request.get_json()
    userData = checkUserId(data)
    #Guardamos el tiempo
    # cube_states = session.query(Cube.cubeState).filter(Cube.idUsu == idUsu).all()
    guardarTiempoUser(data,userData)
    return jsonify(data)
#Metodo para checkear el UserId
def checkUserId(data):
    # Decodifica el token JWT
    decoded = jwt.decode(data['token'], "secretRubik", algorithms=["HS256"])
    return decoded

#Metodo para guardar el tiempo del usuario
def guardarTiempoUser(data, userData):
        try:
        # agrega el nuevo usuario a la sesión y hace commit
            newTiempo = TiemposCuboUser(data,userData)
            session.add(newTiempo)
            session.commit()
            session.close()
            return True
        #Manejo del error y rollback
        except IntegrityError as e:
            array_response = []
            session.rollback()
            session.close()
            return array_response

#Ruta para obtener todos los tiempo de los cubos
@tiempoCubo.route("/getTiempoCubes", methods=["POST"])
def getTiempos():
    data = request.get_json()
    userData = checkUserId(data)
    cube_states = session.query(TiemposCuboUser).filter(TiemposCuboUser.idUsu == userData['idUsu']).all()

    # Crear una lista de diccionarios utilizando el método to_dict() de TiemposCuboUser
    cube_states_list = [cube_state.to_dict() for cube_state in cube_states]

    return jsonify(cube_states_list)

#Metodo para eliminar el tiempo de la lista elegido
@tiempoCubo.route("/deleteTiempoLista", methods=["POST"])
def deleteTiempo():
    data = request.get_json()
    userData = checkUserId(data)
    idTiempo = int(data['idTiempo'])
    # Realizar la eliminación del cube_state que coincide con el usuario específico
    delete_stmt = delete(TiemposCuboUser).where(TiemposCuboUser.idTiempo == idTiempo, TiemposCuboUser.idUsu == int(userData['idUsu']))
    session.execute(delete_stmt)
    
    # Confirmar los cambios en la base de datos
    session.commit()
    session.close()
    return jsonify(success=True)