from fastapi import FastAPI
from app.routers import disciplina, curso, escolaridade, reputacao, usuarios, universidade, departamento, avaliacao, avalia
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="UnB Archive API",
    description="API para o projeto acadêmico de gerenciamento de arquivos e documentos universitários",
    version="1.0.0"
)

app.include_router(
    universidade.router, 
    prefix="/api/v1", 
    tags=["Universidade"]
)

app.include_router(
    departamento.router, 
    prefix="/api/v1", 
    tags=["Departamento"]
)

app.include_router(
    usuarios.router, 
    prefix="/api/v1", 
    tags=["Usuários"]
)

app.include_router(
    reputacao.router, 
    prefix="/api/v1", 
    tags=["Reputação"]
)

app.include_router(
    disciplina.router,
    prefix="/api/v1",
    tags=["Disciplina"]
)

app.include_router(
    avaliacao.router, 
    prefix="/api/v1", 
    tags=["Avaliação"]
)

app.include_router(
    avalia.router, 
    prefix="/api/v1", 
    tags=["Avalia"]
)

app.include_router(
    curso.router,
    prefix="/api/v1",
    tags=["Curso"]
)

app.include_router(
    escolaridade.router,
    prefix="/api/v1",
    tags=["Escolaridade"]
)

app.mount("/", StaticFiles(directory=".", html=True), name="static")

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint para verificar se a API está online."""
    return {"message": "Bem-vindo à UnB Archive API!"}