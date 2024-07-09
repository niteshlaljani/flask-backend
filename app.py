from flask import Flask
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

@app.route("/")
def welcome():
    return "Hello" 

@app.route("/home")
def home():
    return "This is home" 



from controller import *