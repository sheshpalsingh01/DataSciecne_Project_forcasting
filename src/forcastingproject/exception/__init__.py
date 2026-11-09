try:
    from src.forcastingproject.exception.exception import CustomException
except ModuleNotFoundError:
    try:
        from forcastingproject.exception.exception import CustomException
    except ModuleNotFoundError:
        from .exception import CustomException

__all__ = ["CustomException"]

