import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.disciplina_schema import DisciplinaCreate, DisciplinaRead, DisciplinaUpdate

def create_disciplina(disciplina: DisciplinaCreate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Disciplina (nome, iddepartamento)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (disciplina.nome, disciplina.iddepartamento)
            )
            disciplina_cadastrada = cur.fetchone()
            conn.commit()
            return disciplina_cadastrada
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar disciplina: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_disciplinas():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM Disciplina")
            disciplinas = cur.fetchall()
            return disciplinas
    finally:
        if conn:
            conn.close()

def get_disciplina_by_codigo(codigo: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Disciplina WHERE codigo = %s",
                (codigo,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def update_disciplina(codigo: int, disciplina_data: DisciplinaUpdate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            update_fields = []
            params = []
            
            if disciplina_data.nome is not None:
                update_fields.append("nome = %s")
                params.append(disciplina_data.nome)
                
            if disciplina_data.iddepartamento is not None:
                update_fields.append("iddepartamento = %s")
                params.append(disciplina_data.iddepartamento)
                
            params.append(codigo)
            
            query = f"""
                UPDATE Disciplina
                SET {", ".join(update_fields)}
                WHERE codigo = %s
                RETURNING *;
            """
            cur.execute(query, tuple(params))
            updated_disciplina = cur.fetchone()
            conn.commit()
            return updated_disciplina
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar disciplina: {e}")
        raise
    finally:
        if conn:
            conn.close()

def delete_disciplina(codigo: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Disciplina WHERE codigo = %s",
                (codigo,)
            )
            conn.commit()
    finally:
        if conn:
            conn.close()