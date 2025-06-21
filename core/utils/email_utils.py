import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from datetime import datetime

# --- Configurações de E-mail ---
SENDER_EMAIL = "vivi_oliver2015@yahoo.com.br"
SENDER_PASSWORD = "jbin nwly gjvz rkpx" # <<< SUBSTITUÍDO PELA SENHA DE APLICATIVO DO YAHOO
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465 # <<< MUDADO PARA 465 (SSL)

def send_email(receiver_email: str, subject: str, body: str):
    if SENDER_EMAIL == "seu_email@example.com" or SENDER_PASSWORD == "sua_senha_de_email" or \
       SENDER_EMAIL == "" or SENDER_PASSWORD == "":
        st.warning("Configurações de e-mail não definidas (email_utils.py). Notificação por e-mail desativada.")
        return False

    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        # Tenta SSL primeiro (se porta 465) ou TLS (se porta 587)
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server: # Usar SMTP_SSL para porta 465
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        else: # Assumindo porta 587 para TLS
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Inicia a segurança TLS
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        st.toast(f"E-mail enviado para {receiver_email}!", icon="📧")
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("Erro de autenticação SMTP. Verifique seu e-mail e senha (senha de app?) no email_utils.py.")
        st.error("Para Yahoo, pode ser necessário gerar uma 'senha de app' nas configurações de segurança da sua conta.")
        return False
    except smtplib.SMTPConnectError as e:
        st.error(f"Erro de conexão SMTP. Verifique o servidor e a porta no email_utils.py: {e}")
        return False
    except Exception as e:
        st.error(f"Erro inesperado ao enviar e-mail para {receiver_email}: {e}")
        return False
