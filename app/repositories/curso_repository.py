import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.curso_schema import CursoCreate, CursoRead, CursoUpdate

def create_curso(curso: CursoCreate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Curso (curso, departamento_curso)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (curso.curso, curso.departamento_curso)
            )
            curso_cadastrado = cur.fetchone()
            conn.commit()
            return curso_cadastrado
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar curso: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_cursos():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM Curso")
            cursos = cur.fetchall()
            return cursos
    finally:
        if conn:
            conn.close()

def get_cursos_by_departamento(departamento_id: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Curso WHERE departamento_curso = %s",
                (departamento_id,)
            )
            return cur.fetchall()
    finally:
        if conn:
            conn.close()

def update_curso(curso_nome: str, departamento_id: int, curso_data: CursoUpdate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE Curso
                SET curso = %s
                WHERE curso = %s AND departamento_curso = %s
                RETURNING *;
                """,
                (curso_data.curso, curso_nome, departamento_id)
            )
            updated_curso = cur.fetchone()
            conn.commit()
            return updated_curso
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar curso: {e}")
        raise
    finally:
        if conn:
            conn.close()

def delete_curso(curso_nome: str, departamento_id: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Curso WHERE curso = %s AND departamento_curso = %s",
                (curso_nome, departamento_id)
            )
            conn.commit()
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao deletar curso: {e}")
        raise
    finally:
        if conn:
            conn.close()