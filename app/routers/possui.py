from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.possui_schema import PossuiRead, PossuiCreate, PossuiUpdate
from app.repositories import possui_repository

router = APIRouter()

@router.post("/possui", response_model=PossuiRead, status_code=status.HTTP_201_CREATED)
def create_possuir(possui_data: PossuiCreate):
    return possui_repository.create_possui(possui_data)

@router.get("/possui", response_model=List[PossuiRead])
def get_all_possuir():
    return possui_repository.get_all_possuir()

@router.get("/possui/{id_possui}", response_model=PossuiRead)
def get_possuir_id(id_possui: int):
    return possui_repository.get_possuir_by_id(id_possui)

@router.patch("/possui/{id_possui}", response_model=PossuiRead)
def update_possuir_by_id(id_possui: int, update_data: PossuiUpdate):
    result = possui_repository.update_possuir(id_possui, update_data)
    if not result:
        raise HTTPException(404, "Não encontrado.")
    return result

@router.delete("/possui/{id_possui}", status_code=status.HTTP_204_NO_CONTENT)
def delete_possuir(id_possui: int):
    was_deleted = possui_repository.delete_possuir(id_possui)
    if not was_deleted:
        raise HTTPException(404, "Não encontrado.")
    return
