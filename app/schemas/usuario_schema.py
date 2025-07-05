from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class UsuarioBase(BaseModel):
    cpf: str
    nome: str
    matricula: int
    email: str
    id_departamento: int

class DiscenteBase(UsuarioBase):
    status: str
    ano_ingresso: int
    coeficiente_rendimento: Decimal
    id_reputacao: Optional[int] = None

class DocenteBase(UsuarioBase):
    especialidade: str
    permissao_validacao: bool
    id_avalia: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    senha: str

class DiscenteCreate(UsuarioCreate, DiscenteBase):
    pass 

class DocenteCreate(UsuarioCreate, DocenteBase):
    pass

class DiscenteRead(DiscenteBase):
    pass

class DocenteRead(DocenteBase):
    pass

class DiscenteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    coeficiente_rendimento: Optional[Decimal] = None

class DocenteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    especialidade: Optional[str] = None
    permissao_validacao: Optional[bool] = None