Datos para el necesario inicio de app

28/abril
#1
pip install virtualenv
#2
Creamos entorno
python3 -m virtualenv venv
#3
Activamos el entorno
En (cmd)
.\venv\Scripts\activate.bat
#5
Instalamos todas las dependencias
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pymysql

#Creamos modelo, index, app.py y rutas
#Todo lo que se haga, se hace dentro del entorno virtual sí o sí

Hay que instalar los requirements para su uso


Arrancar con
gunicorn --bind 0.0.0.0:5000 wsgi:index

waitress-serve --host=127.0.0.1 --port=5000 index:app