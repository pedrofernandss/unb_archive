from typing import List
from fastapi import APIRouter, HTTPException, status
from app.repositories import reputacao_repository
from app.schemas.reputacao_schema import ReputacaoCreate, ReputacaoRead, ReputacaoUpdate

router = APIRouter()

@router.post("/reputacao", response_model=ReputacaoRead)
def create_reputacao(reputacao_data: ReputacaoCreate):
    """Endpoint para cadastrar um novo departamento no banco de dados."""
    return reputacao_repository.create_reputacao(reputacao_data)

@router.get("/reputacao", response_model=List[ReputacaoRead])
def get_all_reputacoes():
    """Endpoint para listar todos os níveis de reputacao disponíveis."""
    return reputacao_repository.get_all_reputacoes()

@router.patch("/reputacao/{id}", response_model=ReputacaoRead)
def update_reputacao_by_id(id: int, update_data: ReputacaoUpdate):
    """Endpoint para atualizar uma reputação específica."""
    return reputacao_repository.update_reputacao(id, update_data)