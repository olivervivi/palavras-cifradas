import streamlit as st
import base64
from datetime import datetime

# Importações das suas funções de segurança e processamento
from core.crypto.cipher_utils import aes_decrypt_bytes
from app.logic.media_processor import converter_audio
from app.logic.session_manager import get_active_role

def audio_decrypt_novo():
    # ==============================================================================
    # 1. CABEÇALHO E TÍTULO
    # ==============================================================================
    # Aqui definimos o título que aparece no topo da página.
    # IMPORTANTE: O texto abaixo foi corrigido para "Descriptografar".
    st.markdown("<h1 style='text-align: center;'>🔓 Descriptografar Áudio (Premium)</h1>", unsafe_allow_html=True)

    st.markdown("Faça upload de um arquivo `.enc` e informe a senha para descriptografar o conteúdo de áudio.")

    # ==============================================================================
    # 2. VERIFICAÇÃO DE PERMISSÃO (SEGURANÇA)
    # ==============================================================================
    # Verifica se o usuário é "premium" ou "admin". Se não for, bloqueia o acesso.
    if get_active_role() not in ["premium", "admin"]:
        st.warning("⚠️ Esta funcionalidade está disponível apenas para usuários Premium ou Admin.")
        return  # O comando 'return' para o código aqui, não deixando carregar o resto.

    st.markdown("---") # Cria uma linha divisória visual

    # ==============================================================================
    # 3. ÁREA DE ENTRADA (INPUTS)
    # ==============================================================================
    # Campo para digitar a senha
    senha_decrypt = st.text_input("🔑 Digite a senha do áudio:", type="password", key="senha_audio_decrypt")

    # Variável para guardar o áudio depois de descriptografado
    decrypted_bytes = None

    # Botão para selecionar o arquivo no computador
    encrypted_file = st.file_uploader("Selecione um arquivo .enc", type=['enc'], key="uploader_enc_file")

    # ==============================================================================
    # 4. LÓGICA DE DESCRIPTOGRAFIA
    # ==============================================================================
    # Só tenta descriptografar se tiver arquivo E senha preenchidos
    if encrypted_file and senha_decrypt:
        with st.spinner("Descriptografando o arquivo..."):
            # Pega os dados brutos do arquivo
            encrypted_bytes = encrypted_file.getvalue()
            # Tenta descriptografar usando a senha
            decrypted_bytes = aes_decrypt_bytes(encrypted_bytes, senha_decrypt)

    # ==============================================================================
    # 5. EXIBIÇÃO DO RESULTADO
    # ==============================================================================
    # Verifica se deu certo (se não é vazio e se não retornou erro)
    if decrypted_bytes and isinstance(decrypted_bytes, bytes) and b"ERRO:" not in decrypted_bytes:
        st.success("✅ Áudio descriptografado com sucesso!")

        # Converte os dados brutos para um formato que o navegador toca (wav/mp3)
        with st.spinner("Convertendo áudio para reprodução..."):
            resultado = converter_audio(decrypted_bytes)

        # Se a conversão funcionou, mostra o player de áudio
        if resultado:
            audio_bytes, extensao = resultado
            # Player de áudio
            st.audio(audio_bytes, format=f"audio/{extensao}")
            
            # Botão de Download
            st.download_button(
                "⬇️ Baixar Áudio Recuperado", 
                data=decrypted_bytes, 
                file_name="audio_decifrado.wav"
            )

        # Botão para limpar a tela e começar de novo
        if st.button("🧹 Limpar Resultado", key="limpar_desc_result"):
            # Remove os arquivos da memória do Streamlit
            for key in ["uploader_enc_file", "senha_audio_decrypt"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun() # Recarrega a página

    # Caso a senha esteja errada
    elif decrypted_bytes:
        st.error("❌ Senha incorreta ou dados inválidos. Não foi possível descriptografar.")