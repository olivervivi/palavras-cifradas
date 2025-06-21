import streamlit as st
import time
from datetime import datetime

from core.auth.security import hash_senha_usuario, is_password_strong
from core.storage.user_db import load_users, save_users

def registration_page():
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f7;
                color: #2b2b2b;
                font-family: 'Segoe UI', sans-serif;
            }

            .block-container {
                border-radius: 12px;
                padding: 2rem 2rem;
            }

            h1 {
                color: #F6A100;
                text-align: center;
            }

            .info-box {
                max-width: 700px;
                margin: 30px auto;
                padding: 20px;
                border-radius: 12px;
                background-color: #fff9ec;
                border: 1px solid #f6d773;
            }

            div.stButton > button, div.stForm button {
                background-color: #f6d773;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
                font-size: 1rem;
                transition: background-color 0.3s ease;
            }

            div.stButton > button:hover, div.stForm button:hover {
                background-color: #f2c84d;
                color: #000;
            }

            input[type="text"], input[type="password"] {
                border-radius: 8px !important;
                padding: 0.5rem;
                font-size: 1rem;
                border: 1px solid #ccc;
            }

            .rodape {
                text-align: center;
                margin-top: 50px;
                font-size: 0.8rem;
                color: #888;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>📝 Criar Nova Conta</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Preencha os campos para criar uma nova conta.</p>", unsafe_allow_html=True)

    with st.form("register_form"):
        novo_usuario = st.text_input("👤 Nome de usuário", key="register_user_input")
        nova_senha = st.text_input("🔐 Senha", type="password", key="register_pass_input")
        confirmar_senha = st.text_input("🔁 Confirmar senha", type="password", key="confirm_pass_input")

        st.markdown("""
        <div style="font-size: 0.9rem; color: #555; background-color: #fff7d0;
             border-left: 4px solid #f6c300; padding: 10px; border-radius: 6px; margin-top: 5px;">
        🔐 <b>Dica de segurança:</b><br>
        Use uma palavra-passe que misture <b>letras</b>, <b>números</b> e <b>símbolos especiais</b>.<br>
        💡 <i>Exemplo seguro:</i> <code>amor@2025</code>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🧠 Por que isso importa?"):
            st.markdown("""
            Senhas simples como <code>123456</code> são as primeiras testadas por programas automáticos.<br><br>
            Ao usar letras, números e símbolos, você aumenta a proteção dos seus dados.<br>
            Isso é um dos pilares da segurança digital moderna — e agora faz parte do seu app.
            """)

        registrar = st.form_submit_button("Cadastrar")

    if registrar:
        u_clean = novo_usuario.lower().strip()
        s_clean = nova_senha.strip()
        users_db = load_users()
        is_strong, message = is_password_strong(s_clean)

        if not u_clean or not s_clean:
            st.warning("Utilizador e senha são obrigatórios.")
        elif u_clean in users_db or u_clean in ["admin", "padrao", "premium"]:
            st.error("Este nome de utilizador já existe ou é reservado.")
        elif s_clean != confirmar_senha.strip():
            st.error("As senhas não coincidem.")
        elif not is_strong:
            st.error(f"Senha fraca: {message}\n\n💡 Exemplo seguro: amor@2025")
        else:
            try:
                users_db[u_clean] = {"password": hash_senha_usuario(s_clean), "role": "standard"}
                save_users(users_db)
                st.success(f"✅ Utilizador '{u_clean}' registado com sucesso!")
                st.info("Agora pode voltar à página de login para entrar.")
                time.sleep(1)
                st.session_state.current_page = "auth"
                st.rerun()
            except Exception as e:
                st.error("❌ Não foi possível registar o utilizador.")
                st.exception(e)

    st.markdown("---")
    if st.button("⬅️ Voltar ao Login", key="back_to_login_btn"):
        st.session_state.current_page = "auth"
        st.rerun()

    st.markdown("""
        <div class="rodape">
            &copy; 2025 Viviane de Oliveira — Todos os direitos reservados. Este projeto é protegido pela licença CC BY‑NC.
        </div>
    """, unsafe_allow_html=True)

