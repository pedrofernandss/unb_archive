import streamlit as st
import requests
import pandas as pd
import base64 # Para futuras funcionalidades de download

API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="UnB Archive",
    page_icon="📚",
    layout="wide"
)

if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

def buscar_dados_api(endpoint: str):
    """Função genérica para buscar listas de dados de um endpoint da API."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível buscar dados de '{endpoint}': {e}")
        return []

def buscar_nome_por_id(endpoint: str, item_id: int):
    """Busca o nome de um item específico pelo seu ID."""
    if not item_id:
        return "N/A"
    try:
        response = requests.get(f"{API_URL}/{endpoint}/{item_id}")
        if response.status_code == 200:
            return response.json().get("nome", "ID não encontrado")
        return f"ID {item_id} não encontrado"
    except requests.exceptions.RequestException:
        return f"Erro ao buscar ID {item_id}"

if not st.session_state.get('user_info'):
    st.title("🔑 Acessar o Sistema UNB Archive")
    st.write("Para acessar, por favor, identifique-se com seu CPF.")

    with st.form("login_form"):
        cpf = st.text_input("CPF do Usuário", placeholder="Digite o CPF de um usuário cadastrado")
        submitted = st.form_submit_button("Acessar")
        
        if submitted:
            if not cpf:
                st.error("Por favor, insira um CPF.")
            else:
                try:
                    response = requests.get(f"{API_URL}/usuarios/{cpf}")
                    if response.status_code == 200:
                        st.session_state['user_info'] = response.json()
                        st.success("Usuário encontrado! Acessando o sistema...")
                        st.rerun()
                    elif response.status_code == 404:
                        st.error("Usuário não encontrado. Verifique o CPF digitado.")
                    else:
                        st.error(f"Erro ao buscar usuário: {response.status_code}")
                        st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão com a API: {e}")

    with st.form("login_form_universidade"):
        id_universidade = st.text_input("IES da Universidade", placeholder="Digite aqui o IES da sua Universidade")
        submitted = st.form_submit_button("Acessar")
        
        if submitted:
            if not id_universidade:
                st.error("Por favor, insira o IES da Universidade.")
            else:
                try:
                    response = requests.get(f"{API_URL}/universidade/{id_universidade}")
                    if response.status_code == 200:
                        st.session_state['user_info'] = response.json()
                        st.success("Universidade encontrada! Acessando o sistema...")
                        st.rerun()
                    elif response.status_code == 404:
                        st.error("Universidade não encontrada. Verifique o IES digitado.")
                    else:
                        st.error(f"Erro ao buscar universidade: {response.status_code}")
                        st.json(response.json())
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão com a API: {e}")

else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"🏠 Bem-vindo(a) ao UnB Archive!")
        user_display = st.session_state.get('user_info', {}).get('nome', 'Usuário')
        st.subheader(f"Logado como: **{user_display}**")
    with col2:
        if st.button("Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload de Material", "📚 Materiais Disponíveis", "👥 Gerenciar Usuários", "👤 Meu Perfil"])

    with tab1:
        st.header("📤 Enviar Novo Material de Estudo")
        
        disciplinas = buscar_dados_api("disciplina")
        tags = buscar_dados_api("tag")
        opcoes_disciplina = {d['nome']: d['codigo'] for d in disciplinas} if disciplinas else {}
        opcoes_tag = {t['nome_tag']: t['id_tag'] for t in tags} if tags else {}

        with st.form("form_upload", clear_on_submit=True):
            st.info("Preencha os detalhes do material e anexe o arquivo.")
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                nome_material = st.text_input("Nome do Material")
                disciplina_selecionada = st.selectbox("Disciplina", options=opcoes_disciplina.keys())
                ano_semestre = st.text_input("Ano/Semestre (ex: 2024/2)")
            with form_col2:
                tags_selecionadas = st.multiselect("Tags", options=opcoes_tag.keys())
                arquivo = st.file_uploader("Selecione o arquivo")
            descricao = st.text_area("Descrição (opcional)")
            submitted = st.form_submit_button("Enviar Material")

            if submitted:
                if arquivo is not None:
                    id_disciplina = opcoes_disciplina.get(disciplina_selecionada)
                    files = {'arquivo': (arquivo.name, arquivo.getvalue(), arquivo.type)}
                    material_data = {
                        "nome": nome_material, "descricao": descricao, 
                        "id_disciplina": id_disciplina, "ano_semestre_ref": ano_semestre
                    }
                    try:
                        response = requests.post(f"{API_URL}/material/", data=material_data, files=files)
                        if response.status_code == 201:
                            st.success("Material enviado com sucesso!")
                        else:
                            st.error(f"Erro no upload: {response.status_code} - {response.text}")
                    except requests.RequestException as e:
                        st.error(f"Erro de conexão: {e}")
                else:
                    st.warning("Por favor, selecione um arquivo para enviar.")

    with tab2:
        st.header("📚 Materiais Disponíveis")
        if st.button("Atualizar Lista de Materiais"):
            st.rerun()

        materiais = buscar_dados_api("material")
        if materiais:
            st.write(f"Total de materiais encontrados: {len(materiais)}")
            col_nome, col_disciplina, col_semestre, col_download = st.columns([3, 3, 2, 2])
            with col_nome: st.subheader("Nome do Material")
            with col_disciplina: st.subheader("Disciplina")
            with col_semestre: st.subheader("Semestre")
            with col_download: st.subheader("Ação")
            
            st.markdown("---")

            for material in materiais:
                col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
                with col1:
                    st.write(material.get("nome", "N/A"))
                with col2:
                    
                    id_disciplina = material.get("id_disciplina")
                    nome_disciplina = buscar_nome_por_id("disciplina", id_disciplina)
                    st.write(nome_disciplina)
                with col3:
                    st.write(material.get("ano_semestre_ref", "N/A"))
                with col4:
                    
                    id_material = material.get('id_material')

                    if st.button("Baixar", key=f"download_{id_material}", use_container_width=True):
                        try:

                            res_download = requests.get(f"{API_URL}/material/{id_material}/download")
                            if res_download.status_code == 200:
                                file_name = f"{material.get('nome', 'arquivo')}.pdf"
                                
                                b64 = base64.b64encode(res_download.content).decode()
                                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Clique aqui para baixar "{file_name}"</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success("Link de download gerado!")
                            else:
                                st.error(f"Não foi possível obter o arquivo. Erro: {res_download.status_code}")
                        except requests.RequestException as e:
                            st.error(f"Erro de conexão ao tentar baixar: {e}")
        else:
            st.info("Nenhum material disponível no momento.")

    with tab3:
        st.header("👥 Lista de Usuários do Sistema")
        if st.button("Carregar Lista de Usuários"):
            usuarios = buscar_dados_api("usuarios")
            if usuarios:
                st.write(f"Total de usuários encontrados: {len(usuarios)}")
                
                col_nome, col_email, col_uni, col_depto = st.columns(4)
                with col_nome: st.subheader("Nome")
                with col_email: st.subheader("Email")
                with col_uni: st.subheader("Universidade")
                with col_depto: st.subheader("Departamento")
                st.markdown("---")

                for usuario in usuarios:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(usuario.get("nome"))
                    with col2:
                        st.write(usuario.get("email"))
                    with col3:
                        id_universidade = usuario.get("id_universidade")
                        nome_universidade = buscar_nome_por_id("universidade", id_universidade)
                        st.write(nome_universidade)
                    with col4:
                        id_departamento = usuario.get("id_departamento")
                        nome_departamento = buscar_nome_por_id("departamento", id_departamento)
                        st.write(nome_departamento)
            else:
                st.info("Nenhum usuário encontrado.")
    
    with tab4:
        st.header("👤 Gerenciar Meu Perfil")

        user_info = st.session_state.get('user_info')

        if user_info:
            with st.expander("✏️ Editar minhas informações", expanded=True):
                
                universidades = buscar_dados_api("universidade")
                departamentos = buscar_dados_api("departamento")

                opcoes_universidade = {uni['nome']: uni['ies'] for uni in universidades} if universidades else {}
                opcoes_departamento = {depto['nome']: depto['id_departamento'] for depto in departamentos} if departamentos else {}
                
                uni_by_id = {v: k for k, v in opcoes_universidade.items()}
                depto_by_id = {v: k for k, v in opcoes_departamento.items()}

                with st.form("edit_profile_form"):
                    st.write("Altere apenas os campos que deseja modificar.")
                    
                    novo_nome = st.text_input("Nome", value=user_info.get('nome', ''))
                    novo_email = st.text_input("Email", value=user_info.get('email', ''))
                    
                    lista_nomes_uni = list(opcoes_universidade.keys())
                    current_uni_id = user_info.get('id_universidade')
                    default_uni_index = lista_nomes_uni.index(uni_by_id.get(current_uni_id)) if current_uni_id in uni_by_id else 0
                    
                    lista_nomes_depto = list(opcoes_departamento.keys())
                    current_depto_id = user_info.get('id_departamento')
                    default_depto_index = lista_nomes_depto.index(depto_by_id.get(current_depto_id)) if current_depto_id in depto_by_id else 0

                    nova_universidade_nome = st.selectbox("Universidade", options=lista_nomes_uni, index=default_uni_index)
                    novo_departamento_nome = st.selectbox("Departamento", options=lista_nomes_depto, index=default_depto_index)

                    nova_senha = st.text_input("Nova Senha (deixe em branco para não alterar)", type="password")
                    
                    edit_submitted = st.form_submit_button("Salvar Alterações")

                    if edit_submitted:
                        update_data = {}
                        if novo_nome != user_info.get('nome'):
                            update_data['nome'] = novo_nome
                        if novo_email != user_info.get('email'):
                            update_data['email'] = novo_email
                        if nova_senha: 
                            update_data['senha'] = nova_senha
                        
                        novo_id_uni = opcoes_universidade.get(nova_universidade_nome)
                        if novo_id_uni != user_info.get('id_universidade'):
                            update_data['id_universidade'] = novo_id_uni
                        
                        novo_id_depto = opcoes_departamento.get(novo_departamento_nome)
                        if novo_id_depto != user_info.get('id_departamento'):
                            update_data['id_departamento'] = novo_id_depto

                        if not update_data:
                            st.warning("Nenhuma alteração detectada.")
                        else:
                            try:
                                user_cpf = user_info.get('cpf')
                                response = requests.patch(f"{API_URL}/usuarios/{user_cpf}", json=update_data)
                                if response.status_code == 200:
                                    st.success("Perfil atualizado com sucesso!")
                                    st.session_state['user_info'] = response.json()
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao atualizar: {response.status_code}")
                                    st.json(response.json())
                            except requests.RequestException as e:
                                st.error(f"Erro de conexão: {e}")

            st.markdown("---")

            with st.expander("🗑️ Excluir minha conta"):
                st.warning("**Atenção:** Esta ação é permanente e não pode ser desfeita. Todos os seus dados serão apagados.")
                
                confirmation_check = st.checkbox("Eu entendo as consequências e desejo excluir minha conta.")
                
                if confirmation_check:
                    if st.button("Excluir meu perfil permanentemente", type="primary"):
                        try:
                            user_cpf = user_info.get('cpf')
                            response = requests.delete(f"{API_URL}/usuarios/{user_cpf}")
                            
                            if response.status_code == 204:
                                st.success("Sua conta foi excluída com sucesso. Você será desconectado.")
                                for key in st.session_state.keys():
                                    del st.session_state[key]
                                st.rerun()
                            else:
                                st.error(f"Não foi possível excluir a conta: {response.status_code}")
                                st.json(response.json())
                        except requests.RequestException as e:
                            st.error(f"Erro de conexão: {e}")
        else:
            st.error("Não foi possível carregar as informações do perfil.")
