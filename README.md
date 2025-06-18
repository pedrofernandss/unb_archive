# unb_archive

# Projeto de API com FastAPI e PostgreSQL

Este é um projeto acadêmico para a matéria de Bancos de Dados que consiste na criação de um sistema para gerenciamento de [Descreva o objetivo, ex: produtos, usuários, etc.].

A aplicação é construída com Python, usando o framework FastAPI e se conecta a um banco de dados PostgreSQL utilizando SQL puro através da biblioteca `psycopg`.

## Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados na sua máquina:

* **Python** (versão 3.10 ou superior)
* **PostgreSQL** (servidor de banco de dados)
* **Git**

## ⚙️ Configuração do Ambiente Local

Siga estes passos para configurar o projeto na sua máquina.

**1. Clonar o Repositório**
```bash
git clone https://github.com/pedrofernandss/unb_archive.git
cd unb_archive
```

**2. Criar e Ativar o Ambiente Virtual (`venv`)**
É crucial usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Cria a pasta .venv
python -m venv .venv
```

Agora, ative o ambiente:
* **No Windows (PowerShell):**
    ```powershell
    .\.venv\Scripts\Activate.ps1
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

## 🗄️ Configuração do Banco de Dados

**1. Criar o Banco de Dados**
Abra uma ferramenta de gerenciamento do PostgreSQL (como o `psql` ou pgAdmin) e crie um novo banco de dados vazio.
```sql
CREATE DATABASE unb_archive;
```

**2. Criar as Tabelas (Executar o Schema)**
Este projeto usa um arquivo `schema.sql` para definir a estrutura de todas as tabelas. Você deve executar este script manualmente no banco de dados que acabou de criar.

* **Opção 1 (Via Ferramenta Gráfica):**
    1.  Abra o banco `unb_archive` no pgAdmin ou DBeaver.
    2.  Abra uma janela de query.
    3.  Copie todo o conteúdo do arquivo **`database/schema.sql`** e cole na janela de query.
    4.  Execute o script.

* **Opção 2 (Via Linha de Comando):**
    1.  Navegue até a pasta **raiz** do projeto no seu terminal.
    2.  Execute o comando abaixo (substituindo `postgres` pelo seu usuário, se for diferente):
        ```bash
        psql -U postgres -d unb_archive -f database/schema.sql
        ```
    3.  Digite a senha do seu usuário do banco quando solicitado.

Após executar o script, suas tabelas estarão criadas e prontas para uso.

**3. Configurar a Conexão no Projeto**
Este projeto usa um arquivo `.env` para gerenciar a string de conexão.

* Crie um arquivo chamado `.env` na pasta raiz do projeto.
* Copie o conteúdo abaixo para dentro do seu `.env` e **substitua com suas credenciais reais**:

    ```env
    DATABASE_URL="postgresql://postgres:SUA_SENHA_AQUI@localhost:5432/unb_archive"
    ```
```

## ▶️ Rodando a Aplicação

Com o ambiente configurado e o banco de dados pronto, você pode iniciar o servidor da API.

1.  Certifique-se de que seu ambiente virtual (`.venv`) está ativo.
2.  Execute o seguinte comando no terminal, a partir da pasta raiz do projeto:

    ```bash
    uvicorn app.main:app --reload
    ```
3.  O terminal deverá exibir uma mensagem indicando que o servidor está rodando, algo como:
    ```
    INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)