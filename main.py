import streamlit as st
import time
from datetime import datetime

# ✅ Define título da aba do navegador
st.set_page_config(
    layout="wide",
    page_title="Palavras Cifradas",
    page_icon="🔐"
)

# ✅ CSS para fixar o menu lateral visualmente com cor fixa e harmônica
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        overflow-y: auto;
        background-color: #fff8e1; /* cor clara inspirada no dourado */
        border-right: 2px solid #F6A100;
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        z-index: 999;
    }

    .main {
        margin-left: 18rem;
        padding: 2rem;
    }

    .block-container {
        padding-top: 2rem;
    }

    button {
        background-color: #f6d773 !important;
        color: #2b2b2b !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 6px 12px !important;
        font-weight: bold;
    }

    button:hover {
        background-color: #f2c84d !important;
        color: #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Importações de configuração e módulos principais
from app.logic.session_manager import initialize_session_state, get_active_role, sidebar_navigation
from app.logic.ui_styles import apply_app_styling
from core.storage.user_db import load_users

# Importações das páginas
from app.pages.auth_page import auth_page
from app.pages.registration_page import registration_page 
from app.pages.home_page import home_page
from app.pages.text_encryption_page import text_encryption_page
from app.pages.audio_encrypt_page import audio_encrypt_page
from app.pages.audio_decrypt_novo import audio_decrypt_novo
from app.pages.file_folder_encryption_page import file_folder_encryption_page
from app.pages.premium_plan_page import premium_plan_page
from app.pages.admin_panel_page import admin_panel_page
from app.pages.auditoria_usuario_page import auditoria_usuario_page
from app.pages.documentacao_page import documentacao_page 
from app.pages.recovery_page import recovery_page 
from app.pages.manual_instrucoes_page import manual_instrucoes_page
from app.pages.link_generator_page import link_generator_page  # ✅ Página nova corretamente adicionada

# ==============================================================================

def main():
    initialize_session_state()
    load_users()

    if st.session_state.get("refresh"):
        st.session_state.refresh = False
        st.rerun()

    apply_app_styling()

    # ✅ Mapeamento correto: chave interna usada na navegação precisa ser "link_generator"
    PAGES = {
        "auth": auth_page,
        "register": registration_page,
        "home": home_page,
        "text_encryption": text_encryption_page,
        "audio_encrypt": audio_encrypt_page,
        "audio_decrypt": audio_decrypt_novo,
        "file_folder_encryption": file_folder_encryption_page,
        "premium_plan": premium_plan_page,
        "admin_panel": admin_panel_page,
        "auditoria_usuario": auditoria_usuario_page,
        "documentacao": documentacao_page,
        "recovery_password": recovery_page,
        "manual_instrucoes": manual_instrucoes_page,
        "link_generator": link_generator_page  # ✅ Corrigido aqui — esse nome precisa bater com a chamada do botão
    }

    # Exibe o menu lateral e seleciona a página
    if st.session_state.current_page not in ["auth", "register", "recovery_password"]:
        sidebar_navigation(PAGES)

    # Executa a função da página selecionada
    page_function = PAGES.get(st.session_state.current_page, auth_page)
    page_function()

# ✅ Adiciona rodapé centralizado uma única vez
if __name__ == "__main__":
    main()
    st.markdown("""
        <div style='text-align: center; font-size: 0.85rem; color: gray; padding-top: 2rem;'>
            &copy; 2025 Viviane de Oliveira — Todos os direitos reservados. Este projeto é protegido pela licença CC BY‑NC.
        </div>
    """, unsafe_allow_html=True)
