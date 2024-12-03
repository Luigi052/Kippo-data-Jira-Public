import logging
import os
import config
from datetime import datetime


def setup_logging():
    if config.ENABLE_LOGGING:
        os.makedirs(config.LOG_PATH, exist_ok=True)
        log_file = os.path.join(config.LOG_PATH, f'log_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')

        handlers = [logging.FileHandler(log_file)]

        if config.CONSOLE_LOG:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=handlers)


def log_info(message: str):
    if config.ENABLE_LOGGING:
        logging.info(message)


def log_error(message: str):
    if config.ENABLE_LOGGING:
        logging.error(message)
