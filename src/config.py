import json
import logging
from base64 import b64decode
from pathlib import Path

from src.constants import MIN_SECRET_LENGTH

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"


class ConfigError(Exception):
    """Ошибка конфигурации."""


def load_config():
    """Загружает и валидирует config.json.

    :return: Словарь с конфигурацией.
    :raises ConfigError: Если файл не найден или поля некорректны.
    """
    if not CONFIG_PATH.exists():
        raise ConfigError(f"Файл конфигурации не найден: {CONFIG_PATH}")

    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Некорректный JSON: {e}")

    required_fields = ["secret", "max_msg_size_bytes"]
    for field in required_fields:
        if field not in config:
            raise ConfigError(f"Отсутствует обязательное поле: {field}")

    if not isinstance(config["max_msg_size_bytes"], int):
        raise ConfigError("max_msg_size_bytes должен быть целым числом.")

    return config


def get_secret_bytes(config):
    """Извлекает секрет из конфига и декодирует из base64 в байты.

    :param config: Словарь конфигурации.
    :return: Секретный ключ в байтах.
    :raises ConfigError: Если секрет некорректный.
    """
    try:
        secret_bytes = b64decode(config["secret"])
    except Exception as e:
        raise ConfigError(f"Некорректный secret (base64): {e}")

    if len(secret_bytes) < MIN_SECRET_LENGTH:
        raise ConfigError(
            f"Секрет должен быть длиной минимум {MIN_SECRET_LENGTH} байт."
        )

    return secret_bytes


def get_listen_address(config):
    """Извлекает хост и порт из конфига.

    :param config: Словарь конфигурации.
    :return: Кортеж (host, port).
    """
    listen = config.get("listen", "0.0.0.0:8080")
    host, port = listen.split(":")
    return host, int(port)


def get_log_level(config):
    """Извлекает уровень логирования из конфига.

    :param config: Словарь конфигурации.
    :return: Уровень логирования (logging.INFO и т.д.).
    """
    level = config.get("log_level", "info").upper()
    return getattr(logging, level, logging.INFO)
