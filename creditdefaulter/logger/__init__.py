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



def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]


