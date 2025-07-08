from pydantic import BaseModel

class PossuiBase(BaseModel):
    id_material: int
    id_tag: int

class PossuiCreate(PossuiBase):
    pass

class PossuiRead(PossuiBase):
    pass
