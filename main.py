from flask import Flask, render_template, request
app = Flask(__name__)
import os
 

#iport = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
    return render_template('home.html')

 


if __name__ == '__main__':
    #print(iport)
    #app.run(host='0.0.0.0', port=iport,debug = False)
    app.run()
