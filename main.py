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
        
        
@app.route('/fivelargest',methods=['POST'])
def fivelargest():
   con = sql.connect("Earthquake.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT date,time,latitude,depth,mag,place FROM Earthquake ORDER BY mag DESC LIMIT 5")
   rows1 = cur.fetchall()        
   return render_template("home.html",rows1 = rows1)
   
   
@app.route('/question2', methods=['POST'])
def question2():
        Latitude = request.form['Latitude']
        Longitude = request.form['Longitude']
        Distance = request.form['Distance']
        latdirection = request.form['latdirection']
        longdirection = request.form['longdirection']
             
        if latdirection == "west":
            Latitude = str(-1 * float(Latitude))
        
        if longdirection == "south":
            Longitude = str(-1 * float(Longitude))
            
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM Earthquake')
        rows = cur.fetchall()
        ct = 0
        finrows = []
        
        for row in rows:
            pair = []
            xcoord = float(row["latitude"])
            ycoord = float(row["longitude"])
            R = 6373.0

            lat1 = radians(float(Latitude))
            lon1 = radians(float(Longitude))
            lat2 = radians(xcoord)
            lon2 = radians(ycoord)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            if distance <= float(Distance):
                ct += 1
                finrows.append(row)

        return render_template('home.html', counts=ct, finalrow = finrows)
   
   
@app.route('/quakesbetweendaterange',methods=['POST'])
def quakesbetweendaterange():
   con = sql.connect("Earthquake.db")
   con.row_factory = sql.Row
   Start = request.form['StartDate']
   End = request.form['EndDate']
   cur = con.cursor()
   cur.execute("SELECT date,time,latitude,depth,mag,place FROM Earthquake WHERE mag > 3 and date between ? and ?", (Start,End))
   rows2 = cur.fetchall()        
   return render_template("home.html",rows2 = rows2)
   
   
@app.route('/incrementsearch', methods=['GET', 'POST'])
def incrementsearch():
    if request.method == 'POST':
        start = datetime.today() - timedelta(days=3)
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        magn=[]
        count=[]
        for i in np.arange(1,7,1):
            temp = i+1
            query = "SELECT count(*) as\"count\" FROM \"EarthQuake\" WHERE \"mag\" between \'"+str(i)+"\' and \'"+str(temp)+"\' and date between \'"+str(start)+"' and \'"+str(datetime.today())+"'"
            cur.execute(query)
            rows = cur.fetchone()
            rows3 = []
            rows3.append(i)
            rows3.append(temp)
            magn.append(rows3)
            count.append(str(rows["count"]))
    return render_template("home.html",data = magn,counts2 = count )
    
    
@app.route('/question5', methods=['POST'])
def question5():
        Latone = request.form['Latone']
        Longone = request.form['Longone']
        Lattwo = request.form['Lattwo']
        Longtwo = request.form['Longtwo']
        inputdist = request.form['distance']
        
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM EarthQuake')
        rows = cur.fetchall()
        ctone = 0
        cttwo = 0
        #For location 1
        for row in rows:
            pair = []
            xcoord = float(row["latitude"])
            ycoord = float(row["longitude"])
            rad = 6373.0

            lat1 = radians(float(Latone))
            lon1 = radians(float(Longone))
            lat2 = radians(float(Lattwo))
            lon2 = radians(float(Longtwo))
            
            lat = radians(xcoord)
            lon = radians(ycoord)

            dlon1 = lon - lon1
            dlat1 = lat - lat1
            
            dlon2 = lon - lon2
            dlat2 = lat - lat2

            a1 = sin(dlat1 / 2) ** 2 + cos(lat1) * cos(lat) * sin(dlon1 / 2) ** 2
            a2 = sin(dlat2 / 2) ** 2 + cos(lat2) * cos(lat) * sin(dlon2 / 2) ** 2
            
            c1 = 2 * atan2(sqrt(a1), sqrt(1 - a1))
            c2 = 2 * atan2(sqrt(a2), sqrt(1 - a2))

            distance1 = rad * c1
            distance2 = rad * c2
            if distance1 <= float(inputdist):
                ctone += 1
            if distance2 <= float(inputdist):
                cttwo += 1
                
            if(ctone>cttwo):
                str = "Earthquakes are more common at Location 1 than Location 2"
            elif ctone<cttwo:
                str = "Earthquakes are more common at Location 2 than Location 1"
            else:
                str = "Frequency of quake occurrence is same at both locations"
            

        return render_template('home.html', result=str)
        

@app.route('/question6', methods=['POST'])
def question6():
        Latitude = request.form['Latitude']
        Longitude = request.form['Longitude']
        Distance = request.form['Distance']
        
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM Earthquake')
        rows = cur.fetchall()
        ct = 0
        highestmag = []
        finrows = []
        mag = 0
        
        for row in rows:
            pair = []
            xcoord = float(row["latitude"])
            ycoord = float(row["longitude"])
            R = 6373.0

            lat1 = radians(float(Latitude))
            lon1 = radians(float(Longitude))
            lat2 = radians(xcoord)
            lon2 = radians(ycoord)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            if distance <= float(Distance):
                if row["mag"]>mag:
                    ct += 1
                    finrows = []
                    mag = row["mag"]
                    finrows.append(row)

        return render_template('home.html', counts=ct, finalrows = finrows, magnitude = mag)  


@app.route('/question8', methods=['POST'])
def question8():
        Latitude = request.form['Latitude']
        Longitude = request.form['Longitude']
        Distance = request.form['Distance']
        
        startdate = datetime.today() - timedelta(days=7)
        
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Earthquake WHERE date between \'"+str(startdate)+"' and \'"+str(datetime.today())+"'")
        rows = cur.fetchall()
        ct = 0
        highestmag = []
        finrows = []
        mag = 0
        
        for row in rows:
            pair = []
            xcoord = float(row["latitude"])
            ycoord = float(row["longitude"])
            R = 6373.0

            lat1 = radians(float(Latitude))
            lon1 = radians(float(Longitude))
            lat2 = radians(xcoord)
            lon2 = radians(ycoord)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            if distance <= float(Distance):
                if row["mag"]>mag:
                    ct += 1
                    finrows = []
                    mag = row["mag"]
                    finrows.append(row)

        return render_template('home.html', counts8=ct, finalrowsq8 = finrows, magnitude8 = mag)
        
@app.route('/question9', methods=['POST'])
def question9():
        Latitude = 32.729641
        Longitude = -97.110566
        
        con = sql.connect("Earthquake.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM Earthquake where mag > 6')
        rows = cur.fetchall()
        ct = 0
        closest = []
        finrows = []
        tempdistance = sys.maxsize
        
        for row in rows:
            pair = []
            xcoord = float(row["latitude"])
            ycoord = float(row["longitude"])
            R = 6373.0

            lat1 = radians(float(Latitude))
            lon1 = radians(float(Longitude))
            lat2 = radians(xcoord)
            lon2 = radians(ycoord)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            if distance <= float(tempdistance):
                finrows = []
                tempdist = distance
                finrows.append(row)

        return render_template('home.html', finalrowsq9 = finrows)

if __name__ == '__main__':
    #print(iport)
    #app.run(host='0.0.0.0', port=iport,debug = False)
    app.run()