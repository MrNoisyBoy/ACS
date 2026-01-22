"""
Настройка логирования через loguru
Только для технической информации, не для пользователя!
"""

import sys
from loguru import logger
from pathlib import Path

def setup_logger(config: dict):
    """Настройка логирования"""

    # Удаляем все обработчики по умолчанию
    logger.remove()

    # Настройки из конфигурации
    log_level = config.get("log_level", "INFO")
    log_file = config.get("log_file", "system.log")

    # Формат для файла
    file_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Формат для консоли (только ошибки)
    console_format = (
        "<red>{time:HH:mm:ss}</red> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )

    # Добавляем обработчик для файла
    logger.add(
        log_file,
        level=log_level,
        format=file_format,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

    # Добавляем обработчик для консоли (только ERROR и выше)
    logger.add(
        sys.stderr,
        level="ERROR",
        format=console_format,
        colorize=True
    )

    return logger