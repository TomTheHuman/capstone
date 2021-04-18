import mysql.connector
from mysql.connector import Error
import sys
import os


import pandas as pd
import numpy as np

HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASS = os.environ.get('PASS')
DB = os.environ.get('DB')


def get_db():
    try:
        connection = mysql.connector.connect(host=HOST,database=DB,user=USER,password=PASS)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info, file=sys.stdout)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to database: ", record, file=sys.stdout)
        return connection

    except Error as e:
        print("Error while connecting to MySQL", e)

def get_data(req, con):
    if req == "all":
        return pd.read_sql('SELECT * FROM orders', con=con)
    elif req == "brand-totals":
        return pd.read_sql('SELECT brand, SUM(cases_sold) total_cases FROM orders GROUP BY brand', con=con)
    elif req == "month-totals":
        sql_data = pd.read_sql('SELECT brand, month(invoice_date) as invoice_date, sum(cases_sold) as cases_sold from orders group by brand, month(invoice_date) order by brand, month(invoice_date)', con=con)
        sql_data["invoice_date"] = pd.to_datetime('2000-' + sql_data["invoice_date"].astype(int).astype(str) + '-1', format = '%Y-%m')
        return sql_data
