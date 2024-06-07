import os
import sys
import logging
from loguru import logger
from app import settings


class InterceptHandler(logging.Handler):
    """
    This handler intercepts standard logging messages to redirect them to Loguru sinks.
    """

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logger.configure(
    handlers=[
        {"sink": sys.stderr, "level": logging.DEBUG},
    ]
)

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

logger.add(
    os.path.join(settings.LOGS_DIR, "{time:YYYY-MM-DD}.log"),
    rotation="5000 KB",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    level=logging.DEBUG,
)
