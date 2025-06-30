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

def update_avalia(id_avalia: int, data: AvaliaUpdate):
    """
    Atualiza uma avaliacao no banco de dados com.
    """
    update_data = data.model_dump(exclude_unset=True) #Transforma os dados recebidos em dicionário, para mapear o que será atualizado

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

'''
def get_universidade_by_ies(ies: int):
    """
    Função para acessar Universidade específica cadastrada no banco de dados, pelo número do IES
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Universidade
                WHERE Universidade.ies = %s;
                """,
                (ies,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()
'''
