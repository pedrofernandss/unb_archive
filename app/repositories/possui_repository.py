import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.possui_schema import PossuiCreate, PossuiUpdate

def create_possui(possui: PossuiCreate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                INSERT INTO Possui (id_material, id_tag)
                VALUES (%s, %s)
                RETURNING id_possui, id_material, id_tag;
            """, (possui.id_material, possui.id_tag)
            )
            novo_possui = cur.fetchone()
            conn.commit()
            return novo_possui
        
    except psycopg.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_all_possuir():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id_possui, id_material, id_tag FROM Possui")
            return cur.fetchall()
    finally:
        if conn:
            conn.close()

def get_possuir_by_id(id_possui: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM Possui WHERE id_possui = %s",
                (id_possui,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def update_possuir(id_possui: int, data: PossuiUpdate):
    update_data = data.model_dump(exclude_unset=True)
    set_query = [f"{key} = %s" for key in update_data.keys()]
    query_str = ", ".join(set_query)
    params = list(update_data.values()) + [id_possui]

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                f"UPDATE Possui SET {query_str} WHERE id_possui = %s RETURNING *;",
                tuple(params)
            )
            conn.commit()
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def delete_possuir(id_possui: int) -> bool:
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "DELETE FROM Possui WHERE id_possui = %s RETURNING id_possui;",
                (id_possui,)
            )
            deleted = cur.fetchone()
            conn.commit()
            return deleted is not None
    finally:
        if conn:
            conn.close()
