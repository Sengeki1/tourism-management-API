from fastapi import FastAPI, APIRouter
from app.api.models.model import Reserva
from app.database.session import conectar_bd

app = FastAPI()
router = APIRouter()

# Endpoint para criar uma nova reserva
@router.post("/reservas/")
async def criar_reserva(reserva: Reserva):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reservas (nome_cliente, email_cliente, telefone_cliente, tipo_quarto, check_in, check_out, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (reserva.nome_cliente, reserva.email_cliente, reserva.telefone_cliente,
          reserva.tipo_quarto, reserva.check_in,
          reserva.check_out, reserva.status))
    conn.commit()
    conn.close()
    return {"message": "Reserva feita com sucesso!"}


# Endpoint para obter todas as reservas
@router.get("/reservas/")
async def obter_reservas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()
    conn.close()
    return {"reservas": reservas}