# modules for displaying server activities and write to a log file 


import logging
import colorama
import datetime

logging.basicConfig(filename=datetime.datetime.strftime("%d-%m-%Y-%H:%M"), filemode='w')

