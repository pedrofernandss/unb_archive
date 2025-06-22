from fastapi import APIRouter, HTTPException, status

from app.schemas.universidade_schema import UniversidadeRead, UniversidadeCreate, UniversidadeUpdate

from app.repositories import universidade_repository


from typing import List

router = APIRouter()

@router.post("/universidade", response_model=UniversidadeRead, status_code=status.HTTP_201_CREATED)
def create_universidade(universidade_data: UniversidadeCreate):
    """Endpoint para cadastrar uma nova universidade no banco de dados."""
    try:
        nova_universidade = universidade_repository.create_universidade(universidade_data)
        return nova_universidade
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar universidade: {e}"
        )

@router.get("/universidade", response_model=List[UniversidadeRead])
def get_all_universidades():
    """Endpoint para listar todas as universidades cadastradas."""
    return universidade_repository.get_all_universidades()

@router.get("/universidade/{ies}", response_model=UniversidadeRead)
def get_universidade_by_ies(ies: int):
    """Endpoint para listar uma universidade específica."""
    return universidade_repository.get_universidade_by_ies(ies)

@router.patch("/universidade/{ies}", response_model=UniversidadeRead)
def update_universidade_by_ies(ies: int, update_data: UniversidadeUpdate):
    """Endpoint para atualizar uma universidade específica."""
    return universidade_repository.update_universidade(ies, update_data)