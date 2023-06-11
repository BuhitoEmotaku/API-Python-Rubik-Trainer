from app import app
from utils.db import db
from waitress import serve
#cuando arranca crea las tablas
with app.app_context():
    db.create_all()
#Inicia la app
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
