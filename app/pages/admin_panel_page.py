import streamlit as st
from core.storage.user_db import load_users, save_users
from core.auth.security import hash_senha_usuario, is_password_strong

def admin_panel_page():
    """
    Página do Painel de Administração para gerenciar usuários.
    Permite visualizar, redefinir senhas, excluir e alterar permissões.
    """
    st.title("👑 Painel de Administração")
    st.subheader("Gestão de Utilizadores")

    users_db = load_users()
    logged_user = st.session_state.get("logged_in_user", "admin")

    if not users_db:
        st.info("Nenhum utilizador para gerir.")
        return

    admin_count = sum(1 for u in users_db.values() if u["role"] == "admin")

    for username, data in users_db.items():
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

        col1.write(f"**Usuário:** `{username}`")
        col2.write(f"**Nível:** `{data['role']}`")

        can_modify = logged_user == "admin" and username != "admin"

        # Campo para nova senha personalizada
        with col3:
            nova_senha = st.text_input(
                f"Nova senha para {username}",
                type="password",
                key=f"senha_{username}",
                disabled=not can_modify
            )
            if nova_senha and st.button(f"Atualizar Senha", key=f"nova_senha_btn_{username}"):
                senha_ok, motivo = is_password_strong(nova_senha)
                if senha_ok:
                    users_db[username]["password"] = hash_senha_usuario(nova_senha)
                    save_users(users_db)
                    st.success(f"Senha de `{username}` atualizada com sucesso.")
                    st.rerun()
                else:
                    st.warning(f"Senha fraca: {motivo}")

        with col4:
            # Botão de reset rápido para senha padrão
            if st.button("🔁 Reset", key=f"reset_{username}", disabled=not can_modify):
                users_db[username]["password"] = hash_senha_usuario("password123")
                save_users(users_db)
                st.toast(f"Senha de '{username}' resetada para 'password123'.", icon="🔑")
                st.rerun()

            # Botão de exclusão com proteção
            if st.button("🗑️ Excluir", key=f"delete_{username}", type="primary", disabled=not can_modify):
                if data["role"] == "admin" and admin_count <= 1:
                    st.error("⚠️ Não é possível excluir o último administrador do sistema.")
                else:
                    del users_db[username]
                    save_users(users_db)
                    st.toast(f"Usuário '{username}' excluído com sucesso.", icon="🗑️")
                    st.rerun()
