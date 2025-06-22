from pydantic import BaseModel, ConfigDict

class CursoBase(BaseModel):
    curso: str
    departamento_curso: int

class CursoCreate(CursoBase):
    pass

class CursoRead(CursoBase):
    pass