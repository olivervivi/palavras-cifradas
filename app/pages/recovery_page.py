import streamlit as st
import time
from datetime import datetime, timedelta

from core.auth.security import generate_recovery_token, store_recovery_token, verify_recovery_token, hash_senha_usuario, is_password_strong
from core.storage.user_db import load_users, save_users
from core.utils.email_utils import send_email

ADMIN_EMAIL = "vivi-oliver-nh@hotmail.com"

def recovery_page():
    st.markdown("""
        <style>
            body {
                background-color: #f5f5f7;
                color: #2b2b2b;
                font-family: 'Segoe UI', sans-serif;
            }

            .block-container {
                border-radius: 12px;
                padding: 2rem;
            }

            h1, h2, h3, h4, h5, h6 {
                color: #F6A100;
                text-align: center;
            }

            div.stButton > button {
                background-color: #f6d773;
                color: #2b2b2b;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }

            div.stButton > button:hover {
                background-color: #f2c84d;
            }

            input[type="text"], input[type="password"] {
                border-radius: 8px !important;
                padding: 0.5rem;
                border: 1px solid #ccc;
                font-size: 1rem;
            }

            .rodape {
                text-align: center;
                margin-top: 50px;
                font-size: 0.8rem;
                color: #888;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔑 Recuperação de Senha")
    st.markdown("Use esta página para recuperar sua senha de administrador.")

    if "recovery_stage" not in st.session_state:
        st.session_state.recovery_stage = "request_email"

    if st.session_state.recovery_stage == "request_email":
        st.subheader("1. Solicitar Token de Recuperação")
        username_input = st.text_input("👤 Nome de usuário (admin):", key="recovery_user_input")

        if st.button("📧 Enviar Link de Recuperação", key="send_recovery_link_btn"):
            if not username_input:
                st.warning("Digite seu nome de usuário.")
            else:
                users_db = load_users()
                user_info = users_db.get(username_input.lower().strip())

                if user_info and user_info.get("role") == "admin":
                    token = generate_recovery_token(username_input.lower().strip())
                    store_recovery_token(username_input.lower().strip(), token)

                    recovery_link = f"Por favor, use este token para resetar sua senha: {token}\n\nO token é válido por 15 minutos."

                    if send_email(
                        ADMIN_EMAIL,
                        "Recuperação de Senha - Palavras Cifradas",
                        f"Olá {username_input},\n\nUma solicitação de recuperação de senha foi iniciada.\n\n{recovery_link}\n\nSe não foi você, ignore este e-mail."
                    ):
                        st.success(f"Token enviado para {ADMIN_EMAIL}. Verifique sua caixa de entrada e spam.")
                        st.session_state.recovery_stage = "enter_token"
                        st.session_state.recovery_username = username_input.lower().strip()
                        st.rerun()
                    else:
                        st.error("Falha ao enviar o e-mail de recuperação.")
                else:
                    st.error("Usuário não encontrado ou não é administrador.")

    elif st.session_state.recovery_stage == "enter_token":
        st.subheader("2. Inserir Token e Nova Senha")
        st.info("Verifique seu e-mail para o token de recuperação.")

        token_input = st.text_input("🔑 Token de recuperação:", key="token_input")
        new_password = st.text_input("🔒 Nova senha:", type="password", key="new_password_input")
        confirm_password = st.text_input("🔁 Confirmar nova senha:", type="password", key="confirm_new_password_input")

        if st.button("✅ Redefinir Senha", key="reset_password_btn"):
            req_username = st.session_state.get("recovery_username")
            if not req_username:
                st.error("Erro: usuário não identificado. Reinicie o processo.")
                st.session_state.recovery_stage = "request_email"
                st.rerun()

            if not token_input or not new_password or not confirm_password:
                st.warning("Preencha todos os campos.")
            elif new_password != confirm_password:
                st.error("As senhas não coincidem.")
            else:
                is_strong, msg = is_password_strong(new_password)
                if not is_strong:
                    st.error(f"Senha fraca: {msg}")
                elif verify_recovery_token(req_username, token_input):
                    users_db = load_users()
                    users_db[req_username]["password"] = hash_senha_usuario(new_password)
                    save_users(users_db)
                    st.success("Senha redefinida com sucesso!")
                    st.session_state.recovery_stage = "done"
                    st.rerun()
                else:
                    st.error("Token inválido ou expirado.")

    elif st.session_state.recovery_stage == "done":
        st.success("Recuperação concluída.")
        st.info("Sua senha foi atualizada. Volte ao login para acessar sua conta.")
        if st.button("⬅️ Voltar ao Login", key="back_to_login_after_recovery_btn"):
            st.session_state.current_page = "auth"
            st.rerun()

    if st.session_state.recovery_stage != "done" and st.button("⬅️ Cancelar e Voltar ao Login", key="cancel_recovery_btn"):
        st.session_state.current_page = "auth"
        del st.session_state["recovery_stage"]
        if st.session_state.get("recovery_username"):
            del st.session_state[f"recovery_token_{st.session_state.recovery_username}"]
            del st.session_state["recovery_username"]
        st.rerun()

    st.markdown("""
        <div class="rodape">
            &copy; 2025 Viviane de Oliveira — Todos os direitos reservados. Este projeto é protegido pela licença CC BY-NC.
        </div>
    """, unsafe_allow_html=True)