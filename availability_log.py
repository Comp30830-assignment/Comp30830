import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import json
import requests
import time
from IPython.display import display
import traceback
import datetime


url = "dbikes.cznzccwi0urk.us-east-1.rds.amazonaws.com"
user = "admin"
database= "dbikes"
port = "3306"
password = "Foryiuxing18!"

engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)

  


url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=d56dfda32709850e6f9e533857176f085c22106e"

def write_to_file(text):
    now = datetime.datetime.now()
    with open(f"data/bikes_{now}".replace(" ", "_"), "w") as f:
        f.write(text)

def availability_log_to_db(text):
    availability = json.loads(text)
    print(type(availability), len(availability))
    for available in availability:
        print(available)
        vals = (
            available.get("number"),
            available.get("available_bikes"),
            available.get("available_bike_stands"),
            available.get("last_update"))
 

        engine.execute("insert into availability_log values (%s, %s, %s, %s)", vals)
        
    return



def main():
    while True:
        try:
            r = requests.get(url)
            print(r, datetime.datetime.now())
            write_to_file(r.text)
            
            availability_log_to_db(r.text)
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    main()
