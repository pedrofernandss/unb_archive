import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.avaliacao_schema import AvaliacaoCreate, AvaliacaoUpdate


def create_avalicao(avaliacao: AvaliacaoCreate):
    """
    Função para cadastrar avaliacoes no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                INSERT INTO avaliacao (data_avaliacao, nota, id_material)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (avaliacao.data_avaliacao, avaliacao.nota, avaliacao.id_material)
            )

            avalicao_cadastrada = cur.fetchone()

            conn.commit()

            return avalicao_cadastrada

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar avalição: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_all_avaliacoes():
    """
    Função para acessar todas as avaliações cadastradas no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Avaliacao
                """
            )
            avaliacoes = cur.fetchall()
            conn.commit()
            return avaliacoes
    finally:
        if conn:
            conn.close()


def get_avaliacao_by_id(id_avaliacao: int):
    """
    Função para acessar a avaliçao por id 
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Avaliacao
                WHERE Avaliacao.id_avaliacao = %s;
                """,
                (id_avaliacao,)
            )

            return cur.fetchone()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por id: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_avaliacao_by_material(id_material: int):
    """
    Função para acessar a avaliação por material
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *
                FROM Avaliacao A
                INNER JOIN Material M
                ON A.id_material = M.id_material
                WHERE M.id_material = %s;
                """,
                (id_material,)
            )
            return cur.fetchall()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por docente: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_avaliacao(id_avaliacao: int, data: AvaliacaoUpdate):
    """
    Atualiza uma avaliacao no banco de dados
    """
    update_data = data.model_dump(exclude_unset=True)

    set_querie = [f"{key} = %s" for key in update_data.keys()]
    set_querie_str = ", ".join(set_querie)

    params_atualizacao_lista = list(update_data.values())
    params_atualizacao_lista.append(id_avaliacao)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            query = f"""
                UPDATE Avaliacao
                SET {set_querie_str}
                WHERE id_avaliacao = %s
                RETURNING *;       
            """

            cur.execute(query, tuple(params_atualizacao_lista))

            conn.commit()

            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def delete_avaliacao(id_avaliacao: int) -> bool:
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
                DELETE FROM Avaliacao
                WHERE id_avaliacao = %s
                RETURNING id_avaliacao; 
                """,
                (id_avaliacao,)
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
