"""Module with codec functions"""

import base64


def encode_base64url(data: bytes) -> str:
    """
    Кодирует байты в base64url без паддинга.

    :param data: Байты для кодирования.
    :return: Строка в base64url.
    """
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def decode_base64url(data: str) -> bytes:
    """
    Декодирует строку из base64url в байты.

    :param data: Строка в base64url.
    :return: Байты.
    :raises ValueError: Если строка невалидна.
    """
    try:
        padding = 4 - len(data) % 4
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data)
    except Exception:
        raise ValueError("invalid_signature_format")
