"""Tests for HMAC service module"""

import pytest

from src.config import get_secret_bytes, load_config
from src.hmac_service import HMACSigner


@pytest.fixture
def signer():
    """Фикстура с инициализированным HMACSigner."""
    config = load_config()
    secret = get_secret_bytes(config)
    return HMACSigner(secret)


def test_sign_returns_bytes(signer):
    """Подпись возвращает байты."""
    sig = signer.sign("hello")
    assert isinstance(sig, bytes)
    assert len(sig) == 32


def test_verify_correct_signature(signer):
    """Верная подпись проходит проверку."""
    sig = signer.sign("hello")
    assert signer.verify("hello", sig) is True


def test_verify_wrong_message(signer):
    """Изменённое сообщение не проходит проверку."""
    sig = signer.sign("hello")
    assert signer.verify("world", sig) is False


def test_verify_wrong_signature(signer):
    """Изменённая подпись не проходит проверку."""
    signer.sign("hello")
    wrong_sig = b"\x00" * 32
    assert signer.verify("hello", wrong_sig) is False


def test_sign_deterministic(signer):
    """Одинаковые сообщения дают одинаковую подпись."""
    sig1 = signer.sign("hello")
    sig2 = signer.sign("hello")
    assert sig1 == sig2
