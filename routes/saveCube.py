from flask import Blueprint, request, jsonify
from models.saveCube import Cube
from models.usuario import check_password_hash
import jwt
from flask_cors import cross_origin
from engine.engine import session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

# para no usar app.route si no que lo modificamos a cada endpoint
cubeSave = Blueprint("cubeSave", __name__)


#Ruta para guardar el cubo del Usuario
@cubeSave.route("/saveCube", methods=["POST"])
def saveCube():
    print("g")
    data = request.get_json()
    #Guardarmos el cubo en el usuario
    userData = checkUserId(data)
    # cube_states = session.query(Cube.cubeState).filter(Cube.idUsu == idUsu).all()
    guardarCubo(data,userData)
    return jsonify(data)
#Metodo para comprobar id de usuario desencriptando con la contraseña
def checkUserId(data):
    # Decodifica el token JWT
    decoded = jwt.decode(data['token'], "secretRubik", algorithms=["HS256"])
    return decoded

#Metodo para guardar el cubo en la base de datos
def guardarCubo(data, userData):
        try:
        # agrega el nuevo usuario a la sesión y hace commit
            newCube = Cube(data,userData)
            session.add(newCube)
            session.commit()
            session.close()
            return True
        #Manejo de errores
        except IntegrityError as e:
            array_response = []
            session.rollback()
            session.close()
            # maneja el error de violación de la restricción unique
            error_message = str(e)
            if "Duplicate entry" in error_message:
                key = error_message.split("for key '")[1].split("'")[0]
                if key == 'cubeState':
                    array_response.append('Error: El cubo añadido ya está en la lista')
            print(error_message)
            return array_response
#Ruta para obtener todos los cubos al cargar la pagina
@cubeSave.route("/getListCubes", methods=["POST"])
def getCubes():
    data = request.get_json()
    userData = checkUserId(data)
    #Objtenemos todos los objetos de cubos
    cube_states = session.query(Cube.cubeState).filter(Cube.idUsu == userData['idUsu']).all()
    # Recorre los resultados y almacena los cubeState en una lista
    cube_states_list = [cube_state[0] for cube_state in cube_states]

    return jsonify(cube_states_list)

#Ruta para borrar el cubo que seleccionemos
@cubeSave.route("/deleteCube", methods=["POST"])
def deleteCube():
    data = request.get_json()
    userData = checkUserId(data)
    cube_state = data['cubeColor']
    # Realizar la eliminación del cube_state que coincide con el usuario específico
    delete_stmt = delete(Cube).where(Cube.cubeState == cube_state, Cube.idUsu == userData['idUsu'])
    session.execute(delete_stmt)
    
    # Confirmar los cambios en la base de datos
    session.commit()
    session.close()
    return jsonify(success=True)


#Metodo check usuario
def checkUserId(data):
    # Decodifica el token JWT
    decoded = jwt.decode(data['token'], "secretRubik", algorithms=["HS256"])
    return decoded