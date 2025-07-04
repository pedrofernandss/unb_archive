import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.curso_schema import CursoCreate, CursoRead

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