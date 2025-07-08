import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.possui_schema import PossuiCreate

def create_possui(possui: PossuiCreate):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                INSERT INTO Possui (id_material, id_tag)
                VALUES (%s, %s)
                RETURNING id_material, id_tag;
            """, (possui.id_material, possui.id_tag))
            novo = cur.fetchone()
            conn.commit()
            return novo
    finally:
        if conn:
            conn.close()

def delete_possui(id_material: int, id_tag: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM Possui 
                WHERE id_material = %s AND id_tag = %s
                RETURNING *;
            """, (id_material, id_tag))
            deleted = cur.fetchone()
            conn.commit()
            return deleted is not None
    finally:
        if conn:
            conn.close()

def get_tags_by_material(id_material: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT t.id_tag, t.nome_tag
                FROM Tag t
                JOIN Possui p ON t.id_tag = p.id_tag
                WHERE p.id_material = %s;
            """, (id_material,))
            return cur.fetchall()
    finally:
        if conn:
            conn.close()

def get_materiais_by_tag(id_tag: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT m.id_material, m.nome, m.descricao, m.ano_semestre_ref, m.id_disciplina
                FROM Material m
                JOIN Possui p ON m.id_material = p.id_material
                WHERE p.id_tag = %s;
            """, (id_tag,))
            return cur.fetchall()
    finally:
        if conn:
            conn.close()
