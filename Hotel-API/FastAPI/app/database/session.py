from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "sqlite:///./app/database/hotel.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from app.api.models.model import Base, Quarto
    Base.metadata.create_all(bind=engine)
    
    # Inicializa os dados de quartos
    db = SessionLocal()
    try:
        # Verifica se os quartos já estão inicializados
        if not db.query(Quarto).first():
            db.add_all([
                Quarto(classe="A", quantidade=5),
                Quarto(classe="B", quantidade=15),
                Quarto(classe="C", quantidade=30)
            ])
            db.commit()
    finally:
        db.close()

init_db()
