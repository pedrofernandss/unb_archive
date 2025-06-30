from fastapi import FastAPI
from app.routers import usuarios, universidade, avaliacao, avalia

app = FastAPI(
    title="UnB Archive API",
    description="API para o projeto acadêmico de gerenciamento de arquivos e documentos universitários",
    version="1.0.0"
)

app.include_router(
    usuarios.router, 
    prefix="/api/v1", 
    tags=["Usuários"]
)

app.include_router(
    universidade.router, 
    prefix="/api/v1", 
    tags=["Universidade"]
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

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint para verificar se a API está online."""
    return {"message": "Bem-vindo à UnB Archive API!"}