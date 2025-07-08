from pydantic import BaseModel

class ValidacaoMaterialRequest(BaseModel):
    """
    Schema para os dados de entrada da procedure de validação de material.
    """
    id_material: int
    cpf_docente: str
    acao_valida: bool