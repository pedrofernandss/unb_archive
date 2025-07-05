import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import UsuarioCreate

def _create_base_user(cursor, user: UsuarioCreate):
    """
    Função base para cadastrar usuarios no banco de dados da aplicação
    """
    cursor.execute(
        """
        INSERT INTO Usuario (cpf, nome, senha, email, id_departamento, matricula)
        VALUES (%s, %s, %s, %s, %s, %s);
        """,
        (user.cpf, user.nome, user.senha, user.email, user.id_departamento, user.matricula)
    )

def get_all_usuarios():
    """
    Função para acessar todos os usuários cadastrados no banco de dados da aplicação, independente do tipo.
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT *  
                FROM Usuario
                """
            )
            todos_usuarios = cur.fetchall()
            conn.commit()
            return todos_usuarios
    finally:
        if conn: 
            conn.close()