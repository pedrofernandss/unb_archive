from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class UniversidadeBase(BaseModel):
    nome: str
    cidade: str
    estado: str

class UniversidadeCreate(UniversidadeBase):
    pass

class UniversidadeRead(UniversidadeBase):
    ies: int

class UniversidadeUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

