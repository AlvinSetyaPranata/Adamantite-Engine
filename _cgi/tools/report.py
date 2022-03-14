# modules for displaying server activities and write to a log file 


from colorama import init
from termcolor import colored
import logging
import datetime
import os

init()


class Log:
    def __init__(self, log_level=logging.DEBUG, name="SYSTEM", write_log=True):
        self.path_ = ""
        self.write_log = write_log
        

        if self.write_log:
            self.init_check()
            
            self.log_level = log_level
            self.log_ = logging.getLogger(name)
            self.log_.setLevel(self.log_level)
            self.log_.addHandler(self.get_file_handler())
   

    @property
    def debug(self):
        if not self.write_log:
            return colored("DEBUG", "white"), None

        return colored("DEBUG", "white"), self.log_.debug

    @property
    def info(self):
        if not self.write_log:
            return colored("INFO", "green"), None

        return colored("INFO", "green"), self.log_.info

    @property
    def warning(self):
        if not self.write_log:
            return colored("WARNING", "yellow"), None

        return colored("WARNING", "yellow"),self.log_.warning

    @property
    def error(self):
        if not self.write_log:
            return colored("ERROR", "red"), None

        return colored("ERROR", "red"), self.log_.error

    @property
    def critical(self):
        if not self.write_log:
            return colored("CRITICAL", "grey"), None

        return colored("CRITICAL", "grey"), self.log_.critical


    def mark(self, string, color):
        return colored(string, color)


    def get_file_handler(self, fname=os.path.join("logs", datetime.datetime.now().strftime('%d-%m-%Y-%H:%M.log'))):
        f_handler = logging.FileHandler(fname, mode="w+")
        f_format = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s => %(message)s")
        f_handler.setFormatter(f_format)
        f_handler.setLevel(self.log_level)

        return f_handler


    def init_check(self):
        
        if not os.path.isdir("logs"):
            os.mkdir("logs")


    def write(self, message, exception_type):
        """
        Available execption type:

        1. debug => no mark
        2. info => green mark
        3. warning => yellow mark
        4. error => red mark
        5. critical => lightred mark
        """

        abreviation, log_function = exception_type

        if self.write_log:
            log_function(message)


        return datetime.datetime.now().strftime("[%a, %b-%Y %H:%M]") + f"[{abreviation}]> " + message
        


class Reporter(Log):
    def __init__(self, display_function=print, **kwargs):
        super().__init__(**kwargs)
        self.display_function = display_function


    def report(self, message, level, *display_function_args, **display_function_kwargs):
        exc_type = None

        if level == 1:
            exc_type = self.debug

        elif level == 2:
            exc_type = self.info

        elif level == 3:
            exc_type = self.warning

        elif level == 4:
            exc_type = self.error

        elif level == 5:
            exc_type = self.critical

        else:
            raise Exception("Invalid level, must be in range between 1-5")


        self.display_function(self.write(message, exc_type), *display_function_args, **display_function_kwargs)


def __test():
    d = Reporter(write_log=False)
    d.report(d.mark("Hello Worlds", "red"), 2)


if __name__ == "__main__":
    __test()