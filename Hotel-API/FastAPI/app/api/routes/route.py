from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.api.models.schemas import ReservaCreate, ReservaUpdate, Reserva
from app.api.crud import (
    adicionar_reserva, 
    cancelar_reserva, 
    obter_todas_reservas, 
    obter_quartos_disponiveis, 
    buscar_reserva_por_numero_BI, 
    atualizar_reserva
)

router = APIRouter()

# Dependência para obter a sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar uma nova reserva
@router.post("/criar_reserva/", response_model=Reserva)
async def criar_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    try:
        db_reserva = adicionar_reserva(db, reserva)
        return db_reserva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para obter todas as reservas
@router.get("/reservas/", response_model=list[Reserva])
async def obter_reservas(db: Session = Depends(get_db)):
    return obter_todas_reservas(db)

# Endpoint para cancelar uma reserva
@router.delete("/delete_reserva/{numero_BI}/")
async def cancelar_reserva_endpoint(numero_BI: str, db: Session = Depends(get_db)):
    try:
        cancelar_reserva(db, numero_BI)
        return {"message": "Reserva cancelada com sucesso."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para obter a disponibilidade dos quartos
@router.get("/quartos-disponiveis/")
async def quartos_disponiveis(db: Session = Depends(get_db)):
    quartos = obter_quartos_disponiveis(db)
    return {"Quartos disponíveis": {quarto.classe: quarto.quantidade for quarto in quartos}}

# Endpoint para buscar uma reserva pelo número de BI
@router.get("/buscar_reserva/{numero_BI}/", response_model=Reserva)
async def buscar_reserva(numero_BI: str, db: Session = Depends(get_db)):
    db_reserva = buscar_reserva_por_numero_BI(db, numero_BI)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada.")
    return db_reserva

# Endpoint para atualizar uma reserva
@router.put("/atualizar_reserva/{numero_BI}/", response_model=Reserva)
async def atualizar_reserva_endpoint(numero_BI: str, reserva_update: ReservaUpdate, db: Session = Depends(get_db)):
    try:
        db_reserva = atualizar_reserva(db, numero_BI, reserva_update)
        return db_reserva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
