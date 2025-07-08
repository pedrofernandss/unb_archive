from pydantic import BaseModel
from typing import Optional, List

class MaterialCompleto(BaseModel):
    id_material: int
    material_nome: str
    descricao: Optional[str] = None
    ano_semestre_ref: Optional[str] = None
    disciplina_nome: Optional[str] = None
    departamento_nome: Optional[str] = None
    universidade_nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    media_avaliacoes: float
    total_avaliacoes: int
    usuarios_associados: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        orm_mode = True