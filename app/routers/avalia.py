from fastapi import APIRouter, HTTPException, status

from app.schemas.avalia_schema import AvaliaRead, AvaliaCreate, AvaliaUpdate

from app.repositories import avalia_repository


from typing import List

router = APIRouter()


@router.post("/avalia", response_model=AvaliaRead, status_code=status.HTTP_201_CREATED)
def create_avaliacao(avalia_data: AvaliaCreate):
    """Endpoint para cadastrar uma nova validação no banco de dados."""
    try:
        nova_avalia = avalia_repository.create_avalia(avalia_data)
        return nova_avalia

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar Avalia: {e}"
        )


@router.get("/avalia", response_model=List[AvaliaRead])
def get_all_avalias():
    """Endpoint para listar todas as validações cadastradas."""
    return avalia_repository.get_all_avalias()


@router.get("/avalia/docente/{id_docente}", response_model=List[AvaliaRead])
def get_avalia_by_docente(id_docente: str):
    """Endpoint para listar uma validação específica por docente."""
    return avalia_repository.get_avalia_by_docente(id_docente)


@router.get("/avalia/material/{id_material}", response_model=List[AvaliaRead])
def get_avalia_by_material(id_material: int):
    """Endpoint para listar uma validação específica por material."""
    return avalia_repository.get_avalia_by_material(id_material)


@router.patch("/avalia/docente/{id_docente}/material/{id_material}", response_model=AvaliaRead)
def update_avalia(id_docente: str, id_material: int, update_data: AvaliaUpdate):
    """Endpoint para atualizar uma validação específica."""
    updated = avalia_repository.update_avalia(
        id_docente, id_material, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validação não encontrada."
        )
    return updated


@router.delete("/avalia/docente/{id_docente}/material/{id_material}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avalia(id_docente: str, id_material: int):
    """Endpoint para deletar uma validação específica."""
    was_deleted = avalia_repository.delete_avalia(id_docente, id_material)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validação não encontrada para exclusão."
        )
    return
