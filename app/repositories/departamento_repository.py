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

def delete_departamento_by_id_cascade(id_departamento: int) -> int:
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            
            cur.execute("SELECT codigo FROM Disciplina WHERE id_departamento = %s;", (id_departamento,))
            disciplinas_tuples = cur.fetchall()
            
            if disciplinas_tuples:
                disciplina_ids = tuple([item[0] for item in disciplinas_tuples])
               
                cur.execute("SELECT id_material FROM Material WHERE id_disciplina IN %s;", (disciplina_ids,))  # Encontra todos os materiais dessas disciplinas
                materiais_tuples = cur.fetchall()

                if materiais_tuples:
                    material_ids = tuple([item[0] for item in materiais_tuples])
                   
                    cur.execute("DELETE FROM Possui WHERE id_material IN %s;", (material_ids,))
                    cur.execute("DELETE FROM Avalia WHERE id_material IN %s;", (material_ids,))
                    cur.execute("DELETE FROM Avaliacao WHERE id_material IN %s;", (material_ids,))
                    cur.execute("DELETE FROM Compartilha_Produz WHERE id_material IN %s;", (material_ids,))
                    cur.execute("DELETE FROM Material WHERE id_disciplina IN %s;", (disciplina_ids,))
                cur.execute("DELETE FROM Disciplina WHERE id_departamento = %s;", (id_departamento,))

            cur.execute("SELECT cpf FROM Usuario WHERE id_departamento = %s;", (id_departamento,))
            usuarios_tuples = cur.fetchall()
            if usuarios_tuples:
                usuario_cpfs = tuple([item[0] for item in usuarios_tuples])
                cur.execute("DELETE FROM Discente WHERE id_usuario_discente IN %s;", (usuario_cpfs,))
                cur.execute("DELETE FROM Docente WHERE id_usuario_docente IN %s;", (usuario_cpfs,))
                cur.execute("DELETE FROM Usuario WHERE id_departamento = %s;", (id_departamento,))
            
            cur.execute("DELETE FROM Curso WHERE departamento_curso = %s;", (id_departamento,))
            cur.execute("DELETE FROM Escolaridade WHERE departamento_escolaridade = %s;", (id_departamento,))

            cur.execute("DELETE FROM Departamento WHERE id_departamento = %s;", (id_departamento,))
            linhas_deletadas = cur.rowcount
            
            conn.commit()
            return linhas_deletadas
    finally:
        if conn:
            conn.close()