from fastapi import APIRouter, HTTPException, status

from app.schemas.avalia_schema import AvaliaRead, AvaliaCreate, AvaliaUpdate

from app.repositories import avalia_repository


from typing import List

router = APIRouter()


@router.post("/avalia", response_model=AvaliaRead, status_code=status.HTTP_201_CREATED)
def create_avaliacao(avalia_data: AvaliaCreate):
    """Endpoint para cadastrar uma nova avalia no banco de dados."""
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
    """Endpoint para listar todas as universidades cadastradas."""
    return avalia_repository.get_all_avalias()


@router.get("/avalia/id/{id_avalia}", response_model=AvaliaRead)
def get_avalia_id(id_avalia: int):
    """Endpoint para listar uma avalia específica."""
    return avalia_repository.get_avalia_by_id(id_avalia)


@router.get("/avalia/docente/{id_docente}", response_model=List[AvaliaRead])
def get_avalia_by_docente(id_docente: str):
    """Endpoint para listar uma avalia específica."""
    return avalia_repository.get_avalia_by_docente(id_docente)


@router.get("/avalia/material/{id_material}", response_model=List[AvaliaRead])
def get_avalia_by_material(id_material: int):
    """Endpoint para listar uma avalia específica."""
    return avalia_repository.get_avalia_by_material(id_material)


@router.patch("/avalia/{id_avalia}", response_model=AvaliaRead)
def update_avalia_by_id(id_avalia: int, update_data: AvaliaUpdate):
    """Endpoint para atualizar uma universidade específica."""
    return avalia_repository.update_avalia(id_avalia, update_data)


@router.delete("/avalia/{id_avalia}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avalia(id_avalia: int):
    """
    Endpoint para deletar uma avaliação específica.
    Retorna status 204 No Content se a avaliação for deletada com sucesso.
    """
    try:
        was_deleted = avalia_repository.delete_avalia(id_avalia)

        if not was_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Avaliação com ID {id_avalia} não encontrada."
            )
        return

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar avaliação: {e}"
        )
