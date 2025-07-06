from pydantic import BaseModel, ConfigDict
from typing import Optional

class PossuiBase(BaseModel):
    id_material: int
    id_tag: int

class PossuiCreate(PossuiBase):
    pass

class PossuiRead(PossuiBase):
    id_possui: int
    id_material: int
    id_tag: int

class PossuiUpdate(BaseModel):
    id_material: Optional[int] = None
    id_tag: Optional[int] = None