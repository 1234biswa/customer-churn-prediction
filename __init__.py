"""
Utilities module providing logging and exception handling features.
"""
from src.utils.logger import logger
from src.utils.exception import CustomException
from src.utils.styles import apply_custom_css

__all__ = ["logger", "CustomException", "apply_custom_css"]
