# utils.py
import secrets
import string

def generar_clave_especial(longitud=12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))
