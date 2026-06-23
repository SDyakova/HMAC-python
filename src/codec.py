import base64

from src.constants import BASE64_PADDING


def encode_base64url(data: bytes) -> str:
    """Кодирует байты в base64url без паддинга."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def decode_base64url(data: str) -> bytes:
    """Декодирует строку из base64url в байты.

    Raises:
        ValueError: если строка невалидна.
    """
    padding = BASE64_PADDING - len(data) % BASE64_PADDING
    if padding != BASE64_PADDING:
        data += "=" * padding
    try:
        return base64.urlsafe_b64decode(data)
    except Exception:
        raise ValueError("invalid_signature_format")
