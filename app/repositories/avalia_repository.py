import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.avalia_schema import AvaliaCreate, AvaliaUpdate


def create_avalia(avalia: AvaliaCreate):
    """
    Função para cadastrar validações no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                INSERT INTO avalia (id_docente, id_material, valido)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (avalia.id_docente, avalia.id_material, avalia.valido)
            )

            avalia_cadastrada = cur.fetchone()

            conn.commit()

            return avalia_cadastrada

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar avalição: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_all_avalias():
    """
    Função para acessar todas as validações cadastradas no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Avalia
                """
            )
            avalias = cur.fetchall()
            conn.commit()
            return avalias
    finally:
        if conn:
            conn.close()


def get_avalia_by_docente(id_docente: str):
    """
    Função para acessar a validação por docente
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Avalia
                WHERE Avalia.id_docente = %s;
                """,
                (id_docente,)
            )
            return cur.fetchall()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por docente: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_avalia_by_material(id_material: int):
    """
    Função para acessar a validação por material
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Avalia
                WHERE Avalia.id_material = %s;
                """,
                (id_material,)
            )
            return cur.fetchall()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por material: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_avalia(id_docente: str, id_material: int, data: AvaliaUpdate):
    """Atualiza uma validação no banco de dados."""
    update_data = data.model_dump(exclude_unset=True)

    update_data.pop('id_docente', None)
    update_data.pop('id_material', None)

    if not update_data:
        return None

    set_clauses = [f"{key} = %s" for key in update_data.keys()]
    query_str = ", ".join(set_clauses)

    params = list(update_data.values()) + [id_docente, id_material]

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            query = f"""
                UPDATE Avalia
                SET {query_str}
                WHERE id_docente = %s AND id_material = %s
                RETURNING *;       
            """
            cur.execute(query, tuple(params))
            conn.commit()
            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def delete_avalia(id_docente: str, id_material: int) -> bool:
    """Deleta uma validação do banco de dados usando a chave composta."""
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                DELETE FROM Avalia
                WHERE id_docente = %s AND id_material = %s
                RETURNING id_docente; 
                """,
                (id_docente, id_material)
            )
            deleted_record = cur.fetchone()
            conn.commit()
            return deleted_record is not None
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao deletar avaliação: {e}")
        raise
    finally:
        if conn:
            conn.close()
