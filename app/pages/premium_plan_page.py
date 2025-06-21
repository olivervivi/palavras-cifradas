import streamlit as st
import time
from datetime import datetime

from core.storage.user_db import load_users, save_users
from app.logic.session_manager import get_active_role, initialize_session_state

def premium_plan_page():
    """
    Página de upgrade para o plano Premium.
    Simula um processo de pagamento e atualiza a função do usuário.
    """
    st.title("✨ Upgrade para o Plano Premium")
    st.markdown("Desbloqueie o poder da criptografia de ficheiros e outros benefícios exclusivos!")
    
    st.subheader("Vantagens do Plano Premium:")
    st.markdown("""
        - **📦 Criptografia de Arquivos e Pastas**
        - **🎹 Criptografia de Áudio Profissional**
        - **✨ Decifragem Inteligente (AES/XOR)**
        - **📊 Auditoria de Atividades**
        - **🚀 Suporte Prioritário**
    """)
    st.info("Para garantir a segurança da sua conta, recomendamos que use uma senha forte.")
    
    st.markdown("---")
    st.subheader("Simulação de Pagamento")
    
    with st.form("payment_form"):
        st.text_input("Nome no Cartão", value="Utilizador Padrão", help="Este é um campo de simulação.", key="card_name")
        st.text_input("Número do Cartão (fictício)", value="4242 4242 4242 4242", help="Este é um campo de simulação.", key="card_number")
        
        col1, col2 = st.columns(2)
        col1.text_input("Validade (MM/AA)", "12/25", help="Este é um campo de simulação.", key="card_expiry")
        col2.text_input("CVV", "123", type="password", help="Este é um campo de simulação.", key="card_cvv")
        
        # ❌ CORRIGIDO: Removido o argumento key que causava erro
        if st.form_submit_button("Confirmar Upgrade por R$ 9,99/mês"):
            with st.spinner("A processar pagamento..."):
                time.sleep(1)
                
                users_db = load_users()
                current_user = st.session_state.logged_in_user
                
                if current_user in users_db:
                    users_db[current_user]["role"] = "premium"
                    save_users(users_db)
                
                time.sleep(1)
            
            st.session_state.user_role = "premium"
            st.session_state.current_page = "file_folder_encryption"
            st.success("Pagamento aprovado! Sua conta agora é Premium!")
            st.balloons()
            time.sleep(2)
            st.rerun()
