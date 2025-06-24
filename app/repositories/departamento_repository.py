import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.departamento_schema import DepartamentoCreate, DepartamentoRead, DepartamentoUpdate

def create_departamento(departamento: DepartamentoCreate):
    """
    Função para cadastrar departamentos no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                INSERT INTO Departamento (nome, id_universidade)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (departamento.nome, departamento.id_universidade)
            )

            departamento_cadastrado = cur.fetchone()
            
            conn.commit()
        
            return departamento_cadastrado

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar departamento: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_departamentos():
    """
    Função para acessar todos os departamentos cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Departamento
                """
            )
            departamentos = cur.fetchall()
            conn.commit()
            return departamentos
    finally:
        if conn: 
            conn.close()

def get_ies_departamentos(id_universidade: int):
    """
    Função para acessar todos os departamentos de uma universidade no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Departamento
                WHERE id_universidade = %s;
                """,
                (id_universidade,)
            )
            departamentos = cur.fetchall()
            conn.commit()
            return departamentos
    finally:
        if conn: 
            conn.close()

def get_departamento_by_id(id: int):
    """
    Função para acessar um departamento específico cadastrado no banco de dados, pelo seu id
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Departamento
                WHERE Departamento.id_departamento = %s;
                """,
                (id,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def update_departamento(id: int, departamento_data: DepartamentoUpdate):
    """
    Atualiza um departamento no banco de dados.
    """

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:

            cur.execute(
                """
                UPDATE Departamento
                SET nome = %s
                WHERE id_departamento = %s
                RETURNING *;
                """,
                (departamento_data.nome, id)
            )

            return cur.fetchone()
    finally:
        if conn:
            conn.close()