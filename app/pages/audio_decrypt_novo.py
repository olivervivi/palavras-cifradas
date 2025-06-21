import streamlit as st
import base64
from datetime import datetime

from core.crypto.cipher_utils import aes_decrypt_bytes
from app.logic.media_processor import converter_audio
from app.logic.session_manager import get_active_role

def audio_decrypt_novo():
    st.markdown("<h1 style='text-align: center;'>🔓 Descriptografar Áudio (Premium)</h1>", unsafe_allow_html=True)

    st.markdown("Faça upload de um arquivo `.enc` e informe a senha para descriptografar o conteúdo de áudio.")

    if get_active_role() not in ["premium", "admin"]:
        st.warning("Esta funcionalidade está disponível apenas para usuários Premium ou Admin.")
        return

    st.markdown("---")

    senha_decrypt = st.text_input("🔑 Digite a senha do áudio:", type="password", key="senha_audio_decrypt")

    decrypted_bytes = None

    # Upload do arquivo .enc
    encrypted_file = st.file_uploader("Selecione um arquivo .enc", type=['enc'], key="uploader_enc_file")

    if encrypted_file and senha_decrypt:
        with st.spinner("Descriptografando o arquivo..."):
            encrypted_bytes = encrypted_file.getvalue()
            decrypted_bytes = aes_decrypt_bytes(encrypted_bytes, senha_decrypt)

    # Se descriptografou com sucesso
    if decrypted_bytes and isinstance(decrypted_bytes, bytes) and b"ERRO:" not in decrypted_bytes:
        st.success("Áudio descriptografado com sucesso!")

        with st.spinner("Convertendo áudio para reprodução..."):
            resultado = converter_audio(decrypted_bytes)

        if resultado:
            audio_bytes, extensao = resultado
            st.audio(audio_bytes, format=f"audio/{extensao}")
            st.download_button("⬇️ Baixar Áudio", data=decrypted_bytes, file_name="audio_decifrado.wav")

        if st.button("🧹 Limpar Resultado", key="limpar_desc_result"):
            for key in ["uploader_enc_file", "senha_audio_decrypt"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif decrypted_bytes:
        st.error("❌ Senha incorreta ou dados inválidos. Não foi possível descriptografar.")
