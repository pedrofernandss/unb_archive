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
                INSERT INTO avaliacao (data_avaliacao, nota, idMaterial)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (avaliacao.data_avaliacao, avaliacao.nota, avaliacao.idmaterial)
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
    Função para acessar todas as universidades cadastradas no banco de dados da aplicação
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
def update_avaliacao(id_avaliacao: int, data: AvaliacaoUpdate):
    """
    Atualiza uma avaliacao no banco de dados com.
    """
    update_data = data.model_dump(exclude_unset=True) #Transforma os dados recebidos em dicionário, para mapear o que será atualizado

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
