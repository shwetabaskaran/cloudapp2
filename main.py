#References
#http://mathforum.org/library/drmath/view/51879.html


from flask import Flask, render_template, request, send_file, flash
import pathlib
import pandas as pd
import sqlite3 as sql
import base64
import os
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import sys

app = Flask(__name__)
app.secret_key = "secret"
conn = sqlite3.connect('Earthquake.db')
import csv
import base64

csvf = pd.read_csv("earthquakes.csv")
csvf[['date', 'time']] = csvf['time'].str.split('T', expand=True)
csvf['time'] = csvf['time'].str.split('.').str[0]
csvf.to_sql('EarthQuake', conn, if_exists='replace', index=False)
print(csvf)


#iport = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
        return render_template('home.html')
        

if __name__ == '__main__':
    #print(iport)
    #app.run(host='0.0.0.0', port=iport,debug = False)
    app.run()