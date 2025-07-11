from datetime import date
import streamlit as st
import requests
import pandas as pd
import base64
import math


API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="UnB Archive",
    page_icon="📚",
    layout="wide"
)

if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None
if 'materiais_completos' not in st.session_state:
    st.session_state.materiais_completos = []

# --- FUNÇÕES AUXILIARES ---

def buscar_dados_api(endpoint: str):
    """Função genérica para buscar listas de dados de um endpoint da API."""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Retorna None em caso de erro 404 para ser tratado
        if e.response and e.response.status_code == 404:
            return None
        st.error(f"Não foi possível buscar dados de '{endpoint}': {e}")
        return []

def buscar_nome_por_id(endpoint: str, item_id: int):
    """Busca o nome de um item específico pelo seu ID."""
    if not item_id or not isinstance(item_id, int):
        return "N/A"
    try:
        response = requests.get(f"{API_URL}/{endpoint}/{item_id}", timeout=5)
        if response.status_code == 200:
            return response.json().get("nome", response.json().get("nome_tag", "ID não encontrado"))
        return f"ID {item_id} não encontrado"
    except requests.exceptions.RequestException:
        return f"Erro ao buscar ID {item_id}"

@st.cache_data(ttl=60)
def buscar_reputacao_por_cpf(cpf: str):
    """Busca os detalhes de uma reputação específica pelo CPF do usuário."""
    if not cpf:
        return None
    return buscar_dados_api(f"reputacao/usuario/{cpf}")


@st.cache_data(ttl=60) # Cache para otimizar performance
def get_validation_status_for_material(material_id: int) -> str:
    """Busca o status de validação de um material fazendo uma chamada à API."""
    if not material_id:
        return "pendente"
    
    validations = buscar_dados_api(f"avalia/material/{material_id}")
    if not validations:
        return "pendente"
    
    if any(not v.get('valido', True) for v in validations):
        return "invalido"
    
    if any(v.get('valido', True) for v in validations):
        return "validado"
        
    return "pendente"

def gerar_estrelas_display(media: float, max_estrelas: int = 5) -> str:
    """Converte uma nota média em uma string de emojis de estrelas para exibição."""
    if media is None or not isinstance(media, (int, float)) or media < 0:
        return "N/A"
    estrelas_cheias = round(media)
    estrelas_vazias = max_estrelas - estrelas_cheias
    return "★" * estrelas_cheias + "☆" * estrelas_vazias

# --- LÓGICA DA APLICAÇÃO ---

# Tela de Login se o usuário não estiver logado
if not st.session_state.get('user_info'):
    st.title("🔑 Acessar o Sistema UNB Archive")
    with st.form("login_form"):
        cpf = st.text_input("CPF do Usuário", placeholder="Digite o CPF de um usuário cadastrado")
        submitted = st.form_submit_button("Acessar")
        if submitted and cpf:
            try:
                response = requests.get(f"{API_URL}/usuarios/discente/{cpf}")
                if response.status_code == 404:
                    response = requests.get(f"{API_URL}/usuarios/docente/{cpf}")
                if response.status_code == 200:
                    st.session_state['user_info'] = response.json()
                    st.success("Usuário encontrado! Acessando o sistema...")
                    st.rerun()
                else:
                    st.error("Usuário não encontrado. Verifique o CPF digitado.")
            except requests.RequestException as e:
                st.error(f"Erro de conexão com a API: {e}")
        elif submitted:
            st.error("Por favor, insira um CPF.")

# Interface Principal após o login
else:
    user_info = st.session_state.get('user_info', {})
    is_docente = 'especialidade' in user_info
    is_discente = 'coeficiente_rendimento' in user_info

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"🏠 Bem-vindo(a) ao UnB Archive!")
        user_display = user_info.get('nome', 'Usuário')
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
                disciplina_selecionada = st.selectbox("Disciplina", options=list(opcoes_disciplina.keys()))
                ano_semestre = st.text_input("Ano/Semestre (ex: 2024/2)")
            with form_col2:
                tags_selecionadas = st.multiselect("Tags", options=list(opcoes_tag.keys()))
                arquivo = st.file_uploader("Selecione o arquivo")
            descricao = st.text_area("Descrição (opcional)")
            submitted = st.form_submit_button("Enviar Material")

            if submitted:
                if arquivo is not None and nome_material and disciplina_selecionada:
                    id_disciplina = opcoes_disciplina.get(disciplina_selecionada)
                    files = {'arquivo': (arquivo.name, arquivo.getvalue(), arquivo.type)}
                    material_data = {
                        "nome": nome_material, "descricao": descricao, 
                        "id_disciplina": id_disciplina, "ano_semestre_ref": ano_semestre
                    }
                    try:                       
                        response = requests.post(f"{API_URL}/material/upload", data=material_data, files=files)
                        response.raise_for_status() # Lança erro se não for 2xx

                        st.success("Material enviado com sucesso! Vinculando ao seu perfil...")
                        
                        material_criado = response.json()
                        id_material_novo = material_criado.get('id_material')
                        cpf_usuario_logado = user_info.get('cpf')

                        if id_material_novo and cpf_usuario_logado:
                            try:
                                payload_associacao = {
                                    "id_material": id_material_novo,
                                    "cpf_usuario": cpf_usuario_logado
                                }
                                assoc_response = requests.post(f"{API_URL}/associacoes", json=payload_associacao)
                                assoc_response.raise_for_status()
                                st.success("Vínculo entre usuário e material criado com sucesso!")

                            except requests.RequestException as assoc_e:
                                st.warning(f"Material foi criado, mas falha ao criar o vínculo: {assoc_e.response.text if assoc_e.response else assoc_e}")
                        else:
                            st.warning("Material criado, mas não foi possível obter os dados para criar o vínculo.")

                    except requests.RequestException as e:
                        st.error(f"Erro no upload: {e.response.text if e.response else e}")
                else:
                    st.warning("Por favor, preencha todos os campos obrigatórios e selecione um arquivo.")

    with tab2:
        st.header("📚 Materiais Disponíveis")

        def handle_rating_click(material_id, nota_clicada):
            try:
                payload = {"data_avaliacao": date.today().isoformat(), "nota": float(nota_clicada), "id_material": material_id}
                response = requests.post(f"{API_URL}/avaliacoes", json=payload)
                response.raise_for_status()
                st.toast(f"Sua avaliação de {nota_clicada} estrelas foi registrada!", icon="✅")
                st.session_state.materiais_completos = []
            except requests.RequestException as e:
                st.error(f"Erro ao registrar avaliação: {e.response.text if e.response else e}")

        def handle_validation_click(material_id, is_valid_action):
            try:
                payload = {"id_material": material_id, "cpf_docente": user_info['cpf'], "acao_valida": is_valid_action}
                response = requests.post(f"{API_URL}/procedures/gerenciar-validacao", json=payload)
                response.raise_for_status()
                action_text = "validado" if is_valid_action else "invalidado"
                st.toast(f"Material {action_text} com sucesso!", icon="👍")
                st.session_state.materiais_completos = []
            except requests.RequestException as e:
                st.error(f"Erro ao validar: {e.response.json().get('detail', e)}")

        if not st.session_state.materiais_completos or st.button("Atualizar Lista de Materiais"):
            st.session_state.materiais_completos = buscar_dados_api("relatorios/materiais-completos")

        if st.session_state.materiais_completos:
            st.write(f"Total de materiais encontrados: {len(st.session_state.materiais_completos)}")
            
            col_headers = ["Nome", "Disciplina", "Semestre", "Média", "Avalie Agora!", "Status / Ação", "Baixar"]
            col_widths = [3, 2.5, 1, 1.5, 2, 2, 1.5]
            
            cols = st.columns(col_widths)
            for col, header in zip(cols, col_headers):
                col.subheader(header)
            
            st.markdown("---")

            for material in st.session_state.materiais_completos:
                id_material = material.get('id_material')
                status_validacao = get_validation_status_for_material(id_material)
                is_invalid = (status_validacao == 'invalido')
                
                cols = st.columns(col_widths)
                
                with cols[0]:
                    nome_material = material.get("material_nome", "N/A")
                    if is_invalid:
                        st.markdown(f":red[{nome_material}]")
                    else:
                        st.write(nome_material)

                cols[1].write(material.get("disciplina_nome", "N/A"))
                cols[2].write(material.get("ano_semestre_ref", "N/A"))
                
                media_geral = material.get("media_avaliacoes", 0)
                cols[3].write(f"{gerar_estrelas_display(media_geral)} ({media_geral:.1f})")
                
                with cols[4]:
                    star_cols = st.columns(5)
                    for i in range(5):
                        with star_cols[i]:
                            st.button("☆", key=f"star_{i+1}_{id_material}", on_click=handle_rating_click, args=(id_material, i + 1), disabled=is_invalid)
                
                with cols[5]:
                    if is_docente:
                        validation_cols = st.columns(2)
                        with validation_cols[0]:
                            st.button("✔️", key=f"validar_{id_material}", help="Validar", on_click=handle_validation_click, args=(id_material, True), disabled=is_invalid)
                        with validation_cols[1]:
                            st.button("❌", key=f"invalidar_{id_material}", help="Invalidar", on_click=handle_validation_click, args=(id_material, False), disabled=is_invalid)
                    else:
                        if status_validacao == 'validado':
                            st.markdown("✅ :green[Válido]")
                        elif status_validacao == 'invalido':
                            st.markdown("❌ :red[Inválido]")
                        else:
                            st.markdown("⏳ :orange[Em análise]")
                
                with cols[6]:
                    if st.button("⬇️", key=f"download_{id_material}", help="Baixar arquivo" if not is_invalid else "Download desabilitado para material inválido", disabled=is_invalid):
                        try:
                            res_download = requests.get(f"{API_URL}/material/{id_material}/download")
                            if res_download.status_code == 200:
                                file_name = f"{material.get('material_nome', 'arquivo')}.pdf"
                                b64 = base64.b64encode(res_download.content).decode()
                                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Clique para baixar</a>'
                                st.markdown(href, unsafe_allow_html=True)
                            else:
                                st.error(f"Erro: {res_download.status_code}")
                        except requests.RequestException as e:
                            st.error(f"Erro de conexão: {e}")

        else:
            st.info("Nenhum material disponível no momento.")

    with tab3:
        st.header("👥 Gerenciar Usuários")
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
        if user_info:
            
            if is_discente:
                st.subheader("Minha Reputação")
                reputacao_info = buscar_reputacao_por_cpf(user_info['cpf'])
                
                if reputacao_info:
                    rep_col1, rep_col2 = st.columns(2)
                    rep_col1.metric(label="Nível de Reputação", value=reputacao_info.get('nivel', 'N/A'))
                    rep_col2.metric(label="Pontuação Total", value=str(reputacao_info.get('pontuacao', 0)))
                else:
                    st.info("Você ainda não possui uma reputação. Comece a interagir para construir a sua!")
                st.markdown("---")

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
                st.warning("**Atenção:** Esta ação é permanente e não pode ser desfeita.")
                confirmation_check = st.checkbox("Eu entendo as consequências e desejo excluir minha conta.")
                if confirmation_check:
                    if st.button("Excluir meu perfil permanentemente", type="primary"):
                        try:
                            user_cpf = user_info.get('cpf')
                            response = requests.delete(f"{API_URL}/usuarios/{cpf}")
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
