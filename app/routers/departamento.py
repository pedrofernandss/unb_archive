from typing import List
from fastapi import APIRouter, HTTPException, status

from app.schemas.departamento_schema import DepartamentoRead, DepartamentoCreate, DepartamentoUpdate

from app.repositories import departamento_repository

router = APIRouter()

@router.post("/departamento", response_model=DepartamentoRead, status_code=status.HTTP_201_CREATED)
def create_departamento(departamento_data: DepartamentoCreate):
    """Endpoint para cadastrar um novo departamento no banco de dados."""
    try:
        novo_departamento = departamento_repository.create_departamento(departamento_data)
        return novo_departamento
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar universidade: {e}"
        )

@router.get("/departamento", response_model=List[DepartamentoRead])
def get_all_departamento():
    """Endpoint para listar todos os departamentos cadastrados."""
    return departamento_repository.get_all_departamentos()

@router.get("/departamento/universidade/{ies}", response_model=DepartamentoRead)
def get_departamento_by_ies(ies: int):
    """Endpoint para listar todos os departamentos de uma universidade em específico."""
    return departamento_repository.get_ies_departamentos(ies)

@router.get("/departamento/{id}", response_model=DepartamentoRead)
def get_departamento_by_id(id: int):
    """Endpoint para listar um departamento específico."""
    return departamento_repository.get_departamento_by_id(id)

@router.patch("/departamento/{id}", response_model=DepartamentoRead)
def update_departamento_by_id(id: int, update_data: DepartamentoUpdate):
    """Endpoint para atualizar uma universidade específica."""
    return departamento_repository.update_departamento(id, update_data)