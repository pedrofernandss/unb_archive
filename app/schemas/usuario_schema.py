from typing import Optional
from pydantic import BaseModel
from decimal import Decimal

class UsuarioBase(BaseModel):
    cpf: str
    nome: str
    matricula: int
    senha: str
    id_departamento: int

class DiscenteBase(UsuarioBase):
    status: str
    ano_ingresso: int
    coeficiente_rendimento: Decimal

class DocenteBase(UsuarioBase):
    especialidade: str
    permissao_validacao: bool
    idAvalia: Optional[int] = None