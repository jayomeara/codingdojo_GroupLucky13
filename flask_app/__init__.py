from flask import Flask
import logging 
logging.basicConfig(filename='errorLog.log', level=logging.ERROR)
app = Flask(__name__)
app.secret_key = "shhhhhh"