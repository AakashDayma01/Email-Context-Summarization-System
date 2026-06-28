import os
from cryptography.fernet import Fernet

KEY = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(KEY)


def encrypt(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()


def decrypt(text: str) -> str:
    return cipher.decrypt(text.encode()).decode()