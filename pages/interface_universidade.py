import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="Gestão Universidade", layout="centered")

st.title("📚 Gestão de Universidade, Departamento e Disciplina")

# --- Helpers para limpar cache e buscar dados ---
@st.cache_data(ttl=60)
def get_universidades():
    try:
        res = requests.get(f"{API_URL}/universidade")
        res.raise_for_status()
        return res.json()
    except:
        return []

@st.cache_data(ttl=60)
def get_departamentos():
    try:
        res = requests.get(f"{API_URL}/departamento")
        res.raise_for_status()
        return res.json()
    except:
        return []

@st.cache_data(ttl=60)
def get_disciplinas():
    try:
        res = requests.get(f"{API_URL}/disciplina")
        res.raise_for_status()
        return res.json()
    except:
        return []

def limpar_cache():
    get_universidades.clear()
    get_departamentos.clear()
    get_disciplinas.clear()

# --- Seleção de operação ---
operacao = st.sidebar.selectbox("Operação", ["Criar", "Listar", "Editar", "Deletar"])
entidade = st.sidebar.selectbox("Entidade", ["Universidade", "Departamento", "Disciplina"])

# --- FUNÇÕES DE CREATE ---
def criar_universidade():
    st.header("Criar Universidade")
    with st.form("form_uni"):
        nome = st.text_input("Nome")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado (UF)", max_chars=2)
        if st.form_submit_button("Cadastrar"):
            if not nome or not cidade or not estado:
                st.error("Preencha todos os campos!")
                return
            data = {"nome": nome, "cidade": cidade, "estado": estado.upper()}
            res = requests.post(f"{API_URL}/universidade", json=data)
            if res.status_code == 201:
                st.success("Universidade criada!")
                st.json(res.json())
                limpar_cache()
            else:
                st.error(f"Erro: {res.text}")

def criar_departamento():
    st.header("Criar Departamento")
    universidades = get_universidades()
    if not universidades:
        st.warning("Cadastre uma universidade antes.")
        return
    uni_options = {u['nome']: u['ies'] for u in universidades}
    with st.form("form_depto"):
        nome = st.text_input("Nome do Departamento")
        uni_nome = st.selectbox("Universidade", options=uni_options.keys())
        if st.form_submit_button("Cadastrar"):
            if not nome or not uni_nome:
                st.error("Preencha todos os campos!")
                return
            data = {"nome": nome, "id_universidade": uni_options[uni_nome]}
            res = requests.post(f"{API_URL}/departamento", json=data)
            if res.status_code == 201:
                st.success("Departamento criado!")
                st.json(res.json())
                limpar_cache()
            else:
                st.error(f"Erro: {res.text}")

def criar_disciplina():
    st.header("Criar Disciplina")
    departamentos = get_departamentos()
    if not departamentos:
        st.warning("Cadastre um departamento antes.")
        return
    depto_options = {d['nome']: d['id_departamento'] for d in departamentos}
    with st.form("form_disc"):
        nome = st.text_input("Nome da Disciplina")
        depto_nome = st.selectbox("Departamento", options=depto_options.keys())
        if st.form_submit_button("Cadastrar"):
            if not nome or not depto_nome:
                st.error("Preencha todos os campos!")
                return
            data = {"nome": nome, "id_departamento": depto_options[depto_nome]}
            res = requests.post(f"{API_URL}/disciplina", json=data)
            if res.status_code == 201:
                st.success("Disciplina criada!")
                st.json(res.json())
                limpar_cache()
            else:
                st.error(f"Erro: {res.text}")

# --- FUNÇÕES DE LISTAR ---
def listar_universidades():
    st.header("Lista de Universidades")
    universidades = get_universidades()
    if universidades:
        for uni in universidades:
            st.write(f"IES: {uni['ies']} | Nome: {uni['nome']} | Cidade: {uni['cidade']} | Estado: {uni['estado']}")
    else:
        st.warning("Nenhuma universidade cadastrada.")

def listar_departamentos():
    st.header("Lista de Departamentos")
    departamentos = get_departamentos()
    if departamentos:
        for d in departamentos:
            st.write(f"ID: {d['id_departamento']} | Nome: {d['nome']} | Universidade ID: {d['id_universidade']}")
    else:
        st.warning("Nenhum departamento cadastrado.")

def listar_disciplinas():
    st.header("Lista de Disciplinas")
    disciplinas = get_disciplinas()
    if disciplinas:
        for d in disciplinas:
            st.write(f"Código: {d['codigo']} | Nome: {d['nome']} | Departamento ID: {d['id_departamento']}")
    else:
        st.warning("Nenhuma disciplina cadastrada.")

# --- FUNÇÕES DE EDITAR ---
def editar_universidade():
    st.header("Editar Universidade")
    universidades = get_universidades()
    if not universidades:
        st.warning("Nenhuma universidade para editar.")
        return
    opcoes = {f"{u['nome']} ({u['ies']})": u['ies'] for u in universidades}
    escolha = st.selectbox("Escolha a universidade:", list(opcoes.keys()))
    id_ies = opcoes[escolha]

    with st.form("form_edit_uni"):
        novo_nome = st.text_input("Novo Nome")
        nova_cidade = st.text_input("Nova Cidade")
        novo_estado = st.text_input("Novo Estado (UF)", max_chars=2)

        if st.form_submit_button("Atualizar"):
            update_data = {}
            if novo_nome.strip():
                update_data["nome"] = novo_nome
            if nova_cidade.strip():
                update_data["cidade"] = nova_cidade
            if novo_estado.strip():
                update_data["estado"] = novo_estado.upper()

            if update_data:
                res = requests.patch(f"{API_URL}/universidade/{id_ies}", json=update_data)
                if res.status_code == 200:
                    st.success("Universidade atualizada!")
                    st.json(res.json())
                    limpar_cache()
                else:
                    st.error(f"Erro: {res.text}")
            else:
                st.warning("Preencha pelo menos um campo para atualizar.")

def editar_departamento():
    st.header("Editar Departamento")
    departamentos = get_departamentos()
    if not departamentos:
        st.warning("Nenhum departamento para editar.")
        return
    opcoes = {f"{d['nome']} ({d['id_departamento']})": d['id_departamento'] for d in departamentos}
    escolha = st.selectbox("Escolha o departamento:", list(opcoes.keys()))
    id_departamento = opcoes[escolha]

    with st.form("form_edit_depto"):
        novo_nome = st.text_input("Novo Nome")

        if st.form_submit_button("Atualizar"):
            update_data = {}
            if novo_nome.strip():
                update_data["nome"] = novo_nome
            if update_data:
                res = requests.patch(f"{API_URL}/departamento/{id_departamento}", json=update_data)
                if res.status_code == 200:
                    st.success("Departamento atualizado!")
                    st.json(res.json())
                    limpar_cache()
                else:
                    st.error(f"Erro: {res.text}")
            else:
                st.warning("Preencha pelo menos um campo para atualizar.")

def editar_disciplina():
    st.header("Editar Disciplina")
    disciplinas = get_disciplinas()
    if not disciplinas:
        st.warning("Nenhuma disciplina para editar.")
        return
    opcoes = {f"{d['nome']} ({d['codigo']})": d['codigo'] for d in disciplinas}
    escolha = st.selectbox("Escolha a disciplina:", list(opcoes.keys()))
    codigo = opcoes[escolha]

    with st.form("form_edit_disc"):
        novo_nome = st.text_input("Novo Nome")

        if st.form_submit_button("Atualizar"):
            update_data = {}
            if novo_nome.strip():
                update_data["nome"] = novo_nome
            if update_data:
                res = requests.patch(f"{API_URL}/disciplina/{codigo}", json=update_data)
                if res.status_code == 200:
                    st.success("Disciplina atualizada!")
                    st.json(res.json())
                    limpar_cache()
                else:
                    st.error(f"Erro: {res.text}")
            else:
                st.warning("Preencha pelo menos um campo para atualizar.")

# --- FUNÇÕES DE DELETAR ---
def deletar_universidade():
    st.header("Deletar Universidade")
    universidades = get_universidades()
    if not universidades:
        st.warning("Nenhuma universidade para deletar.")
        return
    opcoes = {f"{u['nome']} ({u['ies']})": u['ies'] for u in universidades}
    escolha = st.selectbox("Escolha a universidade:", list(opcoes.keys()))
    id_ies = opcoes[escolha]

    if st.button("Deletar"):
        res = requests.delete(f"{API_URL}/universidade/{id_ies}")
        if res.status_code == 204:
            st.success("Universidade deletada!")
            limpar_cache()
        else:
            st.error(f"Erro: {res.text}")

def deletar_departamento():
    st.header("Deletar Departamento")
    departamentos = get_departamentos()
    if not departamentos:
        st.warning("Nenhum departamento para deletar.")
        return
    opcoes = {f"{d['nome']} ({d['id_departamento']})": d['id_departamento'] for d in departamentos}
    escolha = st.selectbox("Escolha o departamento:", list(opcoes.keys()))
    id_departamento = opcoes[escolha]

    if st.button("Deletar"):
        res = requests.delete(f"{API_URL}/departamento/{id_departamento}")
        if res.status_code == 204:
            st.success("Departamento deletado!")
            limpar_cache()
        else:
            st.error(f"Erro: {res.text}")

def deletar_disciplina():
    st.header("Deletar Disciplina")
    disciplinas = get_disciplinas()
    if not disciplinas:
        st.warning("Nenhuma disciplina para deletar.")
        return
    opcoes = {f"{d['nome']} ({d['codigo']})": d['codigo'] for d in disciplinas}
    escolha = st.selectbox("Escolha a disciplina:", list(opcoes.keys()))
    codigo = opcoes[escolha]

    if st.button("Deletar"):
        res = requests.delete(f"{API_URL}/disciplina/{codigo}")
        if res.status_code == 204:
            st.success("Disciplina deletada!")
            limpar_cache()
        else:
            st.error(f"Erro: {res.text}")

# --- MAIN ---

if operacao == "Criar":
    if entidade == "Universidade":
        criar_universidade()
    elif entidade == "Departamento":
        criar_departamento()
    elif entidade == "Disciplina":
        criar_disciplina()

elif operacao == "Listar":
    if entidade == "Universidade":
        listar_universidades()
    elif entidade == "Departamento":
        listar_departamentos()
    elif entidade == "Disciplina":
        listar_disciplinas()

elif operacao == "Editar":
    if entidade == "Universidade":
        editar_universidade()
    elif entidade == "Departamento":
        editar_departamento()
    elif entidade == "Disciplina":
        editar_disciplina()

elif operacao == "Deletar":
    if entidade == "Universidade":
        deletar_universidade()
    elif entidade == "Departamento":
        deletar_departamento()
    elif entidade == "Disciplina":
        deletar_disciplina()