import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
