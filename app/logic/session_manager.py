import streamlit as st
from app.utils.ui_utils import limpar_tudo_geral

def initialize_session_state():
    defaults = {
        "current_page": "auth",
        "user_role": "guest",
        "logged_in_user": "",
        "historico": [],
        "decrypted_audio_data": None,
        "uploaded_audio_bytes": None,
        "resultado_xor": "",
        "resultado_aes": "",
        "contador_operacoes": {"XOR": 0, "AES": 0, "File": 0},
        "simular_papel": None,
        "tentativas_login": 0,
        "refresh": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_active_role() -> str:
    return st.session_state.get("simular_papel") or st.session_state.get("user_role")

def navigate_safe(page_name: str):
    st.session_state.current_page = page_name
    st.session_state.refresh = True
    st.stop()

def sidebar_navigation(pages_map: dict):
    with st.sidebar:
        st.header(f"Olá, {st.session_state.logged_in_user}!")
        active_role = get_active_role()
        st.subheader("Navegação")

        st.caption(f"🔎 Papel ativo: **{active_role}**")

        if st.button("🏠 Painel de Controle", key="nav_home_btn"):
            navigate_safe("home")
            
        if st.button("✍️ Criptografar/Descriptografar Texto", key="nav_text_encryption_btn"):
            navigate_safe("text_encryption")

        # Início do bloco de restrição Premium/Admin
        if active_role in ["premium", "admin"]:
            if st.button("📦 Arquivos e Pastas", key="nav_file_folder_encryption_btn"):
                navigate_safe("file_folder_encryption")
            if st.button("🔒 Criptografar Áudio", key="nav_audio_encrypt_btn"):
                navigate_safe("audio_encrypt")
            
            # AQUI ESTAVA O ERRO "DESCRITIVO", JÁ ARRUMEI:
            if st.button("🔓 Descriptografar Áudio", key="nav_audio_decrypt_btn"):
                navigate_safe("audio_decrypt")
                
            if st.button("📊 Minhas Atividades", key="nav_auditoria_usuario_btn"):
                navigate_safe("auditoria_usuario")
            if st.button("🔗 Gerar Link Compartilhável", key="nav_link_generator_btn"):
                navigate_safe("link_generator")
        else:
            # Opção para usuários que não possuem acesso total
            if st.button("✨ Fazer Upgrade para Premium", key="nav_premium_plan_btn"):
                navigate_safe("premium_plan")

        if active_role == "admin":
            st.markdown("---")
            if st.button("👑 Gerenciar Usuários", use_container_width=True, key="nav_admin_panel_btn"):
                navigate_safe("admin_panel")

        if st.session_state.user_role == "admin":
            st.markdown("---")
            st.subheader("🧪 Modo de Simulação")
            roles = ["admin", "premium", "standard"]
            current_display_role = get_active_role()
            index = roles.index(current_display_role) if current_display_role in roles else 0
            perfil_simulado_novo = st.selectbox("Acessar como:", options=roles, index=index, key="sim_role_select")

            if perfil_simulado_novo != current_display_role:
                st.session_state.simular_papel = (
                    perfil_simulado_novo
                    if perfil_simulado_novo != st.session_state.user_role else None
                )
                navigate_safe(st.session_state.current_page)

        st.markdown("---")
        st.button("🧼 Limpar Tudo Geral", on_click=limpar_tudo_geral, use_container_width=True, key="clear_all_btn")

        if st.button("🚪 Sair (Logout)", key="logout_button"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            initialize_session_state()
            navigate_safe("auth")

        st.markdown("---")
        st.subheader("Informações")
        if st.button("📘 Documentação Técnica", key="nav_documentacao_btn"):
            navigate_safe("documentacao")
        if st.button("📚 Manual de Instruções", key="nav_manual_instrucoes_btn"):
            navigate_safe("manual_instrucoes")