"""Tests for codec module"""

import pytest

from src.codec import decode_base64url, encode_base64url


def test_encode_base64url():
    """Проверка кодирования в base64url."""
    data = b"test data"
    result = encode_base64url(data)
    assert isinstance(result, str)
    assert "=" not in result
    assert result == "dGVzdCBkYXRh"


def test_decode_base64url():
    """Проверка декодирования из base64url."""
    encoded = "dGVzdCBkYXRh"
    result = decode_base64url(encoded)
    assert result == b"test data"


def test_decode_invalid_base64url():
    """Проверка ошибки при невалидном base64url."""
    with pytest.raises(ValueError, match="invalid_signature_format"):
        decode_base64url("плохая строка")
