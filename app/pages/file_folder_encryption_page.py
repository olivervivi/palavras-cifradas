import streamlit as st
import time
from datetime import datetime

from core.crypto.cipher_utils import aes_encrypt_bytes, aes_decrypt_bytes
from core.auth.security import is_password_strong
from app.logic.session_manager import get_active_role

def file_folder_encryption_page():
    st.markdown("<h1 style=\"text-align: center;\">📦 Criptografia de Arquivos e Pastas (Premium)</h1>", unsafe_allow_html=True)
    st.markdown("Proteja qualquer tipo de arquivo ou pastas inteiras (usando um arquivo .zip). O nome e a extensão do arquivo serão mantidos para sua conveniência.")
    st.info("💡 **Para criptografar uma pasta:** comprima-a em um arquivo `.zip` primeiro e depois faça o upload do `.zip`.")

    if get_active_role() not in ["premium", "admin"]:
        st.warning("Esta funcionalidade está disponível apenas para utilizadores Premium e Administradores.")
        if st.button("✨ Fazer Upgrade para Premium Agora", key="upgrade_file_folder_btn"):
            st.session_state.current_page = "premium_plan"
            st.rerun()
        return

    st.markdown("---")

    modo = st.radio("Selecione a Operação:", ["Criptografar", "Descriptografar"], horizontal=True, key="file_folder_mode")

    if modo == "Criptografar":
        st.markdown("<h3 style='text-align: center;'>🔒 Criptografar um Arquivo ou Pasta (.zip)</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Envie qualquer arquivo ou um .zip contendo sua pasta", key="ff_uploader_encrypt")
        senha = st.text_input("🔑 Crie uma senha para proteger este arquivo:", type="password", key="ff_pass_encrypt", placeholder="Ex: amor@2025")

        st.markdown("🔐 A senha deve ter no mínimo **8 caracteres**, com letras maiúsculas, minúsculas, números e símbolos.")

        with st.expander("🧠 Por que isso importa?"):
            st.markdown("""
            Senhas simples são fáceis de adivinhar por programas automáticos.<br>
            Ao combinar **palavras, números e símbolos**, você dificulta tentativas por força bruta,<br>
            aumentando a segurança real da sua criptografia.
            """, unsafe_allow_html=True)

        if st.button("🔒 Criptografar Arquivo/Pasta", key="encrypt_file_btn"):
            if uploaded_file and senha:
                is_strong, message = is_password_strong(senha)
                if not is_strong:
                    st.error(f"⚠️ Senha fraca: {message}")
                else:
                    with st.spinner(f"Criptografando '{uploaded_file.name}'..."):
                        original_bytes = uploaded_file.getvalue()
                        encrypted_data = aes_encrypt_bytes(original_bytes, senha)

                    if isinstance(encrypted_data, bytes):
                        st.success(f"'{uploaded_file.name}' criptografado com sucesso!")

                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        nome_saida = f"{uploaded_file.name}_{timestamp}.enc"
                        st.download_button(
                            label=f"⬇️ Baixar {nome_saida}",
                            data=encrypted_data,
                            file_name=nome_saida,
                            mime="application/octet-stream",
                            key="download_encrypted_file"
                        )

                        if 'contador_operacoes' not in st.session_state:
                            st.session_state.contador_operacoes = {"XOR": 0, "AES": 0, "File": 0}
                        st.session_state.contador_operacoes["File"] += 1

                        if 'historico' not in st.session_state:
                            st.session_state.historico = []
                        st.session_state.historico.append((
                            "AES Arquivo",
                            f"Criptografado {uploaded_file.name}",
                            datetime.now().strftime("%H:%M:%S")
                        ))
                    else:
                        st.error(f"❌ Erro na criptografia: {encrypted_data}")
            else:
                st.warning("Por favor, envie um arquivo e crie uma senha.")

    elif modo == "Descriptografar":
        st.markdown("<h3 style='text-align: center;'>🔓 Descriptografar um Arquivo ou Pasta</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Envie o arquivo criptografado (com nome original)", key="ff_uploader_decrypt")
        senha = st.text_input("🔑 Digite a senha do arquivo:", type="password", key="ff_pass_decrypt")

        if st.button("🔓 Descriptografar Arquivo/Pasta", key="decrypt_file_btn"):
            if uploaded_file and senha:
                with st.spinner(f"Descriptografando '{uploaded_file.name}'..."):
                    encrypted_bytes = uploaded_file.getvalue()
                    decrypted_data = aes_decrypt_bytes(encrypted_bytes, senha)

                if isinstance(decrypted_data, bytes) and b"ERRO:" not in decrypted_data:
                    st.success(f"'{uploaded_file.name}' descriptografado com sucesso!")

                    nome_saida = uploaded_file.name.replace(".enc", "")
                    st.download_button(
                        label=f"⬇️ Baixar {nome_saida}",
                        data=decrypted_data,
                        file_name=nome_saida,
                        mime="application/octet-stream",
                        key="download_decrypted_file"
                    )

                    if 'contador_operacoes' not in st.session_state:
                        st.session_state.contador_operacoes = {"XOR": 0, "AES": 0, "File": 0}
                    st.session_state.contador_operacoes["File"] += 1

                    if 'historico' not in st.session_state:
                        st.session_state.historico = []
                    st.session_state.historico.append((
                        "AES Arquivo",
                        f"Descriptografado {uploaded_file.name}",
                        datetime.now().strftime("%H:%M:%S")
                    ))
                else:
                    st.error("Senha incorreta ou arquivo corrompido.")
            else:
                st.warning("Por favor, envie um arquivo e digite sua senha.")
