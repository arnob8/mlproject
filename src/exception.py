import sys
import logging

#Step 1: Function to return error details
def error_message_detail(error,error_detail:sys):
    
     #error detail to be present in sys
     _,_,exc_tb = error_detail.exc_info()
     # In which filename I am getting error
     '''
     exc_info() is a function that returns information about the most recent exception raised.
    It returns a tuple with three elements:
    Exception type (e.g., ValueError)
    Exception value (e.g., the actual error message)
    Traceback object (the traceback, which contains detailed information about the error location)
     
     _, _, exc_tb

     the first two underscores (_) are used to ignore the first two values (the exception type and value), 
     as only the traceback is needed in this case.
     exc_tb will store the traceback object, which you can use to get detailed information about where the exception occurred in your code
     
     '''
     file_name = exc_tb.tb_frame.f_code.co_filename

     '''
     exc_tb.tb_frame.f_code.co_filename extracts the filename (as a string) where the exception was raised, 
     by navigating through the traceback object, the stack frame, and the code object

    exc_tb => is a traceback object -> that we get when an exception is caught, it contains information about where the error occured in the code
    tb_frame => attribute of the traceback obj -> pointing to the current stack frame where the exception occured
    A stack frame contains information about the function , the local vars, and current excution context for a 
    specific point in the programs execution
    f_code => attribute of the frame object holds the cold object that was executed in that frame
    A code object represents the compiled version of Python source code and it contains  various pieces of metadata about the code
    such as filename, function name and the code itself
    co_filename => attribute of the code object that contains the filename of the Python source file where the exception was raised
    basically contains the file path relative to where the script is being executed and it tells you exactly where the error occured in the code
     '''
     error_message = "Error occured in Python script name [{0}] line number [{1}] error message [{2}]".format(file_name,exc_tb.tb_lineno,str(error))
     return error_message
#Now whenever the error happens we are going to call the above function

#Step 2 - CustomException Class which inherits from Exception class and is used to call the Function created
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys): #my constructor, 
        super().__init__(error_message) # since we are inheriting the parent exception
        #whatever errorm message is cmoning from error_message_detail will initialize to the class variable or custom variable error_message
        self.error_message = error_message_detail(error_message,error_detail = error_detail)

#Step 3 - The __str__ method is overridden to return self.error_message. This means that when the exception is printed or converted to a string, 
#it will show the detailed error message created by error_message_detail.
    def __str__(self):
        return self.error_message

#Testing code for logger only
#if __name__ =="__main__":
   #logging.info("logging has started")

if __name__ == "__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by Zero")
        raise CustomException(e,sys)