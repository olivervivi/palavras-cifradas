# COPIE E COLE ESTE CÓDIGO INTEIRO NO SEU ARQUIVO: app/utils/ui_utils.py

import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime

# Módulos para exportação de ficheiros
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit


def gerar_qr_code_com_copia(texto: str, key_prefix: str):
    """
    Gera um QR Code para o texto fornecido e exibe o texto.
    Fornece um botão para download do QR Code.
    """
    st.subheader("📷 QR Code e Texto")
    
    QR_CODE_MAX_LEN = 2500  # Limite de caracteres para um QR Code confiável

    if len(texto) > QR_CODE_MAX_LEN:
        st.warning(f"⚠️ O texto resultante é muito longo para ser exibido como QR Code (limite recomendado: {QR_CODE_MAX_LEN} caracteres).")
    else:
        # Cria o QR Code
        img = qrcode.make(texto)
        buffer = BytesIO()
        img.save(buffer, format="PNG")  # Salva a imagem no buffer
        st.image(buffer.getvalue())  # Exibe a imagem no Streamlit
        st.download_button(
            "⬇️ Baixar QR Code",
            buffer.getvalue(),
            "resultado_qrcode.png",
            "image/png",
            key=f"qr_download_{key_prefix}"
        )
    st.code(texto, language=None)  # Exibe o texto em um bloco de código


def criar_botoes_exportacao(texto: str, modo: str):
    """
    Cria botões para exportar o texto resultante em diferentes formatos:
    .txt, .docx, e .pdf.
    """
    st.subheader("⬇️ Opções de Exportação")
    c1, c2, c3 = st.columns(3)
    # Gera um nome base para os arquivos de exportação
    base_nome = f"{modo.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with c1:
        st.download_button("📥 .txt", texto, f"{base_nome}.txt", "text/plain", key=f"txt_{modo}")
    
    with c2:
        b_docx = BytesIO()
        d = Document()
        d.add_paragraph(texto)  # Adiciona o texto ao documento Word
        d.save(b_docx)  # Salva o documento no buffer
        st.download_button("📄 .docx", b_docx.getvalue(), f"{base_nome}.docx", key=f"docx_{modo}")

    with c3:
        b_pdf = BytesIO()
        c = canvas.Canvas(b_pdf, pagesize=letter)  # Cria um novo documento PDF
        c.setFont("Courier", 10)  # Define a fonte e tamanho
        y = 750  # Posição Y inicial
        # Divide o texto em linhas que cabem na largura da página
        for line in simpleSplit(texto, "Courier", 10, 500):
            c.drawString(72, y, line)
            y -= 12
            if y < 50:  # Se estiver perto do fim da página, cria uma nova
                c.showPage()
                c.setFont("Courier", 10)
                y = 750
        c.save()  # Salva o PDF
        st.download_button("🧾 .pdf", b_pdf.getvalue(), f"{base_nome}.pdf", key=f"pdf_{modo}")


# ==============================================================================
# FUNÇÕES DE LIMPEZA (CORRIGIDAS)
# ==============================================================================

def limpar_tudo_xor():
    """Limpa os campos de input e o resultado da aba XOR, usando as chaves do formulário."""
    # CORRIGIDO: Aponta para as chaves com o sufixo '_form'
    if "texto_input_xor_form" in st.session_state:
        st.session_state.texto_input_xor_form = ""
    if "senha_input_xor_form" in st.session_state:
        st.session_state.senha_input_xor_form = ""
    
    # Limpa o resultado
    if "resultado_xor" in st.session_state:
        st.session_state.resultado_xor = ""
    
    st.toast("Campos XOR limpos!", icon="🧹")


def limpar_tudo_aes():
    """Limpa os campos de input e o resultado da aba AES, usando as chaves do formulário."""
    # CORRIGIDO: Aponta para as chaves com o sufixo '_form'
    if "texto_input_aes_form" in st.session_state:
        st.session_state.texto_input_aes_form = ""
    if "senha_input_aes_form" in st.session_state:
        st.session_state.senha_input_aes_form = ""

    # Limpa o resultado
    if "resultado_aes" in st.session_state:
        st.session_state.resultado_aes = ""
        
    st.toast("Campos AES limpos!", icon="🧹")


def limpar_tudo_geral():
    """
    Limpa todos os campos, resultados e estados de arquivos/audio,
    além de redefinir o histórico e contadores de operações.
    """
    # Esta função agora chama as versões corrigidas de limpar_tudo_xor e limpar_tudo_aes
    limpar_tudo_xor()
    limpar_tudo_aes()
    
    # O resto da lógica permanece o mesmo
    if "decrypted_audio_data" in st.session_state:
        st.session_state.decrypted_audio_data = None
    if "uploaded_audio_bytes" in st.session_state:
        st.session_state.uploaded_audio_bytes = None
    if "historico" in st.session_state:
        st.session_state.historico = []
    if "contador_operacoes" in st.session_state:
        st.session_state.contador_operacoes = {"XOR": 0, "AES": 0, "File": 0}
        
    st.toast("Tudo limpo com sucesso!", icon="🧼")