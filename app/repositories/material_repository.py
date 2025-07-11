import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.material_schema import MaterialCreate, MaterialRead, MaterialUpdate


def create_material(nome, descricao, ano_semestre_ref, local_arquivo, id_disciplina):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Material (nome, descricao, ano_semestre_ref, local_arquivo, id_disciplina)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_material, nome, descricao, ano_semestre_ref, local_arquivo,  id_disciplina;
                """,
                (
                    nome,
                    descricao,
                    ano_semestre_ref,
                    local_arquivo,
                    id_disciplina
                )
            )
            material = cur.fetchone()
            conn.commit()
            return material

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar material: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_all_materiais():
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT id_material, nome, descricao, ano_semestre_ref, id_disciplina
                FROM Material
                """
            )
            material = cur.fetchall()
            conn.commit()
            return material
    finally:
        if conn:
            conn.close()


def get_material_by_id(id_material: int):
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Material
                WHERE id_material = %s;
                """,
                (id_material,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def update_material(id_material: int, data: MaterialUpdate):
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return None 

    set_query = [f"{key} = %s" for key in update_data.keys()]
    set_query_str = ", ".join(set_query)

    params_atualizacao_lista = list(update_data.values())
    params_atualizacao_lista.append(id_material)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            query = f"""
                UPDATE Material
                SET {set_query_str}
                WHERE id_material = %s
                RETURNING *;       
            """
            cur.execute(query, tuple(params_atualizacao_lista))
            conn.commit()
            return cur.fetchone()
    finally:
        if conn:
            conn.close()


def delete_material(id_material: int):
    conn = cria_conexao_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Material WHERE id_material = %s;",
                (id_material,)
            )
            conn.commit()
            return cur.rowcount > 0 
    finally:
        conn.close()