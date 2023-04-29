import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Define log file path based on an environment variable
    log_file = os.environ.get('LOG_FILE_LOCATION', '/logs/talk-to-gpt.log')
    
    # Create a file handler and add it to the logger
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger