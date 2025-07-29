import sys
import logging

GLOBAL_LOGGING_LEVEL = logging.DEBUG

# import variable logger in python file for logging functionality 
logger = logging.getLogger(__name__)
logger.setLevel(GLOBAL_LOGGING_LEVEL) 

__console_handler = logging.StreamHandler(sys.stdout)
__console_handler.setLevel(GLOBAL_LOGGING_LEVEL)

__formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
__console_handler.setFormatter(__formatter)

logger.addHandler(__console_handler)
