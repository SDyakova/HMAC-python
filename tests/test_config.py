from src.config import get_secret_bytes, load_config
from src.constants import MIN_SECRET_LENGTH


def test_load_config():
    config = load_config()
    assert "secret" in config
    assert "max_msg_size_bytes" in config


def test_get_secret_bytes():
    config = load_config()
    secret = get_secret_bytes(config)
    assert isinstance(secret, bytes)
    assert len(secret) >= MIN_SECRET_LENGTH
