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


url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&units=metric&appid=925fb7d8a523499058239184ca7054d9"
import datetime
def write_to_file2(text):
    now = datetime.datetime.now()
    with open(f"data/weather_{now}".replace(" ", "_").replace(":", "-"), "w") as f:
        f.write(text) 
        
def weather_to_db(text):
    weather = json.loads(text)
    print(type(weather),len(weather))
    print(text)
    now = datetime.datetime.now()
    vals = (
            weather.get("coord").get("lon"),
            weather.get("coord").get("lat"),
            weather.get("weather")[0].get("description"),
            weather.get("main").get("temp"),
            weather.get("main").get("feels_like"),
            weather.get("main").get("temp_min"),
            weather.get("main").get("temp_max"),
            weather.get("visibility"),
            weather.get("wind").get("speed"),
            weather.get("sys").get("sunrise"),
            weather.get("sys").get("sunrise"))
        
    
    
    print("\n\n\nVALS:{}\n\n\n".format(vals))
    engine.execute("insert into weather values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
    
def weather_main():
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&units=metric&appid=925fb7d8a523499058239184ca7054d9"

        weather = requests.get(url)
        write_to_file2(weather.text)
        weather_to_db(weather.text)
    except:
          print(traceback.format_exc())
          if engine is None:
                return

if __name__ == "__main__":
    weather_main() 
