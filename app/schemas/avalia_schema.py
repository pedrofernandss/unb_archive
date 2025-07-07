from pydantic import BaseModel
from typing import Optional

# 1. Nomes dos campos corrigidos para snake_case
class AvaliaBase(BaseModel):
    iddocente: str
    idmaterial: int
    valido: Optional[bool] = True

class AvaliaCreate(AvaliaBase):
    pass

# 2. AvaliaRead agora reflete a estrutura real da tabela (sem id_avalia)
class AvaliaRead(AvaliaBase):
    pass

# 3. AvaliaUpdate agora permite alterar apenas o campo 'valido'
class AvaliaUpdate(BaseModel):
    valido: Optional[bool] = None