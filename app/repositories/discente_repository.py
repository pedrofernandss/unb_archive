import psycopg
from psycopg.rows import dict_row
from app.database import cria_conexao_db
from app.schemas.usuario_schema import DiscenteCreate, DiscenteUpdate
from . import usuario_repository 

def create_discente(discente: DiscenteCreate):
    """
    Função para cadastrar discentes no banco de dados da aplicação.
    Agora, também cria uma reputação padrão para o novo discente.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            # 1. Cria o registro na tabela Usuario
            usuario_repository._create_base_user(cur, discente)

            # 2. Cria uma reputação padrão para o novo discente
            cur.execute(
                """
                INSERT INTO Reputacao (pontuacao, nivel)
                VALUES (0, 'Iniciante')
                RETURNING id_reputacao;
                """
            )
            # Pega o ID da reputação recém-criada
            new_reputation_id = cur.fetchone()['id_reputacao']

            # 3. Insere o discente com o ID da reputação
            cur.execute(
                """
                INSERT INTO Discente (id_usuario_discente, ano_ingresso, status, coeficiente_rendimento, id_reputacao)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (discente.cpf, discente.ano_ingresso, discente.status, discente.coeficiente_rendimento, new_reputation_id)
            )
            
            # 4. Retorna os dados completos do discente criado
            cur.execute(
                """
                SELECT 
                    u.cpf, u.nome, u.email, u.matricula, u.id_universidade, u.id_departamento,
                    d.ano_ingresso, d.status, d.coeficiente_rendimento, d.id_reputacao
                FROM 
                    Usuario u JOIN Discente d ON u.cpf = d.id_usuario_discente
                WHERE 
                    u.cpf = %s;
                """,
                (discente.cpf,)
            )
            
            discente_cadastrado = cur.fetchone()
            
            conn.commit()
            
            return discente_cadastrado

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao criar discente: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_all_discentes():
    """
    Função para acessar todos os discentes cadastrados no banco de dados da aplicação
    """
    conn = None
    try: 
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Usuario
                JOIN 
                    Discente ON Usuario.cpf = Discente.id_usuario_discente 
                """
            )
            return cur.fetchall()
    finally:
        if conn: 
            conn.close()

def get_discente_by_cpf(cpf: str):
    """
    Função para acessar Discente específico cadastrado no banco de dados, pelo número do CPF
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT * FROM Usuario usuario
                JOIN Discente discente ON usuario.cpf = discente.id_usuario_discente
                WHERE usuario.cpf = %s;
                """,
                (cpf,)
            )
            return cur.fetchone()
    finally:
        if conn:
            conn.close()

def update_discente(cpf: str, data: DiscenteUpdate):
    """
    Atualiza um discente, modificando as tabelas Usuario e/ou Discente.
    """
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        return get_discente_by_cpf(cpf)

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

            campos_discente = [key for key in ["ano_ingresso", "status", "coeficiente_rendimento", "id_reputacao"] if key in update_data]

            if campos_discente:
                set_clauses = [f"{key} = %s" for key in campos_discente]
                params = [update_data[key] for key in campos_discente]
                params.append(cpf)

                query_discente = f"UPDATE Discente SET {', '.join(set_clauses)} WHERE id_usuario_discente = %s;"
                cur.execute(query_discente, tuple(params))

            conn.commit()
            
            return get_discente_by_cpf(cpf)

    except psycopg.Error as e:
        if conn:
            conn.rollback()
        print(f"Erro ao atualizar discente: {e}")
        raise
    finally:
        if conn:
            conn.close()
