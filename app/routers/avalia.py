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
    """Endpoint para listar todas as avalias cadastradas."""
    return avalia_repository.get_all_avalias()

@router.get("/avalia/docente/{iddocente}", response_model=List[AvaliaRead])
def get_avalia_by_docente(iddocente: str):
    """Endpoint para listar uma avalia específica por docente."""
    return avalia_repository.get_avalia_by_docente(iddocente)

@router.get("/avalia/material/{idmaterial}", response_model=List[AvaliaRead])
def get_avalia_by_material(idmaterial: int):
    """Endpoint para listar uma avalia específica por material."""
    return avalia_repository.get_avalia_by_material(idmaterial)

@router.patch("/avalia/docente/{iddocente}/material/{idmaterial}", response_model=AvaliaRead)
def update_avalia(iddocente: str, idmaterial: int, update_data: AvaliaUpdate):
    """Endpoint para atualizar uma validação específica."""
    updated = avalia_repository.update_avalia(iddocente, idmaterial, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validação não encontrada."
        )
    return updated

@router.delete("/avalia/docente/{iddocente}/material/{idmaterial}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avalia(iddocente: str, idmaterial: int):
    """Endpoint para deletar uma validação específica."""
    was_deleted = avalia_repository.delete_avalia(iddocente, idmaterial)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Validação não encontrada para exclusão."
        )
    return