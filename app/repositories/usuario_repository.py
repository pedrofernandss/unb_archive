from app.schemas.usuario_schema import UsuarioCreate

def _create_base_user(cursor, user: UsuarioCreate):
    """
    Função base para cadastrar usuarios no banco de dados da aplicação
    """
    cursor.execute(
        """
        INSERT INTO Usuario (cpf, nome, senha, email, idDepartamento, matricula)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (user.cpf, user.nome, user.senha, user.email, user.id_departamento, user.matricula)
    )