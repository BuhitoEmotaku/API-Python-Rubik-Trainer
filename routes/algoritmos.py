from flask import Blueprint, request, jsonify
from models.algoritmos import Algoritmo
import logging
from engine.engine import session
import twophase.solver  as sv
import kociemba
logger = logging.getLogger()

# para no usar app.route si no que lo modificamos a cada endpoint
algoritmos = Blueprint("algoritmos", __name__)

#Ruta para sacar la lista de algoritmos
@algoritmos.route("/algoritmos", methods=["POST"])
def listaAlgoritmos():
    data = request.get_json()
    id_algoritmo = data['id_algoritmo']
    #Sacamos todos los objetos de los algoritmos
    respuesta = session.query(Algoritmo).filter(Algoritmo.idAlg == id_algoritmo.strip()).all()
    #Sacamos todos los datos con el metodo todict
    if respuesta:
        respuesta_json = [algoritmo.to_dict() for algoritmo in respuesta]
        return jsonify(respuesta_json)
    else:
        return jsonify({'error': 'No se encontraron resultados'})
    

#Ruta para sacar la solución más óptima con Kociemba
@algoritmos.route("/kociemba", methods=["POST"])
def kociembaMethod():
    try:
        #Pasamos el cuestring y lo resolvemos
        data = request.get_json()
        cubestring = data['patternAlg']
        print(cubestring)
        # result = sv.solve(cubestring,19,2)
        result = kociemba.solve(cubestring)
        print(result)
        return jsonify(result)
        #Manejamos la excepcion
    except Exception as e:
        print("Se produjo un error:", str(e))
        return jsonify(False)
