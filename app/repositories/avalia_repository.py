import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.avalia_schema import AvaliaCreate, AvaliaUpdate


def create_avalia(avalia: AvaliaCreate):
    """
    Função para cadastrar avaliacoes no banco de dados da aplicação
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
    Função para acessar todas as universidades cadastradas no banco de dados da aplicação
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


def get_avalia_by_id(id_avalia: int):
    """
    Função para acessar a avalia por id 
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Avalia
                WHERE Avalia.id_avalia = %s;
                """,
                (id_avalia,)
            )

            return cur.fetchone()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por id: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_avalia_by_docente(id_docente: str):
    """
    Função para acessar a avalia por docente
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
    Função para acessar a avalia por docente
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


def update_avalia(id_avalia: int, data: AvaliaUpdate):
    """
    Atualiza uma avaliacao no banco de dados com.
    """
    update_data = data.model_dump(
        # Transforma os dados recebidos em dicionário, para mapear o que será atualizado
        exclude_unset=True)

    set_querie = [f"{key} = %s" for key in update_data.keys()]
    set_querie_str = ", ".join(set_querie)

    params_atualizacao_lista = list(update_data.values())
    params_atualizacao_lista.append(id_avalia)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            query = f"""
                UPDATE Avalia
                SET {set_querie_str}
                WHERE id_avalia = %s
                RETURNING *;       
            """

            cur.execute(query, tuple(params_atualizacao_lista))

            conn.commit()

            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def delete_avalia(id_avalia: int) -> bool:
    conn = None
    """
    Função para deletar uma avaliação do banco de dados.
    Retorna True se a avaliação foi deletada, False caso contrário.
    """
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                DELETE FROM Avalia
                WHERE id_avalia = %s
                RETURNING id_avalia; 
                """,
                (id_avalia,)
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
