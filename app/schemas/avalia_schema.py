from pydantic import BaseModel, ConfigDict
from typing import Optional

class AvaliaBase(BaseModel):
    iddocente: str
    idmaterial: int
    valido: bool = True

class AvaliaCreate(AvaliaBase):
    pass

class AvaliaRead(AvaliaBase):
    id_avalia: int

class AvaliaUpdate(BaseModel):
    iddocente: Optional[str] = None
    valido: Optional[bool] = None