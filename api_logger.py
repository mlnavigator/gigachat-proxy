import json
import os
import logging
from logging.handlers import RotatingFileHandler
from threading import Lock

from config import log_level, error_log_file, requests_log_file, log_max_bytes, log_backup_count

# Класс для форматирования логов в JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }
        return json.dumps(log_record, ensure_ascii=False)

# Настройка логгера
def setup_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))  # Устанавливаем уровень из переменной окружения

    # Обработчик для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        log_file, maxBytes=log_max_bytes, backupCount=log_backup_count
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    # Обработчик для вывода логов в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    return logger


error_logger_lock = Lock()
requests_logger_lock = Lock()
error_logger = setup_logger('Error_logger', error_log_file)
requests_logger = setup_logger('Requests_logger', requests_log_file)
requests_logger.propagate = False
