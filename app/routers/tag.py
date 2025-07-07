from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.tag_schema import TagRead, TagCreate, TagUpdate
from app.repositories import tag_repository

router = APIRouter()

@router.post("/tag", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(tag_data: TagCreate):
    """Endpoint para cadastrar uma nova tag no banco de dados."""
    try:
        nova_tag = tag_repository.create_tag(tag_data)
        return nova_tag

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar tag: {e}"
        )

@router.get("/tag", response_model=List[TagRead])
def get_all_tags():
    return tag_repository.get_all_tags()


@router.get("/tag/{id_tag}", response_model=TagRead)
def get_tag_by_id(id_tag: int):
    """Endpoint para listar uma tag específica."""
    return tag_repository.get_tag_by_id(id_tag)

@router.patch("/tag/{id_tag}", response_model=TagRead)
def update_tag_by_id(id_tag: int, update_data: TagUpdate):
    """Endpoint para atualizar uma tag específica."""
    tag_atualizada = tag_repository.update_tag(id_tag, update_data)
    if not tag_atualizada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag não encontrada.")
    return tag_atualizada

@router.delete("/tag/{id_tag}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id_tag: int):
    result = tag_repository.delete_tag(id_tag)
    if not result:
        raise HTTPException(404, "Tag não encontrada para deletar.")
    return {"detail": "Tag deletada com sucesso"}
