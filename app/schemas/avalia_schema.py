from pydantic import BaseModel, ConfigDict
from typing import Optional

class AvaliaBase(BaseModel):
    idDocente: Optional[str] = None
    idMaterial: Optional[int] = None

class AvaliaCreate(AvaliaBase):
    pass

class AvaliaRead(AvaliaBase):
    id_avalia: int

class AvaliaUpdate(BaseModel):
    pass