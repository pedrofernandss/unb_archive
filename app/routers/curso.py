from typing import List
from fastapi import APIRouter, HTTPException, status
from app.repositories import curso_repository
from app.schemas.curso_schema import CursoRead, CursoCreate

router = APIRouter()

@router.post("/curso", response_model=CursoRead, status_code=status.HTTP_201_CREATED)
def create_curso(curso_data: CursoCreate):
    try:
        return curso_repository.create_curso(curso_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar curso: {str(e)}"
        )

@router.get("/curso", response_model=List[CursoRead])
def get_all_cursos():
    return curso_repository.get_all_cursos()

@router.get("/curso/departamento/{departamento_id}", response_model=List[CursoRead])
def get_cursos_by_departamento(departamento_id: int):
    return curso_repository.get_cursos_by_departamento(departamento_id)