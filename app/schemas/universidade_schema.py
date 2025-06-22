from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class UniversidadeBase(BaseModel):
    nome: str
    cidade: int
    estado: str

class UniversidadeCreate(UniversidadeBase):
    pass

class UniversidadeRead(UniversidadeBase):
    pass

class UniversidadeUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

