import streamlit as st
import time
from datetime import datetime, timedelta

from core.auth.security import verify_senha_usuario
from core.storage.user_db import load_users, save_users
from core.utils.email_utils import send_email

ADMIN_EMAIL = "vivi-oliver-nh@hotmail.com"
MAX_TENTATIVAS = 5
TEMPO_BLOQUEIO_MINUTOS = 5

def is_usuario_bloqueado(username, users_db):
    user_data = users_db.get(username)
    if not user_data:
        return False, None

    tentativas = user_data.get("tentativas", 0)
    ultimo_erro = user_data.get("ultimo_erro")

    if tentativas < MAX_TENTATIVAS:
        return False, None

    if ultimo_erro:
        try:
            dt_erro = datetime.fromisoformat(ultimo_erro)
            if datetime.now() - dt_erro < timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS):
                tempo_restante = timedelta(minutes=TEMPO_BLOQUEIO_MINUTOS) - (datetime.now() - dt_erro)
                return True, int(tempo_restante.total_seconds() // 60) + 1
        except Exception:
            pass

    return False, None

def auth_page():
    # Rodapé superior centralizado
    st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #888; margin-bottom: 20px;">
            &copy; 2025 Viviane de Oliveira — Todos os direitos reservados. Este projeto é protegido pela licença CC BY-NC.
        </div>
    """, unsafe_allow_html=True)

    # CSS personalizado
    st.markdown("""
        <style>
            body {
                background-color: #fdf0ba;
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
                font-size: 2.5rem;
            }
            h2 {
                text-align: center;
                color: #555;
                font-size: 1.3rem;
                margin-top: -15px;
                margin-bottom: 25px;
            }
            .info-box {
                max-width: 800px;
                margin: 30px auto;
                padding: 20px;
                border-radius: 16px;
                background-color: #f9e68a;
                border: 1px solid #f2cd4d;
            }
            .info-box h4 {
                color: #444;
                margin-bottom: 10px;
                text-align: center;
            }
            .info-box p {
                font-size: 15px;
                line-height: 1.6;
                color: #333;
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
                background-color: #fffdf6;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🔐 Palavras Cifradas sua segurança inicial 🔐 </h1>", unsafe_allow_html=True)
    st.markdown("<h2>Proteção e Privacidade de Dados</h2>", unsafe_allow_html=True)

    st.markdown("""
        <div class="info-box">
            <h4>🔐 Segurança Profissional com AES-256 (Plano Premium)</h4>
            <p>
                <b>Usuários Premium</b> contam com <b>criptografia avançada AES-256</b>, o mesmo padrão usado por bancos e governos.<br><br>
                • 💡 Cada arquivo é criptografado com uma chave única derivada da sua <b>senha pessoal</b> (que nunca é armazenada).<br>
                • 🔐 Sem a senha correta, nem os mesmos administradores fornecem descriptografia.<br>
                • 🧠 Proteção contra ataques de força bruta com 480.000 iterações (PBKDF2-HMAC + SHA-256).<br>
                • 📁 Os arquivos podem ser abertos em qualquer lugar — apenas com uma senha.<br><br>
                <span style='color: crimson;'><b>Perdeu a senha? Perdeu o acesso — e isso é o que garante sua segurança.</b></span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👤 Conecte-se")

    if "login_erro" in st.session_state:
        st.warning(st.session_state.login_erro)
        del st.session_state.login_erro

    with st.form("login_form"):
        usuario = st.text_input("👤 Usuário", key="login_user_input")
        senha = st.text_input("🔑 Senha", type="password", key="login_pass_input")
        submit = st.form_submit_button("Entrar")

    if submit:
        with st.spinner("A verificar credenciais..."):
            u_clean, s_clean = usuario.lower().strip(), senha.strip()
            users_db = load_users()

            if u_clean in users_db:
                bloqueado, minutos = is_usuario_bloqueado(u_clean, users_db)
                if bloqueado:
                    st.session_state.login_erro = f"⛔ Usuário temporariamente bloqueado. Tente novamente em {minutos} minuto(s)."
                    st.rerun()

                if verify_senha_usuario(users_db[u_clean]["password"], s_clean):
                    st.session_state.logged_in_user = u_clean
                    st.session_state.user_role = users_db[u_clean]["role"]
                    st.session_state.current_page = "home"
                    users_db[u_clean]["tentativas"] = 0
                    users_db[u_clean]["ultimo_erro"] = None
                    save_users(users_db)

                    if u_clean == "admin":
                        send_email(
                            ADMIN_EMAIL,
                            "Notificação de Login de Administrador - Palavras Cifradas",
                            f"Usuário '{u_clean}' logou com sucesso em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
                        )

                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    users_db[u_clean]["tentativas"] = users_db[u_clean].get("tentativas", 0) + 1
                    users_db[u_clean]["ultimo_erro"] = datetime.now().isoformat()
                    save_users(users_db)

                    restante = MAX_TENTATIVAS - users_db[u_clean]["tentativas"]
                    st.session_state.login_erro = (
                        f"❌ Senha incorreta. Você ainda tem **{restante} tentativa(s)** antes do bloqueio."
                        if restante > 0 else
                        "⛔ Usuário temporariamente bloqueado por excesso de tentativas."
                    )

                    if u_clean == "admin" and users_db[u_clean]["tentativas"] >= 3:
                        send_email(
                            ADMIN_EMAIL,
                            "ALERTA DE SEGURANÇA - Tentativas de Login Falhas (ADMIN)",
                            f"Detectadas {users_db[u_clean]['tentativas']} tentativas de login falhas para o usuário administrador '{u_clean}' em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        )

                    st.rerun()
            else:
                st.session_state.login_erro = "❌ Usuário não encontrado."
                st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 Criar nova conta"):
            st.session_state.current_page = "register"
            st.rerun()
    with col2:
        if st.button("🔐 Esqueci minha senha"):
            st.session_state.current_page = "recovery_password"
            st.rerun()
