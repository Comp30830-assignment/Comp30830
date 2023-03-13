

from flask import Flask, render_template, jsonify,g,abort
import functools
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine, text
import traceback
import glob
import os
from pprint import pprint
import json
import requests
import time
from IPython.display import display



#from jinjia2 import Template
#from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
# app=Flask(__name__)


app=Flask(__name__, static_url_path='')
#app.config.from_object('config')

url = "dbikes.cznzccwi0urk.us-east-1.rds.amazonaws.com"
user = "admin"
database= "dbikes"
port = "3306"
password = "Foryiuxing18!"

#engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)
#engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)

def connect_to_database():
    
    #return engine = create_engine("mysql://{user}:{password}@{url}:{port}/{database}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)
    #engine = create_engine("mysql://{user}:{password}@{url}:{port}/{database}".format(user, password, url, port, database), echo=True)
    #engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)
    engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)
    return engine
    
def get_db(): 
    db = getattr(g, '_database', None) 
    if db is None: 
        db = g._database = connect_to_database() 
    return db

@app.teardown_appcontext 
def close_connection(exception): 
    db = getattr(g, '_database', None) 
    if db is not None: 
        db.close() 
 


@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_db()
    sql = "select * from station ;"
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            print('#found {} stations', len(rows), rows)
            # use this formula to turn the rows into a list of dicts
            return jsonify([row._asdict() for row in rows])
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404

    
    

@app.route('/page')
def page():
    #return app.send_static_file('index.html')#only use in the static files
    #return "Hello!!!!cat!!!!"
    return render_template('test_part.html')

@app.route('/')
def index():
#     return "Hello!!!!cat!!!!"
      return '<h1>Hi!</h1>'

#這句話要放在最後才能運作整個程序
if __name__=="__main__":
    app.run(debug=True)
    


# @app.route('/')
# def contact():
#     return app.send_static_file('/sample/index.html')

# @app.route('/contact')
# def contact():
#     return app.send_static_file('/sample/index.html')

# @app.route('/stations')
# def stations():
#     return list of stations

# @app.route('/station/<int:station_id>')
# def station(station_id):
#     return 'Retrieving info for Station: {}'.format(station_id)