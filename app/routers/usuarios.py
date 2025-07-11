from typing import List
from fastapi import APIRouter, HTTPException, status
from app.repositories import usuario_repository, discente_repository, docente_repository
from app.schemas.usuario_schema import UsuarioBase, DiscenteCreate, DiscenteRead, DiscenteUpdate, DocenteCreate, DocenteRead, DocenteUpdate, UsuarioUpdate

router = APIRouter()

@router.get("/usuarios", response_model=List[UsuarioBase])
def get_all_usuarios():
    """Endpoint para listar todos os usuários cadastrados, independente do tipo."""
    return usuario_repository.get_all_usuarios()

@router.get("/usuarios/{cpf}", response_model=UsuarioBase)
def get_usuario_by_cpf(cpf: str):
    """Endpoint para acessar um usuário cadastrado, independente do tipo."""
    usuario = usuario_repository.get_usuario_by_cpf(cpf)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return usuario

@router.post("/usuarios/discente", response_model=DiscenteRead, status_code=status.HTTP_201_CREATED)
def create_discente(discente_data: DiscenteCreate):
    """Endpoint para cadastrar um novo discente no banco de dados."""
    try:
        novo_discente = discente_repository.create_discente(discente_data)
        return novo_discente
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro ao criar discente: {e}")

@router.get("/usuarios/discente", response_model=List[DiscenteRead])
def get_all_discentes():
    """Endpoint para listar todos os discentes cadastrados."""
    return discente_repository.get_all_discentes()

# --- CORREÇÃO APLICADA AQUI ---
@router.get("/usuarios/discente/{cpf}", response_model=DiscenteRead)
def get_discente_by_cpf(cpf: str):
    """Endpoint para listar um discente específico do banco de dados."""
    discente_selecionado = discente_repository.get_discente_by_cpf(cpf)
    
    # Verifica se o discente foi encontrado. Se não, levanta um erro 404.
    if not discente_selecionado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Discente com CPF {cpf} não encontrado."
        )
    return discente_selecionado

@router.patch("/usuarios/discente/{cpf}", response_model=DiscenteRead)
def update_discente(cpf: str, discente_data: DiscenteUpdate):
    """Endpoint para atualizar informações de discente no banco de dados."""
    discente_atualizado = discente_repository.update_discente(cpf, discente_data)
    if not discente_atualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Discente com CPF {cpf} não encontrado.")
    return discente_atualizado
    
@router.post("/usuarios/docente", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
def create_docente(docente_data: DocenteCreate):
    """Endpoint para cadastrar um novo docente no banco de dados."""
    try:
        novo_docente = docente_repository.create_docente(docente_data)
        return novo_docente
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro ao criar docente: {e}")

@router.get("/usuarios/docente", response_model=List[DocenteRead])
def get_all_docentes():
    """Endpoint para listar todos os docentes cadastrados."""
    return docente_repository.get_all_docentes()

# --- CORREÇÃO APLICADA AQUI ---
@router.get("/usuarios/docente/{cpf}", response_model=DocenteRead)
def get_docente_by_cpf(cpf: str):
    """Endpoint para listar um docente específico do banco de dados."""
    docente_selecionado = docente_repository.get_docente_by_cpf(cpf)

    # Verifica se o docente foi encontrado. Se não, levanta um erro 404.
    if not docente_selecionado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Docente com CPF {cpf} não encontrado."
        )
    return docente_selecionado

@router.patch("/usuarios/docente/{cpf}", response_model=DocenteRead)
def update_docente(cpf: str, docente_data: DocenteUpdate):
    """Endpoint para atualizar informações de docente no banco de dados."""
    docente_atualizado = docente_repository.update_docente(cpf, docente_data)
    if not docente_atualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Docente com CPF {cpf} não encontrado.")
    return docente_atualizado

@router.patch("/usuarios/{cpf}", response_model=UsuarioBase)
def update_user(cpf: str, usuario_data: UsuarioUpdate):
    """Endpoint para atualizar um usuario"""
    usuario_atualizado = usuario_repository.update_by_cpf(cpf, usuario_data)
    if not usuario_atualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com CPF {cpf} não encontrado.")
    return usuario_atualizado

@router.delete("/usuarios/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_and_dependencies(cpf: str):
    """Endpoint para deletar um usuário e todas as suas dependências"""
    deleted_count = usuario_repository.delete_by_cpf(cpf)
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com CPF {cpf} não encontrado.")
    return
