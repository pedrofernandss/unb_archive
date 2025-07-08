from fastapi import APIRouter, HTTPException, status

from app.schemas.avaliacao_schema import AvaliacaoRead, AvaliacaoCreate, AvaliacaoUpdate

from app.repositories import avaliacao_repository


from typing import List

router = APIRouter()

@router.post("/avaliacao", response_model=AvaliacaoRead, status_code=status.HTTP_201_CREATED)
def create_avaliacao(avaliacao_data: AvaliacaoCreate):
    """Endpoint para cadastrar uma nova avaliação no banco de dados."""
    try:
        nova_avaliacao = avaliacao_repository.create_avalicao(avaliacao_data)
        return nova_avaliacao
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar Avaliação: {e}"
        )
    
@router.get("/avaliacao", response_model=List[AvaliacaoRead])
def get_all_avaliacoes():
    """Endpoint para listar todas as avaliações cadastradas."""
    return avaliacao_repository.get_all_avaliacoes()

@router.get("/avaliacao/{idavaliacao}", response_model=AvaliacaoRead)
def get_avaliacao_id(id: int):
    """Endpoint para listar uma avaliação específica por id."""
    return avaliacao_repository.get_avaliacao_by_id(id)

@router.get("/avaliacao/material/{id_material}", response_model=List[AvaliacaoRead])
def get_avaliacao_by_material(id: int):
    """Endpoint para listar avalições de uma material """
    return avaliacao_repository.get_avaliacao_by_material(id)
    
@router.patch("/avaliacao/{id_avaliacao}", response_model=AvaliacaoRead)
def update_avaliacao_by_id(id_avaliacao: int, update_data: AvaliacaoUpdate):
    """Endpoint para atualizar uma universidade específica."""
    return avaliacao_repository.update_avaliacao(id_avaliacao, update_data)

@router.delete("/avaliacao/{id_avaliacao}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avaliacao(id_avaliacao: int):
    """
    Endpoint para deletar uma avaliação específica.
    Retorna status 204 No Content se a avaliação for deletada com sucesso.
    """
    try:
        was_deleted = avaliacao_repository.delete_avaliacao(id_avaliacao)
        
        if not was_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Avaliação com ID {id_avaliacao} não encontrada."
            )
        return

    except Exception as e:
        if isinstance(e, HTTPException): 
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar avaliação: {e}"
        )