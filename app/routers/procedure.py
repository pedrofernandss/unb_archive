from fastapi import APIRouter, HTTPException, status
from app.repositories import procedure_repository
from app.schemas.procedure_schema import ValidacaoMaterialRequest

router = APIRouter()

@router.post("/procedures/gerenciar-validacao", status_code=status.HTTP_204_NO_CONTENT,summary="Executa a lógica de validação de um material por um docente")
def executar_validacao_material(request_data: ValidacaoMaterialRequest):
    """
    Este endpoint executa a procedure gerenciar_validacao_material.

    - id_material: O ID do material a ser validado/invalidado.
    - cpf_docente: O CPF do docente que está realizando a ação.
    - acao_valida: true para validar o material, false para invalidar.

    A procedure irá:
    1.  Verificar as permissões do docente.
    2.  Registrar a validação na tabela Avalia.
    3.  Atualizar os contadores de validação do docente.
    4.  Ajustar a reputação do discente que postou o material.
    """
    try:
        procedure_repository.execute_gerenciar_validacao_material(request_data)

        return
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao executar a procedure: {str(e)}"
        )