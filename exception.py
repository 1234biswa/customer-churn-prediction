import sys
from typing import Any

def get_error_detail_message(error: Exception, error_detail: sys) -> str:
    """
    Extracts filename, line number, and error message from sys.exc_info() traceback.
    """
    _, _, exc_tb = error_detail.exc_info()
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] - error message: [{str(error)}]"
    else:
        error_message = str(error)
    return error_message


class CustomException(Exception):
    """
    Custom Exception class for standardized error reporting across the project.
    """
    def __init__(self, error_message: Exception, error_detail: Any):
        super().__init__(str(error_message))
        self.error_message = get_error_detail_message(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        return self.error_message
