from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.api.routes import route
from app.api.models.model import Reserva
from app.database.base import verificar_tabela_reservas
from app.database.session import conectar_bd

app = FastAPI()

# Verifica se o banco de dados existe, se não existir, cria o banco e a tabela
verificar_tabela_reservas()
