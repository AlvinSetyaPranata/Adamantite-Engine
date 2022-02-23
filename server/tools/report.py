# modules for displaying server activities and write to a log file 


from colorama import init
from termcolor import colored
import logging
import datetime
import os

init()

class Log:
    def __init__(self, log_level=logging.DEBUG, name="SYSTEM"):
        self.path_ = ""
        
        self.init_check()
        
        self.log_level = log_level
        self.log_ = logging.getLogger(name)
        self.log_.setLevel(self.log_level)
        self.log_.addHandler(self.get_file_handler())
   


    @property
    def debug(self):
        return colored("DEBUG", "white"), self.log_.debug

    @property
    def info(self):
        return colored("INFO", "green"), self.log_.info

    @property
    def warning(self):
        return colored("WARNING", "yellow"),self.log_.warning

    @property
    def error(self):
        return colored("ERROR", "red"), self.log_.error

    @property
    def critical(self):
        return colored("CRITICAL", "grey"), self.log_.critical


    def get_file_handler(self, fname=os.path.join("logs", datetime.datetime.now().strftime('%d-%m-%Y-%H:%M.log'))):
        f_handler = logging.FileHandler(fname, mode="w+")
        f_format = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s => %(message)s")
        f_handler.setFormatter(f_format)
        f_handler.setLevel(self.log_level)

        return f_handler


    def init_check(self):
        # check logs directory if doesnt exists then it will create automatically
        # else it will use existing one

        if not os.path.isdir("logs"):
            os.mkdir("logs")


    def report(self, message, exception_type, display_mode=print, *display_mode_args, **display_mode_kwargs):
        """
        Available execption type:

        1. debug => no mark
        2. info => green mark
        3. warning => yellow mark
        4. error => red mark
        5. critical => lightred mark
        """


        exception_type[1](message)
        message = datetime.datetime.now().strftime("[%a, %b-%Y %H:%M]") + f"[{exception_type[0]}]> " + message
        display_mode(message, *display_mode_args, **display_mode_kwargs)
        


def __test():
    d = Log()
    d.report("Hello Worlds", d.info)


if __name__ == "__main__":
    __test()