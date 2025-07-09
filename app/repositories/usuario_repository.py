import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate


def _create_base_user(cursor, user: UsuarioCreate):
    """
    Função base para cadastrar usuarios no banco de dados da aplicação
    """
    cursor.execute(
        """
        INSERT INTO Usuario (cpf, nome, senha, email, id_universidade, id_departamento, matricula)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (user.cpf, user.nome, user.senha, user.email, user.id_universidade,
         user.id_departamento, user.matricula)
    )

def get_usuario_by_cpf(cpf: str):
    """
    Função para acessar um usuario cadastrado no banco de dados da aplicação, independente do tipo.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Usuario
                WHERE usuario.cpf = %s;
                """,
                (cpf,)
            )
            usuario = cur.fetchone()
            conn.commit()
            
            return usuario
    finally:
        if conn:
            conn.close()

def get_all_usuarios():
    """
    Função para acessar todos os usuários cadastrados no banco de dados da aplicação, independente do tipo.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Usuario
                """
            )
            todos_usuarios = cur.fetchall()
            conn.commit()
            return todos_usuarios
    finally:
        if conn:
            conn.close()

def update_by_cpf(cpf: str, data: UsuarioUpdate):
    """
    Atualiza a tabela Usuario com base nos dados fornecidos.
    A query SQL é montada dinamicamente para uma atualização parcial.
    """
    update_data = data.model_dump(exclude_unset=True)

    set_clauses = [f"{key} = %s" for key in update_data.keys()]
    set_clause_str = ", ".join(set_clauses)

    params = list(update_data.values())
    params.append(cpf)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            query = f"""
                UPDATE Usuario
                SET {set_clause_str}
                WHERE cpf = %s;
            """
            
            cur.execute(query, tuple(params))
            conn.commit()
            
            return get_usuario_by_cpf(cpf)
            
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar usuário: {e}")
        raise
    finally:
        if conn:
            conn.close()

def delete_by_cpf(cpf: str) -> int:
    """
    Deleta um Usuario e todos os seus registros dependentes (Discente, Docente, etc.)
    dentro de uma única transação.
    Retorna o número de usuários deletados da tabela principal (0 ou 1).
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:

            cur.execute("DELETE FROM Compartilha_Produz WHERE id_docente = %s;", (cpf,))
            cur.execute("DELETE FROM Avalia WHERE id_docente = %s;", (cpf,))

            cur.execute(
                "DELETE FROM Discente WHERE id_usuario = %s;", (cpf,))
            cur.execute(
                "DELETE FROM Docente WHERE id_usuario = %s;", (cpf,))

            cur.execute("DELETE FROM Usuario WHERE cpf = %s;", (cpf,))

            linhas_deletadas = cur.rowcount

            conn.commit()

            return linhas_deletadas

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao deletar usuário: {e}")
        raise
    finally:
        if conn:
            conn.close()
