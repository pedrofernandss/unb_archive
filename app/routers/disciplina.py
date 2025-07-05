from typing import List
from fastapi import APIRouter, HTTPException, status
from app.repositories import disciplina_repository
from app.schemas.disciplina_schema import DisciplinaRead, DisciplinaCreate, DisciplinaUpdate

router = APIRouter()

@router.post("/disciplina", response_model=DisciplinaRead, status_code=status.HTTP_201_CREATED)
def create_disciplina(disciplina_data: DisciplinaCreate):
    try:
        return disciplina_repository.create_disciplina(disciplina_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar disciplina: {str(e)}"
        )

@router.get("/disciplina", response_model=List[DisciplinaRead])
def get_all_disciplinas():
    return disciplina_repository.get_all_disciplinas()

@router.get("/disciplina/{codigo}", response_model=DisciplinaRead)
def get_disciplina_by_codigo(codigo: int):
    disciplina = disciplina_repository.get_disciplina_by_codigo(codigo)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    return disciplina

@router.patch("/disciplina/{codigo}", response_model=DisciplinaRead)
def update_disciplina(codigo: int, update_data: DisciplinaUpdate):
    try:
        return disciplina_repository.update_disciplina(codigo, update_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar disciplina: {str(e)}"
        )

@router.delete("/disciplina/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disciplina(codigo: int):
    disciplina_repository.delete_disciplina(codigo)
    return