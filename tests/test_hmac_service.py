import pytest

from src.config import get_secret_bytes, load_config
from src.constants import HMAC_SIZE
from src.hmac_service import HMACSigner


@pytest.fixture
def signer():
    config = load_config()
    secret = get_secret_bytes(config)
    return HMACSigner(secret)


def test_sign_returns_bytes(signer):
    sig = signer.sign("hello")
    assert isinstance(sig, bytes)
    assert len(sig) == HMAC_SIZE


def test_verify_correct_signature(signer):
    sig = signer.sign("hello")
    assert signer.verify("hello", sig) is True


def test_verify_wrong_message(signer):
    sig = signer.sign("hello")
    assert signer.verify("world", sig) is False


def test_verify_wrong_signature(signer):
    signer.sign("hello")
    wrong_sig = b"\x00" * HMAC_SIZE
    assert signer.verify("hello", wrong_sig) is False


def test_sign_deterministic(signer):
    sig1 = signer.sign("hello")
    sig2 = signer.sign("hello")
    assert sig1 == sig2
