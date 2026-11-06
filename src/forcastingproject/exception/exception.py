import sys, os
from forcastingproject.logging.logger import logger


class CustomException(Exception):
    def __init__(self, error_msg, error_details: sys):
        super().__init__(error_msg)
        self.error_msg = str(error_msg)

        # Get the original exception trackback
        _,_,exc_tb = error_details.exc_info()

        if exc_tb is not None:
            self.line_no = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.function_name = exc_tb.tb_frame.f_code.co_filename

        else:
            self.line_no = None
            self.file_name = None
            self.function_name = None


    def __str__(self):
        return (
            f"Error Message: {self.error_msg}"
            f"File Name: {self.file_name}"
            f"Function Name: {self.function_name}"
            f"Line Number: {self.line_no}"
        )



    


    

    