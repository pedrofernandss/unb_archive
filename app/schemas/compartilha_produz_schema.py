from pydantic import BaseModel

class CompartilhaProduzBase(BaseModel):
    id_material: int
    cpf_usuario: str

class CompartilhaProduzCreate(CompartilhaProduzBase):
    pass

class CompartilhaProduzRead(CompartilhaProduzBase):
    pass
