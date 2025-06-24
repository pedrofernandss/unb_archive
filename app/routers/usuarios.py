from fastapi import APIRouter, HTTPException, status

from app.schemas.usuario_schema import DiscenteCreate, DiscenteRead

from app.repositories import discente_repository


from typing import List

router = APIRouter()

@router.post("/usuarios/discente", response_model=DiscenteRead, status_code=status.HTTP_201_CREATED)
def create_discente(discente_data: DiscenteCreate):
    """Endpoint para cadastrar um novo discente no banco de dados."""
    try:
        novo_discente = discente_repository.create_discente(discente_data)
        return novo_discente
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Erro ao criar discente: {e}"
        )

@router.get("usuarios/discente", response_model=List[DiscenteRead])
def get_all_discentes():
    """Endpoint para listar todos os discentes cadastrados."""
    return discente_repository.get_all_discentes()