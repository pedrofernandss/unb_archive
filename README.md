# UNB Archive

## 📝 Descrição do Projeto

Este é um projeto acadêmico para a matéria de Bancos de Dados que consiste na criação de um sistema completo para gerenciamento de materiais de estudo, usuários (discentes e docentes), disciplinas e suas inter-relações em um ambiente universitário.

A aplicação é construída com:
* **Backend:** Python, usando o framework **FastAPI**.
* **Banco de Dados:** **PostgreSQL**, com interação via SQL puro através da biblioteca `psycopg`.
* **Frontend:** Uma interface web interativa construída com **Streamlit** para demonstração e interação com a API.

## Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados na sua máquina:

* **Python** (versão 3.10 ou superior)
* **PostgreSQL** (servidor de banco de dados)
* **Git**

## ⚙️ Configuração do Ambiente Local

Siga estes passos para configurar o projeto na sua máquina.

**1. Clonar o Repositório**
```bash
git clone [https://github.com/pedrofernandss/unb_archive.git](https://github.com/pedrofernandss/unb_archive.git)
cd unb_archive
````

**2. Criar e Ativar o Ambiente Virtual (`.venv`)**
É crucial usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Cria a pasta .venv
python -m venv .venv
```

Agora, ative o ambiente:

  * **No Windows (PowerShell):**
    ```powershell
    .\.venv\Scripts\activate
    ```
  * **No macOS ou Linux:**
    ```bash
    source .venv/bin/activate
    ```

Após a ativação, você verá `(.venv)` no início do seu terminal.

**3. Instalar as Dependências**
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias com um único comando:

```bash
pip install -r requirements.txt
```

## 🗄️ Configuração do Banco de Dados

**1. Criar o Banco de Dados (Apenas na primeira vez)**
Abra o `psql` ou uma ferramenta gráfica (pgAdmin, DBeaver) e crie um novo banco de dados vazio.

```sql
CREATE DATABASE unb_archive;
```

**2. Criar as Tabelas (Executar o Schema)**
Este projeto usa um arquivo `schema.sql` para definir a estrutura de todas as tabelas. Você deve executar este script manualmente no banco de dados que acabou de criar.

  * Navegue até a pasta **raiz** do projeto no seu terminal.
  * Execute o comando abaixo (substituindo `postgres` pelo seu usuário, se for diferente):
    ```bash
    psql -U postgres -d unb_archive -f database/schema.sql
    ```
  * Digite a senha do seu usuário do banco quando solicitado.

**3. Configurar a Conexão no Projeto**
Este projeto usa um arquivo `.env` para gerenciar a string de conexão.

  * Crie um arquivo chamado `.env` na pasta raiz do projeto.

  * Copie o conteúdo abaixo para dentro do seu `.env` e **substitua com suas credenciais reais**:

    ```env
    DATABASE_URL="postgresql://postgres:SUA_SENHA_AQUI@localhost:5432/unb_archive"
    ```

## 🔄 Resetando o Banco de Dados (se necessário)

Durante o desenvolvimento, pode ser necessário apagar e recriar o banco de dados para aplicar mudanças no `schema.sql`. Siga estes passos no seu terminal:

**1. Acesse o psql como superusuário:**

```bash
psql -U postgres -h localhost
```

*Digite sua senha.*

**2. Dentro do psql, execute os seguintes comandos:**

```sql
DROP DATABASE unb_archive;
CREATE DATABASE unb_archive;
\q
```

**3. Execute o schema novamente no banco recém-criado:**

```bash
psql -U postgres -d unb_archive -f database/schema.sql
```

## ▶️ Rodando a Aplicação (Backend e Frontend)

A aplicação é dividida em duas partes que precisam ser executadas em **terminais separados**.

### Parte 1: Iniciar o Backend (API FastAPI)

1.  Abra um terminal na pasta raiz do projeto.
2.  Ative o ambiente virtual: `.\.venv\Scripts\activate`
3.  Execute o seguinte comando para iniciar o servidor da API:
    ```bash
    uvicorn app.main:app --reload
    ```
4.  O backend estará rodando em `http://127.0.0.1:8000`.

### Parte 2: Iniciar o Frontend (Interface Streamlit)

1.  Abra um **novo terminal** na pasta raiz do projeto.
2.  Ative o ambiente virtual neste novo terminal: `.\.venv\Scripts\activate`
3.  Execute o comando para iniciar a interface web:
    ```bash
    streamlit run interface_principal.py
    ```
4.  Uma nova aba será aberta no seu navegador com a interface da aplicação, pronta para uso.

## 📚 Documentação da API

Com o backend rodando, você pode acessar a documentação interativa da API (gerada automaticamente pelo FastAPI) nos seguintes endereços:

  * **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
  * **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)
