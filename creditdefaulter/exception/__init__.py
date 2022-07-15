import os,sys

class Credit_Card_Default_Exception(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message = Credit_Card_Default_Exception.get_detailed_error_message(error_message=error_message,error_details=sys)
    
    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_details:sys) -> str:
        """
            error_message: Exception Object
            error_detail: Object of sys module 
        """
        _,_,exec_tb = error_details.exc_info()
        exception_block_line_no = exec_tb.tb_frame.f_lineno
        try_block_line_no = exec_tb.tb_lineno
        filename = exec_tb.tb_frame.f_code.co_filename

        error_message = f"""Error Occured in [{filename}] 
        at try block line no : [{try_block_line_no}] 
        and exception block line no : [{exception_block_line_no}] 
        and error_message is : [{error_message}]"""
        
        return error_message

    def __str__(self):
        return str(self.error_message)

    def __repr__(self) -> str:
        return Credit_Card_Default_Exception.__name__.str()

