import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import DocenteCreate, DocenteUpdate
from . import usuario_repository 

def create_docente(docente: DocenteCreate):
    """
    Função para cadastrar docentes no banco de dados da aplicação
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            usuario_repository._create_base_user(cur, docente)

            cur.execute(
                """
                INSERT INTO Docente (id_usuario_docente, especialidade, permissao_validacao)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (docente.cpf, docente.especialidade, docente.permissao_validacao)
            )
            
            cur.execute(
                """
                SELECT 
                    usuario.cpf, usuario.nome, usuario.email, usuario.matricula, usuario.id_departamento,
                    docente.especialidade, docente.permissao_validacao
                FROM 
                    Usuario usuario JOIN Docente docente ON usuario.cpf = docente.id_usuario_docente
                WHERE 
                    usuario.cpf = %s;
                """,
                (docente.cpf,)
            )
            
            docente_cadastrado = cur.fetchone()
            
            conn.commit()
            
            return docente_cadastrado

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar docente: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_docentes():
    """
    Função para acessar todos os docentes cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Usuario
                JOIN 
                    Docente ON Usuario.cpf = Docente.id_usuario_docente 
                """
            )
            todos_docentes = cur.fetchall()
            conn.commit()
            return todos_docentes
    finally:
        if conn: 
            conn.close()

def get_docente_by_cpf(cpf: str):
    """
    Função para acessar docente específico cadastrado no banco de dados, pelo número do CPF
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Usuario usuario
                JOIN Docente docente ON usuario.cpf = docente.id_usuario_docente
                WHERE usuario.cpf = %s;
                """,
                (cpf,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def update_docente(cpf: str, data: DocenteUpdate):
    """
    Atualiza um docente, modificando as tabelas Usuario e/ou Docente.
    """

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return get_docente_by_cpf(cpf)

    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            
            campos_usuario = [key for key in ["nome", "email", "senha", "id_departamento", "matricula"] if key in update_data]
            
            if campos_usuario:
                set_clauses = [f"{key} = %s" for key in campos_usuario]
                params = [update_data[key] for key in campos_usuario]
                params.append(cpf) 
                
                query_usuario = f"UPDATE Usuario SET {', '.join(set_clauses)} WHERE cpf = %s;"
                cur.execute(query_usuario, tuple(params))

            campos_docente = [key for key in ["especialidade", "permissao_validacao"] if key in update_data]

            if campos_docente:
                set_clauses = [f"{key} = %s" for key in campos_docente]
                params = [update_data[key] for key in campos_docente]
                params.append(cpf)

                query_docente = f"UPDATE Docente SET {', '.join(set_clauses)} WHERE id_usuario_docente = %s;"
                cur.execute(query_docente, tuple(params))

            conn.commit()
            
            return get_docente_by_cpf(cpf)

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar docente: {e}")
        raise
    finally:
        if conn:
            conn.close()