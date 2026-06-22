"""Tests for config module"""

from src.config import get_secret_bytes, load_config


def test_load_config():
    """Загрузка конфига без ошибок."""
    config = load_config()
    assert "secret" in config
    assert "max_msg_size_bytes" in config


def test_get_secret_bytes():
    """Декодирование секрета в байты."""
    config = load_config()
    secret = get_secret_bytes(config)
    assert isinstance(secret, bytes)
    assert len(secret) >= 16
