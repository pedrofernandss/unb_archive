from pydantic import BaseModel, ConfigDict
from typing import Optional

class ReputacaoBase(BaseModel):
    pontuacao: int
    nivel: Optional[str] = None

class ReputacaoCreate(ReputacaoBase):
    pass

class ReputacaoRead(ReputacaoBase):
    id_reputacao: int

class ReputacaoUpdate(BaseModel):
    pontuacao: Optional[int] = None
    nivel: Optional[str] = None