from pydantic import BaseModel
from datetime import datetime

class ReservaBase(BaseModel):
    numero_BI: str
    nome_cliente: str
    email_cliente: str
    telefone_cliente: str
    tipo_quarto: str
    check_in: datetime
    check_out: datetime
    status: str

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(ReservaBase):
    pass

class ReservaInDBBase(ReservaBase):
    class Config:
        from_attributes = True

class Reserva(ReservaInDBBase):
    pass

class QuartoBase(BaseModel):
    classe: str
    quantidade: int

class Quarto(QuartoBase):
    id: int

    class Config:
        from_attributes = True

