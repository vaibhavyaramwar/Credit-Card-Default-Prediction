from flask import Flask,abort,request
from flask.helpers import send_file
from flask.templating import render_template
from creditdefaulter.config.configuration import Configuration
from creditdefaulter.entity.creditcard_predictor import CreditCardData, CreditCardPredictor
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
from creditdefaulter.constant import *
import os,sys
import json

from creditdefaulter.pipeline.pipeline import Pipeline
from creditdefaulter.logger import *
from creditdefaulter.util.util import read_yaml_file, write_yaml_file

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        
        logging.info("New request received")
        return render_template("index.html")
    except Exception as e:
        credit_Card_Default_Exception = Credit_Card_Default_Exception(e,sys)
        logging.info(credit_Card_Default_Exception.error_message)

@app.route("/artifact",defaults={'req_path','creditdeafulter'})
@app.route("/artifact/<path:req_path>")
def render_artifact_dir(req_path):
    try:
        os.makedirs("creditdeafulter",exist_ok=True)
        abs_path = os.path.join(req_path)

        if not os.path.exists(abs_path):
            abort(404)

        if os.path.isfile(abs_path):
            if '.html' in abs_path:
                with open(abs_path,"r",encoding="utf-8") as file:
                    content = ''
                    for line in file.readlines():
                       content = f'{content}{line}'
                       return content
            return send_file(abs_path)

        
        files={}
        for file_name in os.listdir(abs_path):
            if "artifact" in os.path.join(abs_path,file_name):
                files.update(os.path.join(abs_path,file_name),file_name)

        result = {
            "files":files,
            "parent_folder":os.path.dirname(abs_path),
            "parent_label":abs_path
        }

        return render_template('files.html',result=result)
        
    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

@app.route("/view_experiment_history",methods=["GET","POST"])
def view_experiment_history():
    
    experiment_status = Pipeline.get_experiment_status()
    context = {"experiment":experiment_status.to_html(classes="table table-striped col-12")}
    return render_template("experiment_history.html",context=context)
    
@app.route("/train",methods=["GET","POST"])
def train():
    message = ""

    pipeline= Pipeline(configuration=Configuration(current_time_stamp=get_current_time_stamp()))
    if not pipeline.experiment.running_status:
        message = "Pipeline Processing Started"
        pipeline.start()
    else:
        message = "Pipline Execution is already in progress , could not start the pipeline"
 
    experiment_status = Pipeline.get_experiment_status()
    
    context = {
        "experiment": experiment_status.to_html(classes="table table-striped col-12"),
        "message": message
    }

    render_template("train.html",context=context)


@app.route("/predict",methods=["GET","POST"])
def predict():

    context =  {
        HOUSING_DATA_KEY : None,
        MEDIAN_HOUSING_VALUE_KEY : None
    }

    if request.method == "POST":
        limit_bal = float(request.form["limit_bal"])
        sex = str(request.form["sex"])
        education = str(request.form["education"])
        marriage = str(request.form["marriage"])
        age = float(request.form["age"])
        pay_0 = str(request.form["pay_0"])
        pay_2 = str(request.form["pay_2"])
        pay_3 = str(request.form["pay_3"])
        pay_4 = str(request.form["pay_4"])
        pay_5 = str(request.form["pay_5"])
        pay_6 = str(request.form["pay_6"])
        bill_amt1 = float(request.form["bill_amt1"])
        bill_amt2 = float(request.form["bill_amt2"])
        bill_amt3 = float(request.form["bill_amt3"])
        bill_amt4 = float(request.form["bill_amt4"])
        bill_amt5 = float(request.form["bill_amt5"])
        bill_amt6 = float(request.form["bill_amt6"])
        pay_amt1 = float(request.form["pay_amt1"])
        pay_amt2 = float(request.form["pay_amt2"])
        pay_amt3 = float(request.form["pay_amt3"])
        pay_amt4 = float(request.form["pay_amt4"])
        pay_amt5 = float(request.form["pay_amt5"])
        pay_amt6 = float(request.form["pay_amt6"])

        creditCardData = CreditCardData(limit_bal = limit_bal,sex = sex,
                        education = education,marriage = marriage,age = age,
                        pay_0 = pay_0,pay_2 = pay_2,pay_3 = pay_3,
                        pay_4 = pay_4,pay_5 = pay_5,pay_6 = pay_6,
                        bill_amt1 = bill_amt1,bill_amt2 = bill_amt2,bill_amt3 = bill_amt3,
                        bill_amt4 = bill_amt4,bill_amt5 = bill_amt5,bill_amt6 = bill_amt6,
                        pay_amt1 = pay_amt1,pay_amt2 = pay_amt2,pay_amt3 = pay_amt3,
                        pay_amt4 = pay_amt4,pay_amt5 = pay_amt5,pay_amt6 = pay_amt6)

        credit_data_df = creditCardData.get_credit_card_Data_frame()

        creditCardPredictor = CreditCardPredictor(model_dir=MODEL_DIR)
        default_payment_next_month = creditCardPredictor.predict(X = credit_data_df)

        context = {HOUSING_DATA_KEY: creditCardData.get_credit_card_data_as_dict(),
                   MEDIAN_HOUSING_VALUE_KEY: default_payment_next_month,
                }

    return render_template('predict.html', context=context)
    

@app.route("/saved_modles",defaults={"req_path":"saved_modles"})
@app.route("/saved_modles/<path:req_path>")
def saved_models(req_path):
    abs_path = os.path.join(req_path)

    if not os.path.exists(abs_path):
        abort(404)

    if os.path.isfile(abs_path):
        send_file(abs_path)

    files = {os.path.join(abs_path,file):file for file in os.listdir(abs_path)}

    result = {
        "files":files,
        "parent_folder":os.path.dirname(abs_path),
        "parent_label":abs_path
    }

    return render_template("saved_models_files.html",result=result)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


@app.route("/update_model_config",methods=["GET","POST"])
def update_model_config():
    
    try:
        new_model_config = request.form("new_model_config")
        new_model_config = new_model_config.replace("'",'"')
        config = json.loads(new_model_config)
        write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH,data=config)
        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        render_template("update_model.html",result={"model_config":model_config})
    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

if __name__ == "__main__":
    app.run(debug=True)


