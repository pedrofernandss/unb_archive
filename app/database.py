import psycopg
import os
from dotenv import load_dotenv
from psycopg import Error

load_dotenv()

def cria_conexao_db():
    """
    Cria e retorna uma nova conexão com o banco de dados.
    """
    try:
        database_url = os.getenv("DATABASE_URL")

        conn = psycopg.connect(database_url) # type: ignore
        print("Conexão com o PostgreSQL estabelecida com sucesso!")
        return conn

    except Error as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")