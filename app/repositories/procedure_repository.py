import psycopg
from app.database import cria_conexao_db
from app.schemas.procedure_schema import ValidacaoMaterialRequest

def execute_gerenciar_validacao_material(request_data: ValidacaoMaterialRequest):
    """
    Chama a stored procedure 'gerenciar_validacao_material' no banco de dados.
    """
    conn = None
    try:
        conn = cria_conexao_db()
        with conn.cursor() as cur:
            cur.execute(
                "CALL gerenciar_validacao_material(%s, %s, %s);",
                (
                    request_data.id_material,
                    request_data.cpf_docente,
                    request_data.acao_valida
                )
            )
            conn.commit()
    except psycopg.Error as e:
        if conn:
            conn.rollback()

        raise e
    finally:
        if conn:
            conn.close()