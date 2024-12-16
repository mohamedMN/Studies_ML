import sys 
import logging
def error_message_detail(erreur, erreur_detail:sys):
    _,_,exc_tb=erreur_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Eurror occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(erreur)

    )
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,erreur_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, erreur_detail)

    def __str__(self):
        return self.error_message
    

if __name__=="__main__":
    try:
        s=5/0
    except Exception as e:
        logging.info("dived by zero")
        raise CustomException(e,sys)