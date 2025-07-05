from pydantic import BaseModel, ConfigDict
from typing import Optional


class AvaliaBase(BaseModel):
    id_docente: str
    id_material: int
    valido: bool = True


class AvaliaCreate(AvaliaBase):
    pass


class AvaliaRead(AvaliaBase):
    id_avalia: int


class AvaliaUpdate(BaseModel):
    id_docente: Optional[str] = None
    valido: Optional[bool] = None
