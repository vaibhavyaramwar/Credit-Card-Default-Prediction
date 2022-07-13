from flask import Flask
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
import sys

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        
        logging.info("New request received")
        return "This is a Machine Learning Project for Credit Card Default Prediction"
    except Exception as e:
        credit_Card_Default_Exception = Credit_Card_Default_Exception(e,sys)
        logging.info(credit_Card_Default_Exception.error_message)

if __name__ == "__main__":
    app.run(debug=True)


