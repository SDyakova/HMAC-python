"""Main module for run FastAPI application"""

import logging
import sys

import uvicorn

from src.app import app
from src.config import get_listen_address, get_log_level, load_config


def main():
    """Запуск приложения."""
    try:
        config = load_config()
        host, port = get_listen_address(config)
        log_level = get_log_level(config)

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

        logger = logging.getLogger(__name__)
        logger.info("Запуск сервера на %s:%s", host, port)

        uvicorn.run(app, host=host, port=port)
    except Exception as e:
        logging.critical("Критическая ошибка при запуске: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
