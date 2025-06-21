import streamlit as st

def manual_instrucoes_page():
    st.title("📚 Manual de Instruções — Palavras Cifradas")
    
    # Certifique-se de que o arquivo TXT existe na raiz do seu projeto
    try:
        # CORRIGIDO: Nome do arquivo TXT para corresponder ao que o usuário criou
        with open("Manual_Usuario_Palavras_Cifradas.txt", "r", encoding="utf-8") as file:
            st.markdown(file.read())
    except FileNotFoundError:
        st.error("Erro: O arquivo 'Manual_Usuario_Palavras_Cifradas.txt' não foi encontrado na pasta raiz do projeto.")
        st.info("Por favor, certifique-se de que este arquivo TXT com o seu manual esteja na pasta principal do projeto.")
    except Exception as e:
        st.error(f"Erro ao carregar o manual de instruções: {e}")

