import streamlit as st
import uuid
import base64
from datetime import datetime, timedelta

# Simulando armazenamento temporário
# Em produção, use um banco de dados ou armazenamento mais seguro e escalável
LINKS_TEMPORARIOS = {}

# Função auxiliar para gerar ID único e expiração automática
def gerar_link_unico(conteudo, expiracao_minutos=15):
    id_unico = str(uuid.uuid4())
    validade = datetime.now() + timedelta(minutes=expiracao_minutos)
    conteudo_codificado = base64.urlsafe_b64encode(conteudo.encode()).decode()
    LINKS_TEMPORARIOS[id_unico] = {
        "conteudo": conteudo_codificado,
        "validade": validade,
        "usado": False
    }
    return id_unico

# Página de geração e acesso ao link

def link_generator_page():
    st.markdown("""
        <h1 style='text-align: center;'>🔗 Gerar Link Compartilhável</h1>
        <p style='text-align: center;'>Crie um link seguro para compartilhar textos criptografados com senha. O link expira após o primeiro uso ou após o tempo definido.</p>
    """, unsafe_allow_html=True)

    aba = st.radio("Escolha uma opção:", ["🔐 Criar Link", "🔓 Acessar Link"], horizontal=True)

    if aba == "🔐 Criar Link":
        with st.form(key="form_gerar_link"):
            conteudo = st.text_area("📝 Conteúdo criptografado (XOR ou AES):", height=150)
            senha = st.text_input("🔑 Senha necessária para desbloqueio:", type="password")
            tempo_expiracao = st.slider("⏱ Tempo de expiração do link (minutos)", 1, 60, 15)
            gerar = st.form_submit_button("🔗 Gerar Link Compartilhável")

        if gerar:
            if not conteudo or not senha:
                st.warning("⚠️ Preencha o conteúdo e a senha antes de gerar o link.")
            else:
                id_unico = gerar_link_unico(conteudo + senha, tempo_expiracao)
                link_gerado = f"?link_id={id_unico}"
                st.success("✅ Link gerado com sucesso!")
                st.write("🔒 Este link só poderá ser usado **uma vez** ou até expirar.")
                st.code(link_gerado, language="markdown")
                st.session_state.historico.append((
                    "Link Compartilhável", f"Gerado com expiração de {tempo_expiracao} min", datetime.now().strftime("%H:%M:%S")
                ))

    elif aba == "🔓 Acessar Link":
        link_id = st.text_input("🔗 Cole o ID do link gerado:").replace("?link_id=", "").strip()
        senha_acesso = st.text_input("🔑 Senha para desbloquear:", type="password")

        if st.button("🔍 Verificar e Acessar"):
            dados = LINKS_TEMPORARIOS.get(link_id)

            if not dados:
                st.error("❌ Link inválido ou não encontrado.")
            elif dados["usado"]:
                st.error("⚠️ Este link já foi utilizado e está expirado.")
            elif datetime.now() > dados["validade"]:
                st.error("⏰ Link expirado pelo tempo.")
            elif base64.urlsafe_b64decode(dados["conteudo"]).decode().endswith(senha_acesso):
                conteudo_real = base64.urlsafe_b64decode(dados["conteudo"]).decode().replace(senha_acesso, "")
                st.success("🔓 Acesso concedido! Conteúdo descriptografado:")
                st.code(conteudo_real)
                LINKS_TEMPORARIOS[link_id]["usado"] = True
            else:
                st.error("🔐 Senha incorreta.")

    st.markdown("""
        <hr>
        <p style='text-align: center; font-size: 0.85rem; color: gray;'>
        Recurso compatível com os textos gerados na aba de criptografia AES ou XOR.
        </p>
    """, unsafe_allow_html=True)

# OBS: Esse sistema é local e temporário. Para produção, considere persistência segura com banco de dados.
