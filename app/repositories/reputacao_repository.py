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
            cur.execute("SELECT * FROM Reputacao")
            return cur.fetchall()
    finally:
        if conn: 
            conn.close()

# MUDANÇA: Nova função para buscar reputação pelo CPF do discente
def get_reputacao_by_cpf(cpf: str):
    """
    Busca a reputação de um discente específico pelo seu CPF.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT r.* FROM Reputacao r
                JOIN Discente d ON r.id_reputacao = d.id_reputacao
                WHERE d.id_usuario_discente = %s;
                """,
                (cpf,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def update_reputacao(id: int, reputacao_data: ReputacaoUpdate):
    """
    Atualiza uma reputação no banco de dados.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE Reputacao
                SET pontuacao = %s, nivel = %s
                WHERE id_reputacao = %s
                RETURNING *;
                """,
                (reputacao_data.pontuacao, reputacao_data.nivel, id)
            )
            reputacao_atualizada = cur.fetchone()
            conn.commit()
            return reputacao_atualizada
    finally:
        if conn:
            conn.close()

def delete_reputation_by_cpf(cpf: str) -> int:
    """
    Deleta a Reputacao associada a um Discente específico.
    """
    # Esta função pode ser otimizada, mas mantida por enquanto
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id_reputacao FROM Discente WHERE id_usuario_discente = %s;",
                (cpf,)
            )
            linha_reputacao = cur.fetchone()
            
            if not linha_reputacao or not linha_reputacao['id_reputacao']:
                return 0

            id_reputacao_alvo = linha_reputacao['id_reputacao']

            cur.execute(
                "UPDATE Discente SET id_reputacao = NULL WHERE id_usuario_discente = %s;",
                (cpf,)
            )
            
            cur.execute(
                "DELETE FROM Reputacao WHERE id_reputacao = %s;",
                (id_reputacao_alvo,)
            )
            
            linha_deletada = cur.rowcount
            conn.commit()
            return linha_deletada
    finally:
        if conn:
            conn.close()
