from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.possui_schema import PossuiCreate, PossuiRead
from app.repositories import possui_repository

router = APIRouter()

@router.post("/possui", response_model=PossuiRead, status_code=status.HTTP_201_CREATED)
def create_possui(possui_data: PossuiCreate):
    return possui_repository.create_possui(possui_data)

@router.delete("/possui", status_code=status.HTTP_204_NO_CONTENT)
def delete_possui(id_material: int, id_tag: int):
    deleted = possui_repository.delete_possui(id_material, id_tag)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado.")
    return

@router.get("/material/{id_material}/tags", response_model=List[dict])
def get_tags_by_material(id_material: int):
    return possui_repository.get_tags_by_material(id_material)

@router.get("/tag/{id_tag}/materiais", response_model=List[dict])
def get_materiais_by_tag(id_tag: int):
    return possui_repository.get_materiais_by_tag(id_tag)
