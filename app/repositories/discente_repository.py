import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import DiscenteCreate
from . import usuario_repository 

def create_discente(discente: DiscenteCreate):
    """
    Função para cadastrar discentes no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            usuario_repository._create_base_user(cur, discente)

            cur.execute(
                """
                INSERT INTO Discente (id_usuario_discente, ano_ingresso, status, coeficiente_rendimento)
                VALUES (%s, %s, %s, %s);
                """,
                (discente.cpf, discente.ano_ingresso, discente.status, discente.coeficiente_rendimento)
            )
            
            conn.commit()
        
            return discente

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar discente: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_discentes():
    """
    Função para acessar todos os discentes cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Usuario
                JOIN 
                    Discente ON Usuario.cpf = Discente.id_usuario_discente 
                """
            )
            conn.commit()
            return cur.fetchall()
    finally:
        if conn: 
            conn.close()

def get_discente_by_cpf(cpf: str):
    """
    Função para acessar Discente específico cadastrado no banco de dados, pelo número do CPF
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Usuario usuario
                JOIN Discente discente ON usuario.cpf = discente.id_usuario_discente
                WHERE usuario.cpf = %s;
                """,
                (cpf,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()