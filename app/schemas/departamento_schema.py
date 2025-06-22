from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class DepartamentoBase(BaseModel):
    nome: str
    id_universidade: int

class DepartamentoCreate(DepartamentoBase):
    pass

class DepartamentoRead(DepartamentoBase):
    id_departamento: int

class DepartamentoUpdate(BaseModel):
    nome: Optional[str] = None