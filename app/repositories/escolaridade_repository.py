import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.escolaridade_schema import EscolaridadeCreate, EscolaridadeRead, EscolaridadeUpdate

def create_escolaridade(escolaridade: EscolaridadeCreate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Escolaridade (escolaridade, departamento_escolaridade)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (escolaridade.escolaridade, escolaridade.departamento_escolaridade)
            )
            escolaridade_cadastrada = cur.fetchone()
            conn.commit()
            return escolaridade_cadastrada
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar escolaridade: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_escolaridades():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM Escolaridade")
            escolaridades = cur.fetchall()
            return escolaridades
    finally:
        if conn:
            conn.close()

def get_escolaridades_by_departamento(departamento_id: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Escolaridade WHERE departamento_escolaridade = %s",
                (departamento_id,)
            )
            escolaridade_departamento = cur.fetchall()
            conn.commit()
            
            return escolaridade_departamento
    finally:
        if conn:
            conn.close()
            
def update_escolaridade(escolaridade_nome: str, departamento_id: int, escolaridade_data: EscolaridadeUpdate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE Escolaridade
                SET escolaridade = %s
                WHERE escolaridade = %s AND departamento_escolaridade = %s
                RETURNING *;
                """,
                (escolaridade_data.escolaridade, escolaridade_nome, departamento_id)
            )
            updated_escolaridade = cur.fetchone()
            conn.commit()
            return updated_escolaridade
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar escolaridade: {e}")
        raise
    finally:
        if conn:
            conn.close()

def delete_escolaridade(escolaridade_nome: str, departamento_id: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Escolaridade WHERE escolaridade = %s AND departamento_escolaridade = %s",
                (escolaridade_nome, departamento_id)
            )
            conn.commit()
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao deletar escolaridade: {e}")
        raise
    finally:
        if conn:
            conn.close()