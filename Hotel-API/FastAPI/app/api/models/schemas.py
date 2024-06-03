from typing import Optional
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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True