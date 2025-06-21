import streamlit as st
import time
from datetime import datetime
from io import BytesIO

from core.crypto.cipher_utils import xor_encrypt, xor_decrypt, aes_encrypt_text, aes_decrypt_text
from app.logic.session_manager import get_active_role
from app.utils.ui_utils import limpar_tudo_xor, limpar_tudo_aes, gerar_qr_code_com_copia
from core.auth.security import is_password_strong

def text_encryption_page():
    st.title("✍️ Criptografia de Texto")
    st.markdown("Ferramentas para encriptar e desencriptar mensagens de texto de forma segura.")

    xor_tab, aes_tab = st.tabs(["🛡️ Criptografia XOR (Básica)", "🌟 Criptografia AES (Premium)"])

    with xor_tab:
        st.info("XOR é uma cifra rápida e simples. Pressione Enter no campo da senha para processar.")

        modo = st.radio("Selecione o Modo:", ["Cifrar", "Decifrar"], horizontal=True, key="modo_xor_form")

        with st.form(key="xor_form"):
            if modo == "Decifrar":
                uploaded_file = st.file_uploader("📁 Envie o arquivo .enc OU cole o texto cifrado:", type=["enc"], key="xor_file_upload")
                if uploaded_file:
                    texto_xor = uploaded_file.read().decode("utf-8")
                else:
                    texto_xor = st.text_area("📝 Cole o conteúdo cifrado:", key="texto_input_xor_form")
            else:
                texto_xor = st.text_area("📝 Digite a mensagem aqui:", key="texto_input_xor_form")

            senha_xor = st.text_input("🔑 Palavra-passe:", type="password", key="senha_input_xor_form")
            submitted_xor = st.form_submit_button("🚀 Processar com XOR")

        if submitted_xor:
            if not texto_xor or not senha_xor:
                st.warning("⚠️ Texto e senha são obrigatórios.")
            else:
                with st.spinner("A processar..."):
                    if modo == "Cifrar":
                        resultado = xor_encrypt(texto_xor, senha_xor)
                    else:
                        resultado = xor_decrypt(texto_xor, senha_xor)
                    st.session_state.resultado_xor = resultado

                if "Erro" not in resultado:
                    st.toast(f"Texto '{modo}' com sucesso!", icon="✅")
                    st.session_state.historico.append(("XOR", f"Texto {modo}", datetime.now().strftime("%H:%M:%S")))
                    st.session_state.contador_operacoes["XOR"] += 1
                else:
                    st.error(f"❌ {resultado}")

        st.markdown("---")
        st.button("🧹 Limpar Tudo (XOR)", on_click=limpar_tudo_xor, use_container_width=True, key="clear_xor_btn_form")

        if st.session_state.get("resultado_xor") and "Erro" not in st.session_state.resultado_xor:
            st.markdown("---")
            st.subheader("📤 Resultado XOR")
            st.code(st.session_state.resultado_xor)
            st.info("✨ A geração de QR Code para o resultado está disponível nos planos Premium.")

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            buffer = BytesIO(st.session_state.resultado_xor.encode())
            st.download_button("⬇️ Baixar Resultado Criptografado", data=buffer, file_name=f"mensagem_XOR_{timestamp}.enc")

    with aes_tab:
        if get_active_role() in ["premium", "admin"]:
            st.info("AES é o padrão industrial. Recomendado para dados sensíveis.")

            modo = st.radio("Selecione o Modo AES:", ["Cifrar", "Decifrar"], horizontal=True, key="modo_aes_form")

            with st.form(key="aes_form"):
                if modo == "Decifrar":
                    uploaded_file = st.file_uploader("📁 Envie o arquivo .enc OU cole o texto cifrado:", type=["enc"], key="aes_file_upload")
                    if uploaded_file:
                        texto_aes = uploaded_file.read().decode("utf-8")
                    else:
                        texto_aes = st.text_area("📝 Cole o conteúdo cifrado:", key="texto_input_aes_form")
                else:
                    texto_aes = st.text_area("📝 Digite a mensagem AES aqui:", key="texto_input_aes_form")

                senha_aes = st.text_input(
                    "🔑 Palavra-passe AES (mínimo 8 caracteres, Ex: amor@2025):",
                    type="password", key="senha_input_aes_form"
                )

                with st.expander("🧠 Por que isso importa?"):
                    st.markdown("""
                        Senhas simples são fáceis de adivinhar por programas automáticos.<br>
                        Ao combinar **letras, números e símbolos**, você dificulta tentativas por força bruta,
                        tornando sua criptografia realmente **segura**.
                    """, unsafe_allow_html=True)

                submitted_aes = st.form_submit_button("🚀 Processar com AES")

            if submitted_aes:
                if not texto_aes or not senha_aes:
                    st.warning("⚠️ Texto e senha são obrigatórios.")
                else:
                    is_strong, message = is_password_strong(senha_aes)
                    if not is_strong:
                        st.error(f"Senha fraca: {message}")
                    else:
                        with st.spinner("A processar..."):
                            if modo == "Cifrar":
                                resultado = aes_encrypt_text(texto_aes, senha_aes)
                            else:
                                if "::" in texto_aes:
                                    resultado = xor_decrypt(texto_aes, senha_aes)
                                else:
                                    resultado = aes_decrypt_text(texto_aes, senha_aes)
                            st.session_state.resultado_aes = resultado

                        if "Erro" not in resultado:
                            st.toast("Texto processado com sucesso!", icon="✅")
                            st.session_state.historico.append(("AES/XOR Premium", f"Texto {modo}", datetime.now().strftime("%H:%M:%S")))
                            st.session_state.contador_operacoes["AES"] += 1
                        else:
                            st.error(f"❌ {resultado}")

            st.markdown("---")
            st.button("🧹 Limpar Tudo (AES)", on_click=limpar_tudo_aes, use_container_width=True, key="clear_aes_btn_form")

            if st.session_state.get("resultado_aes") and "Erro" not in st.session_state.resultado_aes:
                st.markdown("---")
                st.subheader("📤 Resultado AES (Premium)")
                gerar_qr_code_com_copia(st.session_state.resultado_aes, key_prefix="aes")

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                buffer = BytesIO(st.session_state.resultado_aes.encode())
                st.download_button("⬇️ Baixar Resultado Criptografado", data=buffer, file_name=f"mensagem_AES_{timestamp}.enc")
        else:
            st.warning("Esta é uma funcionalidade exclusiva para membros Premium.")
            if st.button("✨ Fazer Upgrade para Premium Agora", key="upgrade_aes_button"):
                st.session_state.current_page = "premium_plan"
                st.rerun()
