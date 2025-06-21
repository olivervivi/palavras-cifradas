import json
import os
# Importar a função de hash de senha para criar usuários padrão
from core.auth.security import hash_senha_usuario

DB_FILE = "users.json"

def save_users(users_data: dict):
    """Salva os dados dos usuários no arquivo JSON."""
    with open(DB_FILE, "w") as f:
        json.dump(users_data, f, indent=4)

def load_users() -> dict:
    """
    Carrega os dados dos usuários do arquivo JSON.
    Se o arquivo não existir ou estiver vazio, cria usuários padrão.
    """
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        # Se o arquivo não existir ou estiver vazio, inicializa com usuários padrão
        default_users = {
            'admin': {"password": hash_senha_usuario("xxUrubu@Up"), "role": "admin"},
            'padrao': {"password": hash_senha_usuario("xxUrubu"), "role": "standard"},
            'premium': {"password": hash_senha_usuario("xxUrubu"), "role": "premium"}
        }
        save_users(default_users)
        return default_users
    
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Se o arquivo existir, mas estiver corrompido, retorna um dicionário vazio
        # e o problema pode ser tratado externamente ou o arquivo pode ser recriado
        print(f"Aviso: O arquivo '{DB_FILE}' está corrompido ou vazio. Recriando usuários padrão.")
        default_users = {
            'admin': {"password": hash_senha_usuario("xxUrubu@Up"), "role": "admin"},
            'padrao': {"password": hash_senha_usuario("xxUrubu"), "role": "standard"},
            'premium': {"password": hash_senha_usuario("xxUrubu"), "role": "premium"}
        }
        save_users(default_users)
        return default_users
    except FileNotFoundError:
        # Esta exceção já é tratada pela verificação os.path.exists
        return {}
