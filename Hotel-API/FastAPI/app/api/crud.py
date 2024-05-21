from sqlalchemy.orm import Session
from app.api.models.model import Reserva, Quarto
from app.api.models.schemas import ReservaCreate, ReservaUpdate

def adicionar_reserva(db: Session, reserva: ReservaCreate) -> Reserva:
    quarto = db.query(Quarto).filter(Quarto.classe == reserva.tipo_quarto).first()
    if not quarto or quarto.quantidade <= 0:
        raise ValueError("Não há quartos disponíveis desta classe.")

    db_reserva = Reserva(
        numero_BI=reserva.numero_BI,
        nome_cliente=reserva.nome_cliente,
        email_cliente=reserva.email_cliente,
        telefone_cliente=reserva.telefone_cliente,
        tipo_quarto=reserva.tipo_quarto,
        check_in=reserva.check_in,
        check_out=reserva.check_out,
        status=reserva.status
    )
    db.add(db_reserva)
    quarto.quantidade -= 1
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def cancelar_reserva(db: Session, numero_BI: str):
    reserva = db.query(Reserva).filter(Reserva.numero_BI == numero_BI).first()
    if not reserva:
        raise ValueError("Reserva não encontrada.")

    quarto = db.query(Quarto).filter(Quarto.classe == reserva.tipo_quarto).first()
    if not quarto:
        raise ValueError("Classe de quarto inválida.")

    db.delete(reserva)
    quarto.quantidade += 1
    db.commit()

def obter_todas_reservas(db: Session) -> list[Reserva]:
    return db.query(Reserva).all()

def obter_quartos_disponiveis(db: Session) -> list[Quarto]:
    return db.query(Quarto).all()

def buscar_reserva_por_numero_BI(db: Session, numero_BI: str) -> Reserva:
    return db.query(Reserva).filter(Reserva.numero_BI == numero_BI).first()

def atualizar_reserva(db: Session, numero_BI: str, reserva_update: ReservaUpdate) -> Reserva:
    reserva = db.query(Reserva).filter(Reserva.numero_BI == numero_BI).first()
    if not reserva:
        raise ValueError("Reserva não encontrada.")

    if reserva.tipo_quarto != reserva_update.tipo_quarto:
        quarto_atual = db.query(Quarto).filter(Quarto.classe == reserva.tipo_quarto).first()
        quarto_novo = db.query(Quarto).filter(Quarto.classe == reserva_update.tipo_quarto).first()

        if quarto_novo.quantidade <= 0:
            raise ValueError("Não há quartos disponíveis desta classe.")

        quarto_atual.quantidade += 1
        quarto_novo.quantidade -= 1

    for key, value in reserva_update.dict().items():
        setattr(reserva, key, value)

    db.commit()
    db.refresh(reserva)
    return reserva
