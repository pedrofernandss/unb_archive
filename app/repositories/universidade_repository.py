import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.universidade_schema import UniversidadeCreate, UniversidadeUpdate

def create_universidade(universidade: UniversidadeCreate):
    """
    Função para cadastrar universidades no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                INSERT INTO Universidade (nome, cidade, estado)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (universidade.nome, universidade.cidade, universidade.estado)
            )

            universidade_cadastrada = cur.fetchone()
            
            conn.commit()
        
            return universidade_cadastrada

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar universidade: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_universidades():
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
                FROM Universidade
                """
            )
            universidades = cur.fetchall()
            conn.commit()
            return universidades
    finally:
        if conn: 
            conn.close()

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

def update_universidade(ies: int, data: UniversidadeUpdate):
    """
    Atualiza uma universidade no banco de dados com.
    """
    update_data = data.model_dump(exclude_unset=True) #Transforma os dados recebidos em dicionário, para mapear o que será atualizado

    set_querie = [f"{key} = %s" for key in update_data.keys()]
    set_querie_str = ", ".join(set_querie)

    params_atualizacao_lista = list(update_data.values())
    params_atualizacao_lista.append(ies)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            query = f"""
                UPDATE Universidade
                SET {set_querie_str}
                WHERE ies = %s
                RETURNING *;       
            """

            cur.execute(query, tuple(params_atualizacao_lista))

            conn.commit()

            return cur.fetchone()
    finally:
        if conn:
            conn.close()
