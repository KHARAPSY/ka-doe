import logging
import sys

def setup_logger(name: str = None) -> logging.Logger:
    """
    Sets up and returns a logger with a consistent format.
    Logs to both stdout and can be extended to file/remote sinks.
    """
    formatter = logging.Formatter(
        fmt='[%(asctime)s] | [%(name)s] | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
