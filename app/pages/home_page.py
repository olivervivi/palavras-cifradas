import streamlit as st
import pandas as pd
from datetime import datetime

from app.logic.session_manager import get_active_role

def home_page():
    st.title("🏠 Painel de Controle") 
    st.markdown(f"Bem-vindo de volta, **{st.session_state.logged_in_user}**!")
    st.info("Utilize o menu à esquerda para navegar pelas ferramentas de segurança.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Operações XOR", st.session_state.contador_operacoes.get('XOR', 0))
    col2.metric("Osperações AES", st.session_state.contador_operacoes.get('AES', 0))
    col3.metric("Ficheiros Processados", st.session_state.contador_operacoes.get('File', 0))

    st.subheader("Atividade Recente")
    if not st.session_state.historico:
        st.info("Nenhuma atividade recente para mostrar.")
    else:
        history_data = []
        for op_type, op_detail, timestamp in reversed(st.session_state.historico[-5:]):
            history_data.append({"Hora": timestamp, "Operação": op_type, "Detalhe": f"{op_detail[:50]}..."})
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
