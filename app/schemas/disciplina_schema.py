from pydantic import BaseModel, ConfigDict
from typing import Optional


class DisciplinaBase(BaseModel):
    nome: Optional[str] = None
    iddepartamento: int


class DisciplinaCreate(DisciplinaBase):
    pass


class DisciplinaRead(DisciplinaBase):
    codigo: int


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    iddepartamento: Optional[int] = None
