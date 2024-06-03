from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.models.model import Base
from app.database.session import init_db, engine
from app.api.models.model import User

def verificar_tabela_reservas(): 
    Base.metadata.create_all(bind=engine)

verificar_tabela_reservas()
