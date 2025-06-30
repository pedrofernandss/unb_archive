from fastapi import APIRouter, HTTPException, status

from app.schemas.avaliacao_schema import AvaliacaoRead, AvaliacaoCreate, AvaliacaoUpdate

from app.repositories import avaliacao_repository


from typing import List

router = APIRouter()

@router.post("/avaliacao", response_model=AvaliacaoRead, status_code=status.HTTP_201_CREATED)
def create_avaliacao(avaliacao_data: AvaliacaoCreate):
    """Endpoint para cadastrar uma nova universidade no banco de dados."""
    try:
        nova_avaliacao = avaliacao_repository.create_avalicao(avaliacao_data)
        return nova_avaliacao
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar Avaliação: {e}"
        )
    
@router.patch("/avaliacao/{id_avaliacao}", response_model=AvaliacaoRead)
def update_avaliacao_by_id(id_avaliacao: int, update_data: AvaliacaoUpdate):
    """Endpoint para atualizar uma universidade específica."""
    return avaliacao_repository.update_avaliacao(id_avaliacao, update_data)
'''
@router.get("/universidade", response_model=List[UniversidadeRead])
def get_all_universidades():
    """Endpoint para listar todas as universidades cadastradas."""
    return universidade_repository.get_all_universidades()

@router.get("/universidade/{ies}", response_model=UniversidadeRead)
def get_universidade_by_ies(ies: int):
    """Endpoint para listar uma universidade específica."""
    return universidade_repository.get_universidade_by_ies(ies)
    '''