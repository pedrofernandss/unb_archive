import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.reputacao_schema import ReputacaoCreate, ReputacaoUpdate 

def create_reputacao(reputacao: ReputacaoCreate):
    """
    Função para adicionar uma reputacao ao usuário no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                INSERT INTO Reputacao (pontuacao, nivel)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (reputacao.pontuacao, reputacao.nivel)
            )

            reputacao_cadastrada = cur.fetchone()
            
            conn.commit()
        
            return reputacao_cadastrada

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar Reputacao : {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_reputacoes():
    """
    Função para acessar todos os níveis de reputação cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Reputacao
                """
            )
            departamentos = cur.fetchall()
            conn.commit()
            return departamentos
    finally:
        if conn: 
            conn.close()

def update_reputacao(id: int, reputacao_data: ReputacaoUpdate):
    """
    Atualiza um departamento no banco de dados.
    """

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                UPDATE Reputacao
                SET nivel = %s
                WHERE id_reputacao = %s
                RETURNING *;
                """,
                (reputacao_data.nivel, id)
            )
            reputacao_atualizada = cur.fetchone()
            conn.commit()
            
            return reputacao_atualizada
    finally:
        if conn:
            conn.close()