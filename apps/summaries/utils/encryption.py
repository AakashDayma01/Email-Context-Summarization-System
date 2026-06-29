import os
from cryptography.fernet import Fernet

KEY = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(KEY)


def encrypt(text: str) -> str:
    """
    Encrypt plain text using the configured Fernet encryption key.

    This function is used to securely encrypt email summary data
    before storing it in the PostgreSQL database.

    Args:
        text (str): Plain text to be encrypted.

    Returns:
        str: Encrypted text encoded as a string.
    """
    return cipher.encrypt(text.encode()).decode()


def decrypt(text: str) -> str:
    """
    Decrypt encrypted text using the configured Fernet encryption key.

    This function is used to retrieve the original email summary
    from the encrypted data stored in the PostgreSQL database.

    Args:
        text (str): Encrypted text.

    Returns:
        str: Decrypted plain text.
    """
    return cipher.decrypt(text.encode()).decode()