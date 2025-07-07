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
                INSERT INTO avalia (iddocente, idmaterial, valido)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (avalia.iddocente, avalia.idmaterial, avalia.valido)
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

def get_avalia_by_docente(iddocente: str):
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
                WHERE Avalia.iddocente = %s;
                """,
                (iddocente,)
            )
            return cur.fetchall()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por docente: {e}")
        raise
    finally:
        if conn: 
            conn.close()

def get_avalia_by_material(idmaterial: int):
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
                WHERE Avalia.idmaterial = %s;
                """,
                (idmaterial,)
            )
            return cur.fetchall()
    except psycopg.Error as e:
        print(f"Erro ao buscar avaliações por material: {e}")
        raise
    finally:
        if conn: 
            conn.close()

def update_avalia(iddocente: str, idmaterial: int, data: AvaliaUpdate):
    """Atualiza uma avaliacao no banco de dados."""
    update_data = data.model_dump(exclude_unset=True)

    # Remove os identificadores para não tentar atualizá-los
    update_data.pop('iddocente', None)
    update_data.pop('idmaterial', None)

    if not update_data:
        return None 

    set_clauses = [f"{key} = %s" for key in update_data.keys()]
    query_str = ", ".join(set_clauses)

    params = list(update_data.values()) + [iddocente, idmaterial]

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            query = f"""
                UPDATE Avalia
                SET {query_str}
                WHERE iddocente = %s AND idmaterial = %s
                RETURNING *;       
            """
            cur.execute(query, tuple(params))
            conn.commit()
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def delete_avalia(iddocente: str, idmaterial: int) -> bool:
    """Deleta uma avaliação do banco de dados usando a chave composta."""
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                DELETE FROM Avalia
                WHERE iddocente = %s AND idmaterial = %s
                RETURNING iddocente; 
                """,
                (iddocente, idmaterial)
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