from pydantic import BaseModel, ConfigDict
from typing import Optional


class MaterialBase(BaseModel):
    nome: str
    descricao: str
    ano_semestre_ref: str
    local_arquivo: str
    id_disciplina: str


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id_material: int
    idAvalia: Optional[int] = None


class MaterialUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ano_semestre_ref: Optional[str] = None
