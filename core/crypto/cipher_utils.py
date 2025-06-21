import os
import base64
import hashlib
import re
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# ✅ Verificação de força da senha
def verificar_forca_senha(senha: str) -> bool:
    """
    Verifica se a senha atende aos critérios mínimos de segurança:
    - Pelo menos 8 caracteres
    - Contém letras (maiúsculas ou minúsculas)
    - Contém números
    - Contém pelo menos um símbolo especial
    """
    if len(senha) < 8:
        return False
    if not re.search(r"[a-zA-Z]", senha):
        return False
    if not re.search(r"\d", senha):
        return False
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", senha):
        return False
    return True

# ✅ Mensagem clara e com exemplo aceito
MENSAGEM_SENHA_FRACA = (
    "Erro: Sua senha é considerada fraca.\n\n"
    "Use pelo menos 8 caracteres, com letras, números e símbolos especiais.\n"
    "💡 Exemplo seguro: amor@2025"
)

def gerar_chave_aes_segura(senha: str, salt: bytes) -> bytes:
    """
    Gera uma chave segura derivada da senha usando PBKDF2HMAC (SHA-256, 480.000 iterações).
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(senha.encode()))

def aes_encrypt_bytes(data_bytes: bytes, senha: str) -> bytes | str:
    """
    Criptografa bytes usando AES (via Fernet). Retorna salt + dados criptografados.
    """
    if not verificar_forca_senha(senha):
        return MENSAGEM_SENHA_FRACA

    try:
        salt = os.urandom(16)
        chave = gerar_chave_aes_segura(senha, salt)
        f = Fernet(chave)
        return salt + f.encrypt(data_bytes)
    except Exception as e:
        return f"Erro na criptografia AES (bytes): {e}"

def aes_decrypt_bytes(encrypted_data_bytes: bytes, senha: str) -> bytes | str:
    """
    Descriptografa dados criptografados com AES. Retorna os bytes originais ou erro.
    """
    try:
        salt, token = encrypted_data_bytes[:16], encrypted_data_bytes[16:]
        chave = gerar_chave_aes_segura(senha, salt)
        f = Fernet(chave)
        return f.decrypt(token)
    except InvalidToken:
        return b"ERRO: Senha incorreta ou ficheiro corrompido."
    except Exception as e:
        return f"Erro na descriptografia AES (bytes): {e}".encode()

def xor_encrypt(txt: str, senha: str) -> str:
    """
    Criptografa texto com XOR, incluindo hash da senha para validação. Retorna Base64.
    """
    if not verificar_forca_senha(senha):
        return MENSAGEM_SENHA_FRACA

    try:
        s_b = senha.encode()
        t_b = txt.encode()
        h = hashlib.md5(s_b).hexdigest()
        x = bytes([b ^ s_b[i % len(s_b)] for i, b in enumerate(t_b)])
        b64 = base64.b64encode(x).decode()
        return f"{h}::{b64}"
    except Exception as e:
        return f"Erro na criptografia XOR: {e}"

def xor_decrypt(txt_cifrado: str, senha: str) -> str:
    """
    Descriptografa dados cifrados com XOR, validando o hash da senha.
    """
    try:
        s_b = senha.encode()
        h, b64 = txt_cifrado.split("::", 1)
        if hashlib.md5(s_b).hexdigest() != h:
            raise ValueError("Senha incorreta.")

        b64 += "=" * ((4 - len(b64) % 4) % 4)
        d = base64.b64decode(b64.encode())
        x = bytes([b ^ s_b[i % len(s_b)] for i, b in enumerate(d)])
        return x.decode()
    except ValueError as ve:
        return f"Erro na descriptografia XOR: {ve}"
    except Exception as e:
        return f"Erro na descriptografia XOR: {e}"

def aes_encrypt_text(texto: str, senha: str) -> str:
    """
    Criptografa texto com AES. Retorna string Base64 contendo salt + dados criptografados.
    """
    if not verificar_forca_senha(senha):
        return MENSAGEM_SENHA_FRACA

    try:
        salt = os.urandom(16)
        chave = gerar_chave_aes_segura(senha, salt)
        f = Fernet(chave)
        token = f.encrypt(texto.encode())
        return base64.b64encode(salt + token).decode()
    except Exception as e:
        return f"Erro na criptografia AES (texto): {e}"

def aes_decrypt_text(texto_cifrado: str, senha: str) -> str:
    """
    Descriptografa texto cifrado em AES (Base64), extraindo salt e decodificando.
    """
    try:
        dados_decodificados = base64.b64decode(texto_cifrado.encode())
        salt, token = dados_decodificados[:16], dados_decodificados[16:]
        chave = gerar_chave_aes_segura(senha, salt)
        f = Fernet(chave)
        return f.decrypt(token).decode()
    except InvalidToken:
        return "Erro: Senha incorreta ou texto cifrado inválido."
    except Exception as e:
        return f"Erro: {e}"
