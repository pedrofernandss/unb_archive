from pydantic import BaseModel, ConfigDict
from typing import Optional

class TagBase(BaseModel):
    nome_tag: str

class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id_tag: int

class TagUpdate(BaseModel):
    nome_tag: Optional[str] = None
