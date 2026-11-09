try:
    from src.forcastingproject.logging.logger import logger
except ModuleNotFoundError:
    try:
        from forcastingproject.logging.logger import logger
    except ModuleNotFoundError:
        from .logger import logger

__all__ = ["logger"]

