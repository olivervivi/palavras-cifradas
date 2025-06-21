import streamlit as st
import pandas as pd
from datetime import datetime # Certifique-se de importar datetime para usar no histórico

from app.logic.session_manager import get_active_role

def auditoria_usuario_page():
    """
    Página de auditoria de atividades do usuário.
    Exibe um histórico das operações de criptografia realizadas.
    Recurso Premium/Admin.
    """
    st.title("📊 Minhas Atividades")

    # Verifica se o usuário tem permissão
    if get_active_role() not in ["premium", "admin"]:
        st.warning("Esta funcionalidade está disponível apenas para utilizadores Premium e Administradores.")
        if st.button("✨ Fazer Upgrade para Premium Agora"):
            st.session_state.current_page = "premium_plan"
            st.rerun()
        return # Interrompe a execução da página para não-premium

    st.markdown("Aqui pode rever todas as operações de criptografia que realizou.")

    if not st.session_state.historico:
        st.info("Ainda não existem registos de atividade.")
    else:
        # Prepara os dados do histórico para exibição em um DataFrame
        history_data = []
        # Exibe o histórico em ordem reversa (mais recente primeiro)
        for op_type, op_detail, timestamp in reversed(st.session_state.historico):
            history_data.append({"Hora": timestamp, "Operação": op_type, "Detalhe": f"{op_detail[:40]}..."})
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True) # Exibe o DataFrame
