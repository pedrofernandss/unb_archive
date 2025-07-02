import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.material_schema import MaterialCreate, MaterialRead, MaterialUpdate

def create_material(material: MaterialCreate):
    """
    Função para cadastrar materiais no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO Material (nome, descricao, ano_semestre_ref, local_arquivo, idDisciplina)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (material.nome, material.descricao, material.ano_semestre_ref, material.local_arquivo, material.iddisciplina)
            )
            material_cadastrado = cur.fetchone()
            conn.commit()
            return material_cadastrado

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar material: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_material():
    """
    Função para acessar todos os materiais cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Material
                """
            )
            materiais = cur.fetchall()
            return materiais
    finally:
        if conn: 
            conn.close()

def get_material_by_id(id_material: int):
    """
    Função para acessar um material específico cadastrado no banco de dados pelo seu id.
    """
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

def update_material(id_material: int, material_data: MaterialUpdate):
    """
    Atualiza um material no banco de dados.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            # Cria lista dinâmica de campos
            fields = []
            values = []

            if material_data.nome is not None:
                fields.append("nome = %s")
                values.append(material_data.nome)
            if material_data.descricao is not None:
                fields.append("descricao = %s")
                values.append(material_data.descricao)
            if material_data.ano_semestre_ref is not None:
                fields.append("ano_semestre_ref = %s")
                values.append(material_data.ano_semestre_ref)

            if not fields:
                raise ValueError("Nenhum campo para atualizar.")

            values.append(id_material)

            query = f"""
                UPDATE Material
                SET {', '.join(fields)}
                WHERE id_material = %s
                RETURNING *;
            """

            cur.execute(query, tuple(values))
            updated_material = cur.fetchone()
            conn.commit()
            return updated_material

    finally:
        if conn:
            conn.close()

def delete_material(id_material: int):
    """
    Remove um material do banco de dados.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                DELETE FROM Material
                WHERE id_material = %s
                RETURNING *;
                """,
                (id_material,)
            )
            deleted_material = cur.fetchone()
            conn.commit()
            return deleted_material
    finally:
        if conn:
            conn.close()
