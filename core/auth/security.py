import os
import base64
import re
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# 🔐 Hash simples SHA-256 usado no cadastro padrão
import hashlib
def hash_senha(senha: str) -> str:
    """
    Gera um hash SHA-256 da senha (versão simplificada, sem salt).
    Usado para usuários padrão no cadastro inicial.
    """
    return hashlib.sha256(senha.encode()).hexdigest()

def hash_senha_usuario(senha: str) -> str:
    """
    Gera um hash seguro da senha do usuário usando PBKDF2HMAC.
    Inclui um salt único para cada senha.
    Retorna o salt (em hex) e o hash da chave, separados por '::'.
    """
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return salt.hex() + "::" + chave.decode()

def verify_senha_usuario(senha_armazenada: str, senha_fornecida: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash da senha armazenada.
    """
    try:
        salt_hex, chave_armazenada = senha_armazenada.split("::")
        salt = bytes.fromhex(salt_hex)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            backend=default_backend()
        )
        chave_verificada = base64.urlsafe_b64encode(kdf.derive(senha_fornecida.encode()))
        return chave_verificada.decode() == chave_armazenada
    except (ValueError, Exception):
        return False

def is_password_strong(password: str) -> tuple[bool, str]:
    """
    Verifica a força de uma senha com base em critérios específicos.
    Retorna uma tupla (booleano, mensagem) indicando se a senha é forte e o motivo, se não for.
    """
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."
    if not re.search("[a-z]", password):
        return False, "A senha deve conter pelo menos uma letra minúscula."
    if not re.search("[A-Z]", password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."
    if not re.search("[0-9]", password):
        return False, "A senha deve conter pelo menos um número."
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "A senha deve conter pelo menos um símbolo especial."
    return True, ""

# --- Funções de Recuperação de Senha ---
def generate_recovery_token(username: str) -> str:
    """Gera um token de recuperação único para um usuário."""
    token_raw = f"{username}-{os.urandom(24).hex()}-{datetime.now().isoformat()}"
    return base64.urlsafe_b64encode(token_raw.encode()).decode()

def store_recovery_token(username: str, token: str, expiry_minutes: int = 15) -> None:
    """Armazena o token de recuperação e sua expiração no session_state (temporariamente)."""
    import streamlit as st
    st.session_state[f"recovery_token_{username}"] = {
        "token": token,
        "expiry": datetime.now() + timedelta(minutes=expiry_minutes)
    }

def verify_recovery_token(username: str, provided_token: str) -> bool:
    """Verifica se o token de recuperação fornecido é válido e não expirou."""
    import streamlit as st
    stored_token_info = st.session_state.get(f"recovery_token_{username}")

    if not stored_token_info:
        return False

    stored_token = stored_token_info.get("token")
    expiry_time = stored_token_info.get("expiry")

    if stored_token == provided_token and datetime.now() < expiry_time:
        del st.session_state[f"recovery_token_{username}"]
        return True
    return False
