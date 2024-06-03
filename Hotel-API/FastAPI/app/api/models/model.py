from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base

class Quarto(Base):
    __tablename__ = "quartos"
    id = Column(Integer, primary_key=True, index=True)
    classe = Column(String, index=True, unique=True)
    quantidade = Column(Integer)

class Reserva(Base):
    __tablename__ = "reservas"
    numero_BI = Column(String, primary_key=True, index=True)
    nome_cliente = Column(String)
    email_cliente = Column(String)
    telefone_cliente = Column(String)
    tipo_quarto = Column(String, ForeignKey('quartos.classe'))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    status = Column(String)

    quarto = relationship("Quarto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
