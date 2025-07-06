from typing import Optional
from pydantic import BaseModel

class CursoBase(BaseModel):
    curso: str
    departamento_curso: int

class CursoCreate(CursoBase):
    pass

class CursoRead(CursoBase):
    pass

class CursoUpdate(BaseModel):
    curso: Optional[str] = None
    departamento_curso: Optional[int] = None