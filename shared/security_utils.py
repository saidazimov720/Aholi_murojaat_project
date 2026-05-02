from cryptography.fernet import Fernet, InvalidToken


class CryptoManager:
    """Encrypt and decrypt text with a shared Fernet key."""

    def __init__(self, secret_key: bytes | str):
        if isinstance(secret_key, str):
            secret_key = secret_key.encode("utf-8")
        self.fernet = Fernet(secret_key)

    def encrypt_data(self, text: str) -> str:
        if not isinstance(text, str):
            raise TypeError("encrypt_data expects a string")
        return self.fernet.encrypt(text.encode("utf-8")).decode("utf-8")

    def decrypt_data(self, token: str) -> str:
        if not isinstance(token, str):
            raise TypeError("decrypt_data expects a string token")
        try:
            return self.fernet.decrypt(token.encode("utf-8")).decode("utf-8")
        except InvalidToken as exc:
            raise ValueError("Encrypted message cannot be decrypted with this key") from exc
