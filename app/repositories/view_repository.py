from psycopg.rows import dict_row
from app.database import cria_conexao_db

def get_all_materiais_completos():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM vw_materiais_completos;")
            return cur.fetchall()
    finally:
        if conn:
            conn.close()