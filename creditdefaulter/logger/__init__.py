import logging
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = ""
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)
logging.basicConfig(filename = LOG_FILE_PATH,filemode= "w",format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

