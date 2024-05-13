from fastapi import APIRouter, FastAPI, HTTPException
from datetime import datetime
from app.api.routes import route
from app.api.models.model import Reserva
from app.database.base import verificar_tabela_reservas

app = FastAPI()
router = APIRouter()

verificar_tabela_reservas()

app.include_router(route.router, tags=["Reservas Internas"])

QUARTOS_CLASSE_A = 5
QUARTOS_CLASSE_B = 15
QUARTOS_CLASSE_C = 30

quartos_reservados = []

@app.post("/reserva/")
def fazer_reserva(reserva: Reserva):
    global QUARTOS_CLASSE_A, QUARTOS_CLASSE_B, QUARTOS_CLASSE_C
    
    if reserva.tipo_quarto == "A":
        if QUARTOS_CLASSE_A > 0:
            QUARTOS_CLASSE_A -= 1
            quartos_reservados.append(reserva)
            return {"message": "Reserva feita com sucesso!"}
        else:
            raise HTTPException(status_code=400, detail="Não há quartos disponíveis desta classe.")
    elif reserva.tipo_quarto == "B":
        if QUARTOS_CLASSE_B > 0:
            QUARTOS_CLASSE_B -= 1
            quartos_reservados.append(reserva)
            return {"message": "Reserva feita com sucesso!"}
        else:
            raise HTTPException(status_code=400, detail="Não há quartos disponíveis desta classe.")
    elif reserva.tipo_quarto == "C":
        if QUARTOS_CLASSE_C > 0:
            QUARTOS_CLASSE_C -= 1
            quartos_reservados.append(reserva)
            return {"message": "Reserva feita com sucesso!"}
        else:
            raise HTTPException(status_code=400, detail="Não há quartos disponíveis desta classe.")
    else:
        raise HTTPException(status_code=400, detail="Classe de quarto inválida.")


@app.delete("/reserva/{id}/")
def cancelar_reserva(id: int):
    global quartos_reservados, QUARTOS_CLASSE_A, QUARTOS_CLASSE_B, QUARTOS_CLASSE_C
    
    if id < 0 or id >= len(quartos_reservados):
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    
    reserva_cancelada = quartos_reservados.pop(id)
    
    if reserva_cancelada.tipo_quarto == "A":
        QUARTOS_CLASSE_A += 1
    elif reserva_cancelada.tipo_quarto == "B":
        QUARTOS_CLASSE_B += 1
    elif reserva_cancelada.tipo_quarto == "C":
        QUARTOS_CLASSE_C += 1

    return {"message": "Reserva cancelada com sucesso."}


@app.get("/quartos-disponiveis/")
def quartos_disponiveis():
    return {
        "Quartos disponíveis": {
            "Classe A": QUARTOS_CLASSE_A,
            "Classe B": QUARTOS_CLASSE_B,
            "Classe C": QUARTOS_CLASSE_C
        }
    }