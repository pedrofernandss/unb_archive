from typing import List
from fastapi import APIRouter, HTTPException, status
from app.repositories import escolaridade_repository
from app.schemas.escolaridade_schema import EscolaridadeRead, EscolaridadeCreate, EscolaridadeUpdate

router = APIRouter()

@router.post("/escolaridade", response_model=EscolaridadeRead, status_code=status.HTTP_201_CREATED)
def create_escolaridade(escolaridade_data: EscolaridadeCreate):
    try:
        return escolaridade_repository.create_escolaridade(escolaridade_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar escolaridade: {str(e)}"
        )

@router.get("/escolaridade", response_model=List[EscolaridadeRead])
def get_all_escolaridades():
    return escolaridade_repository.get_all_escolaridades()

@router.get("/escolaridade/departamento/{departamento_id}", response_model=List[EscolaridadeRead])
def get_escolaridades_by_departamento(departamento_id: int):
    return escolaridade_repository.get_escolaridades_by_departamento(departamento_id)

@router.put("/escolaridade/{escolaridade_nome}/departamento/{departamento_id}", response_model=EscolaridadeRead)
def update_escolaridade(escolaridade_nome: str, departamento_id: int, escolaridade_data: EscolaridadeUpdate):
    try:
        return escolaridade_repository.update_escolaridade(escolaridade_nome, departamento_id, escolaridade_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar escolaridade: {str(e)}"
        )

@router.delete("/escolaridade/{escolaridade_nome}/departamento/{departamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escolaridade(escolaridade_nome: str, departamento_id: int):
    try:
        escolaridade_repository.delete_escolaridade(escolaridade_nome, departamento_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao deletar escolaridade: {str(e)}"
        )