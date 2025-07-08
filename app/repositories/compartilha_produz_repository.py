import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.compartilha_produz_schema import CompartilhaProduzCreate

def create_associacao(associacao: CompartilhaProduzCreate):
    """
    Cria uma nova associação entre um usuário e um material no banco de dados.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Compartilha_Produz (id_material, cpf_usuario)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (associacao.id_material, associacao.cpf_usuario)
            )
            nova_associacao = cur.fetchone()
            conn.commit()
            return nova_associacao
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_associacoes_by_material(id_material: int):
    """
    Busca todas as associações para um determinado material (quem compartilhou).
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Compartilha_Produz WHERE id_material = %s",
                (id_material,)
            )
            return cur.fetchall()
    finally:
        if conn:
            conn.close()

def get_associacoes_by_usuario(cpf_usuario: str):
    """
    Busca todas as associações para um determinado usuário (o que ele compartilhou).
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Compartilha_Produz WHERE cpf_usuario = %s",
                (cpf_usuario,)
            )
            return cur.fetchall()
    finally:
        if conn:
            conn.close()

def delete_associacao(id_material: int, cpf_usuario: str) -> bool:
    """
    Deleta uma associação específica usando a chave primária composta.
    Retorna True se a exclusão foi bem-sucedida, False caso contrário.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM Compartilha_Produz 
                WHERE id_material = %s AND cpf_usuario = %s
                """,
                (id_material, cpf_usuario)
            )

            deleted_count = cur.rowcount
            conn.commit()
            return deleted_count > 0
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()