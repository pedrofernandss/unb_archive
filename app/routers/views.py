from fastapi import APIRouter
from typing import List
from app.repositories import view_repository
from app.schemas.view_schema import MaterialCompleto

router = APIRouter()

@router.get("/relatorios/materiais-completos",response_model=List[MaterialCompleto],summary="Retorna um relatório completo de todos os materiais")
def get_relatorio_materiais():
    """
    Endpoint que consulta a VIEW vw_materiais_completos para retornar
    uma lista detalhada de cada material com suas informações agregadas,
    como média de notas, tags e usuários associados.
    """
    return view_repository.get_all_materiais_completos()