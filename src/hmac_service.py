"""Module with HMAC sign functions"""

import hashlib
import hmac


class HMACSigner:
    """Class for HMAC sign and verify signature"""

    def __init__(self, secret: bytes):
        """
        Инициализация с секретным ключом.

        :param secret: Секретный ключ в байтах.
        """
        self._secret = secret

    def sign(self, msg: str) -> bytes:
        """
        Подписать сообщение алгоритмом HMAC-SHA256.

        :param msg: Сообщение для подписи.
        :return: Подпись в байтах.
        """
        msg_bytes = msg.encode("utf-8")
        return hmac.new(self._secret, msg_bytes, hashlib.sha256).digest()

    def verify(self, msg: str, signature: bytes) -> bool:
        """
        Проверить подпись сообщения.

        :param msg: Сообщение для проверки.
        :param signature: Подпись в байтах.
        :return: True если подпись верна, иначе False.
        """
        expected = self.sign(msg)
        return hmac.compare_digest(expected, signature)


def hmac_service() -> HMACSigner:
    """
    Фабрика для создания HMACSigner.

    :return: Инициализированный HMACSigner.
    """
    from src.config import get_secret_bytes, load_config

    config = load_config()
    secret = get_secret_bytes(config)
    return HMACSigner(secret)
