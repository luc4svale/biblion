import secrets

def str_rand(length: int = 64) -> str:
    length = max(4, length)
    return secrets.token_hex(length // 2)
