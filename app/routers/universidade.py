from typing import List
from fastapi import APIRouter, status
from app.repositories import universidade_repository
from app.schemas.universidade_schema import UniversidadeRead, UniversidadeCreate, UniversidadeUpdate

router = APIRouter()

@router.post("/universidade", response_model=UniversidadeRead, status_code=status.HTTP_201_CREATED)
def create_universidade(universidade_data: UniversidadeCreate):
    """Endpoint para cadastrar uma nova universidade no banco de dados."""
    return universidade_repository.create_universidade(universidade_data)

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