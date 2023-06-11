from flask import Blueprint, request, jsonify
from models.usuario import User
from models.usuario import check_password_hash
import logging
from flask_cors import cross_origin
from engine.engine import session 
import json
import jwt
import re
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
# Email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Para pintar datos
logger = logging.getLogger()

# para no usar app.route si no que lo modificamos a cada endpoint
usuarios = Blueprint("usuarios", __name__)

#Metodo para descifrar el Token
def descifrarToken(token):
    # Decodifica el token JWT
    try:
        decoded = jwt.decode(token, "secretRubik", algorithms=["HS256"])
        # Resto del código si la decodificación es exitosa
    except Exception as e:
        # Manejo del error
        decoded = False
    return decoded

#Metodo para ver el usuario correcto
def checkUsuarioCorrecto(data):

    # Buscar usuario en la base de datos
    #User.query.filter_by(name=data["name"]).first()
    usuario = session.query(User).filter(User.name == data["name"]).first()
    # Verificar si el usuario existe y si la contraseña es correcta
    #hacemos return de los datos
    session.close()
    if usuario is None or not usuario.verificar_contraseña(data["password"]):
        return False
    else: return usuario
    # Ruta para loguearse
    
@usuarios.route("/loguear", methods=["POST"])
def loguearWeb():
    data = request.get_json()
    #check usuario is true
    usuario = checkUsuarioCorrecto(data)
    if(usuario == False):
        return jsonify({"mensaje": "Nombre de usuario o contraseña incorrectos"})
    
    token = usuario.generar_token_de_acceso()
    # Si el usuario existe y la contraseña es correcta, devolver un token de acceso
    return jsonify(token)
    # name = request.json["name"]
    # name = request.json["password"]
    # name = request.json["email"]
    
#Ruta para checkear login
@usuarios.route("/checkLogin", methods=["POST"])
def checkLogin():
    data = request.get_json()
    tokenDecoded = descifrarToken(data["token"])
    #Si es true return
    checkUsuarioCorrecto(tokenDecoded)
    # Si el usuario existe y la contraseña es correcta, devolver un token de acceso
    return jsonify(True)

#Ruta para borrar usuario
@usuarios.route("/borrarUser", methods=["POST"])
def borrarUsuario():
    data = request.get_json()
    tokenDecoded = descifrarToken(data["token"])
    # Identifica el idUsu del usuario que deseas eliminar
    idUsu = tokenDecoded['idUsu']  # Reemplaza con el idUsu correcto obtenido del token

    # Recupera el usuario de la base de datos
    user = session.query(User).filter(User.idUsu == idUsu).first()

    if user:
        try:
            # Elimina el usuario y todas las filas relacionadas automáticamente
            session.delete(user)

            # Confirma la transacción
            session.commit()

            print("Usuario y filas relacionadas eliminados exitosamente")
        except:
            # Si ocurre un error, realiza un rollback de la transacción
            session.rollback()
            print("Error al eliminar el usuario y las filas relacionadas")
    else:
        print("El usuario no existe")

    # Cierra la sesión
    session.close()
    return jsonify(True)

#Ruta para registrar usuario
@usuarios.route("/registrar", methods=["POST"])
def registrarWeb():

    array_response = []
    check = False
    data = request.get_json()
    #Comprobar todos los campos y si coinciden
    tokenDecoded = descifrarToken(data["clave"])
    if(tokenDecoded == False):
        return jsonify(False)
    print(tokenDecoded['name'],tokenDecoded['email'])
    if(tokenDecoded['name'] != data['name']):
        array_response.append("El nombre no coincide con el de los campos.")
        check = True
    if(tokenDecoded['email'] != data['email']):
        array_response.append("El email no coincide con el de los campos.")
        check = True

    usuario_existente = User.query.filter_by(name=tokenDecoded['name']).first()
    if usuario_existente is not None:
        check = True
        array_response.append('Error: El nombre de usuario ya existe')

    usuario_existente = User.query.filter_by(email=tokenDecoded['email']).first()
    if usuario_existente is not None:
        check = True
        array_response.append('Error: El correo electrónico ya existe')
    
    # Expresión regular para verificar el formato del correo electrónico
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, data['email']):
        print("El correo electrónico es válido.")
    else:
         array_response.append("El correo electrónico no es válido.")
         check = True
    if(check):
        return array_response
    else:
        print (data)
        respuesta = User(data).crearUsuario(data)
        return jsonify(respuesta)




#Ruta para cambiar contraseña
@usuarios.route("/cambiarContrasena", methods=["POST"])
def cambiarContrasena():
    data = request.get_json()
    tokenContra = descifrarToken(data['token'])
    if(tokenContra == False):
        return jsonify('false')
    #Hacemos update de la contraseña con ese email
    query = text("UPDATE users SET password = :contra WHERE email = :email")
    session.execute(query, {"contra": generate_password_hash(data['contrasenaNueva']), "email": tokenContra['email']})
    session.close()
    return jsonify('true')


#Ruta para recuperarContraseña 
@usuarios.route("/recuperarContraseña", methods=["POST"])
def recuperarContraseña():
    data = request.get_json()
    # Expresión regular para verificar el formato del correo electrónico
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, data['email']):
        print("El correo electrónico es válido.")
    else:
         return jsonify('false')
    #expiracion = datetime.utcnow() + timedelta(days=10)
    payload = {
        'email':data['email']
    }
    #Mandamos un correo electrónico
    token = jwt.encode(payload, 'secretRubik', algorithm='HS256')

    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "rubiktrainer@gmail.com"
    email_to = data['email']

    pswd = "nioioiscnkaskavm"

    # content of message

    body = f"""\nBienvenido a RubikTrainer!\n\nEsto es un correo creado simplemente para la recuperación de la contraseña!\n\nEste es el código para la recuperación:\n Código: ({token})\nEl código no incluye paréntesis!\n\nUn saludo, Rubikero!"""

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = "no-reply <rubiktrainer@gmail.com>"
    msg['To'] = data['email']
    msg['Subject'] = 'Email de verificación de Registro - RubikTrainer'

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Cast as string
    text = msg.as_string()
    # Create context
    simple_email_context = ssl.create_default_context()


    try:
        # Connect to the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")
            
        # Send the actual email
        print()
        print(f"Sending email to - {email_to}")
        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to - {email_to}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()
        return jsonify('true')


#ruta para checkearRegistro
@usuarios.route("/checkRegister", methods=["POST"])
def checkRegister():

    data = request.get_json()

    array_response = []
    check = False
    #Si existe devuelve true sino false
    usuario_existente = User.query.filter_by(name=data['name']).first()
    if usuario_existente is not None:
        check = True
        array_response.append('Error: El nombre de usuario ya existe')

    usuario_existente = User.query.filter_by(email=data['email']).first()
    if usuario_existente is not None:
        check = True
        array_response.append('Error: El correo electrónico ya existe')
    
    # Expresión regular para verificar el formato del correo electrónico
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, data['email']):
        print("El correo electrónico es válido.")
    else:
         array_response.append("El correo electrónico no es válido.")
         check = True
    # ...
    
        # Setup port number and servr name
    if(check == False):
        #expiracion = datetime.utcnow() + timedelta(days=10)
        payload = {
            'name': data['name'],
            'email':data['email']
        }
        #Mandamos el correo
        token = jwt.encode(payload, 'secretRubik', algorithm='HS256')

        smtp_port = 587                 # Standard secure SMTP port
        smtp_server = "smtp.gmail.com"  # Google SMTP Server

        email_from = "rubiktrainer@gmail.com"
        email_to = data['email']

        pswd = "nioioiscnkaskavm"

        # content of message

        body = f"""\nBienvenido a RubikTrainer!\n\nEsto es un correo creado simplemente para la verificación de la cuenta!\n\nEste es el código para registrarse:\n Código: ({token})\nEl código no incluye paréntesis!\n\nUn saludo, Rubikero!"""

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = "no-reply <rubiktrainer@gmail.com>"
        msg['To'] = data['email']
        msg['Subject'] = 'Email de verificación de Registro - RubikTrainer'

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Cast as string
        text = msg.as_string()
        # Create context
        simple_email_context = ssl.create_default_context()


        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pswd)
            print("Connected to server :-)")
            
            # Send the actual email
            print()
            print(f"Sending email to - {email_to}")
            TIE_server.sendmail(email_from, email_to, text)
            print(f"Email successfully sent to - {email_to}")

        # If there's an error, print it out
        except Exception as e:
            print(e)

        # Close the port
        finally:
            TIE_server.quit()
            return jsonify('true')

    else:
        return array_response
    
