import streamlit as st
from app.logic.session_manager import get_active_role

def apply_app_styling():
    """
    Aplica fundo contínuo (#fff8e1) para toda a aplicação Streamlit,
    incluindo partes vazias abaixo da área principal.
    """

    st.markdown("""
        <style>
        html, body {
            background-color: #fff8e1 !important;
            margin: 0 !important;
            padding: 0 !important;
            height: 100% !important;
        }

        .main, .block-container, [data-testid="stSidebar"] {
            background-color: #fff8e1 !important;
        }

        .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding: 2rem 4rem !important;
            border-radius: 10px;
            min-height: 100vh !important;  /* Garante preenchimento vertical total */
        }

        html::before, body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #fff8e1;
            z-index: -9999;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
            }
        }

        .stButton > button, .stDownloadButton > button {
            width: 100%;
            font-size: 1.1rem !important;
            padding: 0.8rem 1.6rem !important;
        }

        h1, h2, h3 {
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Proteção contra prints e seleção
    st.markdown("""
        <style>
        .main {
            user-select: none;
            -webkit-user-select: none;
            -ms-user-select: none;
        }

        @media print {
            body * {
                display: none !important;
                visibility: hidden !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
