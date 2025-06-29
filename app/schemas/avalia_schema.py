from pydantic import BaseModel, ConfigDict
from typing import Optional

class AvaliaBase(BaseModel):
    idDocente: str
    idMaterial: int

class AvaliaCreate(AvaliaBase):
    pass

class AvaliaRead(AvaliaBase):
    id_avalia: int

class AvaliaUpdate(BaseModel):
    pass