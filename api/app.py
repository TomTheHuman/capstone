from flask import Flask, render_template, request, session, jsonify, make_response
import json
import db
import lstm
import data
import sys
from flask_cors import CORS
# Database tools
import mysql.connector
from mysql.connector import Error
# Data tools
import pandas as pd
import numpy as np
# Matplot library for plotting
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
# Keras & SciKit Learn
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler
# Chart library
import chart_studio.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go

app = Flask(__name__)
CORS(app)
app.secret_key='8753^7Qn_Pds%!7'

# Main flask app call
@app.route("/", methods=['GET'])
def index():
    return "Nothing..."

@app.route('/query', methods = ['POST'])
def query():
    try:
        json_data = request.json
        connection = db.get_db()
        connection.connect()
        if connection.is_connected():
            print("Fetching data frame for " + json_data['brand'] + ', ' + json_data['size'], file=sys.stdout)
            query = str("SELECT * FROM orders WHERE brand = '" + json_data['brand'] + "' AND package_size = '" + json_data['size']) +"'"
            data_table = pd.read_sql(query, con=connection)
            predicted_data = lstm.predict(data_table)
            connection.close()

            # response_data = pd.DataFrame(predicted_data, columns = ['invoice_date', 'cases_sold', 'cases_pred'])
            response = predicted_data.to_json(orient="records", date_format="iso")
            parsed = json.loads(response)
            return {'predict': parsed }


    except Error as e:
        return "Error fetching table..."


@app.route("/data", methods=['GET'])
def get_data():
        return data.get_options()

@app.route("/brand-totals", methods=['GET'])
def get_master():
    try:
        connection = db.get_db()
        connection.connect()
        if connection.is_connected():
            print("Fetching brand totals data...", file=sys.stdout)
            data = db.get_data("brand-totals", con=connection).to_json(orient="records", date_format="iso")
            connection.close()
            return {'data': json.loads(data)}


    except Error as e:
        return "Error fetching table..."

@app.route("/month-totals", methods=['GET'])
def get_monthly():
    try:
        connection = db.get_db()
        connection.connect()
        if connection.is_connected():
            print("Fetching brand totals data...", file=sys.stdout)
            data = db.get_data("month-totals", con=connection).to_json(orient="records", date_format="iso")
            connection.close()
            return {'data': json.loads(data)}


    except Error as e:
        return "Error fetching table..."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
