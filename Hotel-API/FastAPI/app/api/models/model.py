from pydantic import BaseModel


class Reserva(BaseModel):
    nome_cliente: str
    email_cliente: str
    telefone_cliente: str
    tipo_quarto: str
    check_in: int
    check_out: int
    status: str = "ativa"