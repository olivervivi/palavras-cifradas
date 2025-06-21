import streamlit as st

def documentacao_page():
    st.title("📘 Documentação Técnica — Palavras Cifradas")
    
    # Certifique-se de que o arquivo TXT existe na raiz do seu projeto
    try:
        with open("Documentacao_Tecnica_Palavras_Cifradas.txt", "r", encoding="utf-8") as file:
            st.markdown(file.read())
    except FileNotFoundError:
        st.error("Erro: O arquivo 'Documentacao_Tecnica_Palavras_Cifradas.txt' não foi encontrado na pasta raiz do projeto.")
        st.info("Por favor, crie este arquivo com o conteúdo da sua documentação.")
    except Exception as e:
        st.error(f"Erro ao carregar a documentação: {e}")
