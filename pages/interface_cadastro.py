import streamlit as st
import requests
import pandas as pd
from decimal import Decimal

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="Cadastro de Usuários - UnB Archive",
    page_icon="👤",
    layout="centered"
)

st.title("👤 Cadastro de Novo Usuário")

@st.cache_data
def buscar_universidades():
    """Busca a lista de universidades da API."""
    try:
        response = requests.get(f"{API_URL}/universidade")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível buscar as universidades: {e}")
        return []

@st.cache_data
def buscar_departamentos():
    """Busca a lista de departamentos da API."""
    try:
        response = requests.get(f"{API_URL}/departamento")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível buscar os departamentos: {e}")
        return []

universidades = buscar_universidades()
departamentos = buscar_departamentos()

if universidades:
    opcoes_universidade = {uni['nome']: uni['ies'] for uni in universidades}
else:
    opcoes_universidade = {}
    st.warning("Nenhuma universidade encontrada. Cadastre uma universidade primeiro.")

if departamentos:
    opcoes_departamento = {depto['nome']: depto['id_departamento'] for depto in departamentos}
else:
    opcoes_departamento = {}
    st.warning("Nenhum departamento encontrado. Cadastre um departamento primeiro.")

tipo_usuario = st.radio(
    "Qual tipo de usuário você deseja cadastrar?",
    ("Discente", "Docente"),
    horizontal=True
)

if tipo_usuario == "Discente":
    st.header("Formulário de Cadastro de Discente")
    
    with st.form("form_discente", clear_on_submit=True):
        st.info("Preencha todos os campos para cadastrar um novo discente.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cpf = st.text_input("CPF (ex: 111.222.333-44)")
            nome = st.text_input("Nome Completo")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            matricula = st.number_input("Matrícula", step=1, format="%d")

        with col2:
            uni_selecionada_nome = st.selectbox("Universidade", options=opcoes_universidade.keys())
            depto_selecionado_nome = st.selectbox("Departamento", options=opcoes_departamento.keys())
            ano_ingresso = st.number_input("Ano de Ingresso", min_value=1960, max_value=2025, step=1)
            status = st.selectbox("Status", ["Regular", "Formado", "Trancado"])
            coeficiente = st.number_input("Coeficiente de Rendimento", min_value=0.0, max_value=10.0, step=0.1)

        submitted = st.form_submit_button("Cadastrar Discente")

        if submitted:
            if not all([cpf, nome, email, senha, matricula, depto_selecionado_nome, uni_selecionada_nome]):
                st.error("Todos os campos são obrigatórios.")
            else:
                id_universidade = opcoes_universidade[uni_selecionada_nome]
                id_departamento = opcoes_departamento[depto_selecionado_nome]
                
                discente_data = {
                    "cpf": cpf, "nome": nome, "senha": senha, "email": email,
                    "id_universidade": id_universidade,
                    "id_departamento": id_departamento,
                    "matricula": matricula,
                    "ano_ingresso": ano_ingresso, "status": status,
                    "coeficiente_rendimento": float(coeficiente)
                }
                
                try:
                    response = requests.post(f"{API_URL}/usuarios/discente", json=discente_data)
                    if response.status_code == 201:
                        st.success("Discente cadastrado com sucesso!")
                        st.json(response.json())
                    else:
                        st.error(f"Erro ao cadastrar discente: {response.status_code}")
                        st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão com a API: {e}")

elif tipo_usuario == "Docente":
    st.header("Formulário de Cadastro de Docente")
    
    with st.form("form_docente", clear_on_submit=True):
        st.info("Preencha todos os campos para cadastrar um novo docente.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cpf = st.text_input("CPF (ex: 111.222.333-44)")
            nome = st.text_input("Nome Completo")
            email = st.text_input("Email")
            matricula = st.number_input("Matrícula", step=1, format="%d")
            senha = st.text_input("Senha", type="password")
        
        with col2:
            uni_selecionada_nome = st.selectbox("Universidade", options=opcoes_universidade.keys())
            depto_selecionado_nome = st.selectbox("Departamento", options=opcoes_departamento.keys())
            especialidade = st.text_input("Especialidade (ex: Engenharia de Software)")
            permissao_validacao = st.checkbox("Tem permissão para validar materiais?")

        submitted = st.form_submit_button("Cadastrar Docente")
        
        if submitted:
            if not all([cpf, nome, email, matricula, senha, depto_selecionado_nome, uni_selecionada_nome]):
                st.error("Todos os campos são obrigatórios.")
            else:
                id_universidade = opcoes_universidade[uni_selecionada_nome]
                id_departamento = opcoes_departamento[depto_selecionado_nome]

                docente_data = {
                    "cpf": cpf, "nome": nome, "senha": senha, "email": email, "matricula": matricula,
                    "id_universidade": id_universidade,
                    "id_departamento": id_departamento,
                    "especialidade": especialidade,
                    "permissao_validacao": permissao_validacao
                }
                
                try:
                    response = requests.post(f"{API_URL}/usuarios/docente", json=docente_data)
                    if response.status_code == 201:
                        st.success("Docente cadastrado com sucesso!")
                        st.json(response.json())
                    else:
                        st.error(f"Erro ao cadastrar docente: {response.status_code}")
                        st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão com a API: {e}")