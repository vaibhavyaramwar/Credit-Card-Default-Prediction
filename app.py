from flask import Flask

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return "This a Machine Learning Project for Credit Card Default Prediction"

if __name__ == "__main__":
    app.run(debug=True)