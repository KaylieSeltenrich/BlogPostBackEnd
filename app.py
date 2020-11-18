import mariadb
from flask import Flask, request, Response
import json 
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/blogpost', methods=['GET','POST','PATCH','DELETE'])
def blogpost():