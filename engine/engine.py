from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# crea una instancia de Engine
engine = create_engine('mysql+pymysql://root@localhost/rubiktrainerdatabase')

# crea una sesión
Session = sessionmaker(bind=engine)
session = Session()

