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

url = "dbikes.cznzccwi0urk.us-east-1.rds.amazonaws.com"
user = "admin"
database= "dbikes"
port = "3306"
password = "Foryiuxing18!"

engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)

import requests 
import traceback
import datetime 
import time
import json
url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=d56dfda32709850e6f9e533857176f085c22106e"
r = requests.get(url)


import os

if not os.path.exists("data"):
    os.makedirs("data")

def write_to_file(text):
    now = datetime.datetime.now()
    with open(f"data/bikes_{now}".replace(" ", "_"), "w") as f:
        f.write(r.text)

def update_availability(text):
    availability = json.loads(text)
    for available in availability:
        
        engine.execute("update availability set available_bikes = %s, available_bike_stands = %s, last_update = %s where number = %s", (available.get("available_bikes"), available.get("available_bike_stands"), available.get("last_update"), available.get("number")))
        
    return



def main():
    
    try:
        r = requests.get(url)
        print(r, datetime.datetime.now())
        write_to_file(r.text)
        update_availability(r.text)
        
    except:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
