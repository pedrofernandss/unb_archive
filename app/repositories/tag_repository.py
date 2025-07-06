import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.tag_schema import TagCreate, TagUpdate, TagRead

def create_tag(tag: TagCreate):
    """
    Função para cadastrar uma nova tag no banco de dados da aplicação.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Tag (nome_tag)
                VALUES (%s)
                RETURNING *;
                """,
                (tag.nome_tag,)
            )
            nova_tag = cur.fetchone()
            conn.commit()
            return nova_tag

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar tag: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_tags():
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * 
                FROM Tag
                """
            )
            tags = cur.fetchall()
            return tags
    finally:
        if conn:
            conn.close()

def update_tag(id_tag: int, data: TagUpdate):
    """
    Atualiza uma tag no banco de dados.
    """
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return None  # Nada para atualizar

    set_query = [f"{key} = %s" for key in update_data.keys()]
    set_query_str = ", ".join(set_query)

    params = list(update_data.values())
    params.append(id_tag)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            query = f"""
                UPDATE Tag
                SET {set_query_str}
                WHERE id_tag = %s
                RETURNING *;
            """
            cur.execute(query, tuple(params))
            conn.commit()
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def get_tag_by_id(id_tag: int):
    """
    Função para acessar TAG específica cadastrada no banco de dados, pelo número do id_tag
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Tag
                WHERE id_tag = %s;
                """,
                (id_tag,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()