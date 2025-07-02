from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.material_schema import (
    MaterialCreate, MaterialRead, MaterialUpdate,
)
from app.repositories import material_repository

router = APIRouter()

@router.post("/material", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material(material: MaterialCreate):
    result = material_repository.create_material(material)
    if not result:
        raise HTTPException(400, "Erro ao criar material.")
    return result

@router.get("/", response_model=List[MaterialRead])
def get_all():
    return material_repository.get_all_material()

@router.get("/{id_material}", response_model=MaterialRead)
def get_by_id(id_material: int):
    result = material_repository.get_material_by_id(id_material)
    if not result:
        raise HTTPException(404, "Material não encontrado.")
    return result

@router.put("/{id_material}", response_model=MaterialRead)
def update(id_material: int, data: MaterialUpdate):
    result = material_repository.update_material(id_material, data)
    if not result:
        raise HTTPException(404, "Nada atualizado.")
    return result

@router.delete("/{id_material}", response_model=MaterialRead)
def delete(id_material: int):
    result = material_repository.delete_material(id_material)
    if not result:
        raise HTTPException(404, "Material não encontrado para deletar.")
    return result

