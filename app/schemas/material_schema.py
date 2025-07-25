from pydantic import BaseModel, ConfigDict
from typing import Optional


class MaterialBase(BaseModel):
    nome: str
    descricao: str
    ano_semestre_ref: str
    id_disciplina: int


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id_material: int
    id_avalia: Optional[int] = None

    class Config: from_atributes = True


class MaterialUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ano_semestre_ref: Optional[str] = None