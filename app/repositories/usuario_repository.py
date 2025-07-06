import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import UsuarioCreate


def _create_base_user(cursor, user: UsuarioCreate):
    """
    Função base para cadastrar usuarios no banco de dados da aplicação
    """
    cursor.execute(
        """
        INSERT INTO Usuario (cpf, nome, senha, email, id_departamento, matricula)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (user.cpf, user.nome, user.senha, user.email,
         user.id_departamento, user.matricula)
    )


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
