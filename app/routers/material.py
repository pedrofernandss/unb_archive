from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import List
from app.schemas.material_schema import MaterialCreate, MaterialRead, MaterialUpdate
from app.repositories import material_repository
import io

router = APIRouter(
    prefix="/material",
    tags=["Material"], 
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MaterialRead)
async def create_material(
    nome: str = Form(...),
    descricao: str = Form(...),
    ano_semestre_ref: str = Form(...),
    arquivo: UploadFile = File(...),
    id_disciplina: int = Form(...)
):
    try:
        conteudo_pdf = await arquivo.read()

        novo_material = material_repository.create_material(
            nome=nome,
            descricao=descricao,
            ano_semestre_ref=ano_semestre_ref,
            local_arquivo=conteudo_pdf,
            id_disciplina=id_disciplina
        )

        return novo_material

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erro ao criar material: {e}")


@router.get("/", response_model=List[MaterialRead])
def get_all_materiais():
    return material_repository.get_all_materiais()


@router.get("/{id_material}", response_model=MaterialRead)
def get_by_id(id_material: int):
    result = material_repository.get_material_by_id(id_material)
    if not result:
        raise HTTPException(404, "Material não encontrado.")
    return result

@router.get("/{id_material}/download")
def download_pdf(id_material: int):
    material = material_repository.get_material_by_id(id_material)
    if not material or not material.get("local_arquivo"):
        raise HTTPException(status_code=404, detail="PDF não encontrado.")

    pdf_bytes = material["local_arquivo"]

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=material_{id_material}.pdf"}
    )


@router.put("/{id_material}", response_model=MaterialRead)
def update(id_material: int, data: MaterialUpdate):
    result = material_repository.update_material(id_material, data)
    if not result:
        raise HTTPException(404, "Nada atualizado.")
    return result


@router.delete("/{id_material}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id_material: int):
    result = material_repository.delete_material(id_material)
    if not result:
        raise HTTPException(404, "Material não encontrado para deletar.")
    return {"detail": "Material deletado com sucesso"}
