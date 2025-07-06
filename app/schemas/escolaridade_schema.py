from pydantic import BaseModel, ConfigDict

class EscolaridadeBase(BaseModel):
    escolaridade: str
    departamento_escolaridade: int

class EscolaridadeCreate(EscolaridadeBase):
    pass

class EscolaridadeRead(EscolaridadeBase):
    pass

class EscolaridadeUpdate(BaseModel):
    escolaridade: str