import streamlit as st
import base64
from datetime import datetime
from core.crypto.cipher_utils import aes_encrypt_bytes
from core.auth.security import is_password_strong
from app.logic.media_processor import converter_audio
from app.logic.session_manager import get_active_role

def audio_encrypt_page():
    st.markdown("<h1 style='text-align: center;'>🔒 Criptografar Áudio</h1>", unsafe_allow_html=True)

    if get_active_role() not in ["premium", "admin"]:
        st.warning("Esta funcionalidade é exclusiva para usuários Premium.")
        if st.button("Fazer Upgrade"):
            st.session_state.current_page = "premium_plan"
            st.rerun()
        return

    uploaded_audio = st.file_uploader("Envie um áudio (MP3, WAV, OGG, FLAC)", type=["mp3", "wav", "ogg", "flac"], key="upload_audio_encrypt")

    if uploaded_audio and st.session_state.get("last_audio_encrypt") != uploaded_audio.name:
        st.session_state.last_audio_encrypt = uploaded_audio.name
        for key in ["playable_audio_bytes", "encrypted_result_b64", "encrypted_file_result"]:
            st.session_state.pop(key, None)
        st.rerun()

    if uploaded_audio and "playable_audio_bytes" not in st.session_state:
        with st.spinner("Convertendo áudio..."):
            resultado, erro = converter_audio(uploaded_audio.getvalue())
            if erro:
                st.error(erro)
            else:
                st.session_state.playable_audio_bytes = resultado

    if "playable_audio_bytes" in st.session_state:
        st.audio(st.session_state.playable_audio_bytes)

        senha = st.text_input("Senha para criptografia:", type="password", key="senha_audio_encrypt", placeholder="Ex: amor@2025")
        st.markdown("🔐 A senha deve ter no mínimo **8 caracteres**, com letras maiúsculas, minúsculas, números e símbolos.")

        with st.expander("🧠 Por que isso importa?"):
            st.markdown("""
            Senhas simples são fáceis de adivinhar por programas automáticos.<br>
            Ao combinar **palavras, números e símbolos**, você dificulta tentativas por força bruta,<br>
            aumentando a segurança real da sua criptografia.
            """, unsafe_allow_html=True)

        if st.button("🔐 Criptografar"):
            if senha:
                is_strong, msg = is_password_strong(senha)
                if not is_strong:
                    st.error(f"⚠️ Senha fraca: {msg}")
                else:
                    with st.spinner("Criptografando..."):
                        encrypted_data = aes_encrypt_bytes(st.session_state.playable_audio_bytes, senha)
                        if isinstance(encrypted_data, bytes):
                            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                            nome_base = st.session_state.last_audio_encrypt.rsplit(".", 1)[0]
                            nome_arquivo = f"{nome_base}_{timestamp}.enc"

                            st.session_state.encrypted_file_result = {
                                "data": encrypted_data,
                                "name": nome_arquivo
                            }
                            st.success("Áudio criptografado com sucesso!")
                            st.session_state.historico.append((
                                "AES Áudio",
                                f"Criptografado {st.session_state.last_audio_encrypt}",
                                datetime.now().strftime("%H:%M:%S")
                            ))
                        else:
                            st.error("Erro ao criptografar.")
            else:
                st.warning("Digite uma senha para criptografar.")

    if "encrypted_file_result" in st.session_state:
        st.download_button(
            "⬇️ Baixar Arquivo .enc",
            data=st.session_state.encrypted_file_result["data"],
            file_name=st.session_state.encrypted_file_result["name"],
            mime="application/octet-stream"
        )

        if st.button("🗑️ Limpar"):
            for key in ["playable_audio_bytes", "encrypted_file_result", "last_audio_encrypt"]:
                st.session_state.pop(key, None)
            st.rerun()
