from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.compartilha_produz_schema import CompartilhaProduzRead, CompartilhaProduzCreate
from app.repositories import compartilha_produz_repository

router = APIRouter()

@router.post("/associacoes", response_model=CompartilhaProduzRead, status_code=status.HTTP_201_CREATED,summary="Cria uma nova associação usuário-material")
def create_associacao(associacao_data: CompartilhaProduzCreate):
    """
    Cria uma nova associação para registrar que um usuário 
    (discente ou docente) compartilhou um material.
    """
    try:
        nova_associacao = compartilha_produz_repository.create_associacao(associacao_data)
        return nova_associacao
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Não foi possível criar a associação. O usuário já pode ter compartilhado este material. Erro: {e}"
        )

@router.get("/associacoes/usuario/{cpf_usuario}", response_model=List[CompartilhaProduzRead],summary="Busca todos os materiais compartilhados por um usuário")
def get_associacoes_por_usuario(cpf_usuario: str):
    """
    Retorna uma lista de todos os materiais que um usuário específico compartilhou.
    """
    return compartilha_produz_repository.get_associacoes_by_usuario(cpf_usuario)

@router.get("/associacoes/material/{id_material}",response_model=List[CompartilhaProduzRead],summary="Busca todos os usuários que compartilharam um material")
def get_associacoes_por_material(id_material: int):
    """
    Retorna uma lista de todos os usuários que compartilharam um material específico.
    """
    return compartilha_produz_repository.get_associacoes_by_material(id_material)

@router.delete("/associacoes/material/{id_material}/usuario/{cpf_usuario}",status_code=status.HTTP_204_NO_CONTENT,summary="Deleta uma associação usuário-material")
def delete_associacao(id_material: int, cpf_usuario: str):
    """
    Deleta a associação entre um usuário e um material, efetivamente
    "desfazendo" o compartilhamento.
    """
    was_deleted = compartilha_produz_repository.delete_associacao(id_material, cpf_usuario)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação não encontrada para exclusão."
        )
    return