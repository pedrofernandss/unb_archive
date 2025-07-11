from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date


class AvaliacaoBase(BaseModel):
    data_avaliacao: date
    nota: float = Field(..., ge=1, le=5)
    id_material: int


class AvaliacaoCreate(AvaliacaoBase):
    pass


class AvaliacaoRead(AvaliacaoBase):
    id_avaliacao: int


class AvaliacaoUpdate(BaseModel):
    data_avaliacao: Optional[date] = None
    nota: Optional[Decimal] = None
