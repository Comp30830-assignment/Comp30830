#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:





# In[3]:


engine = create_engine(f"mysql+mysqldb://{user}:{password}@{url}:{port}/{database}", echo=True)


# In[4]:


sql = """use test"""
engine.execute(sql)


# In[5]:


sql = """drop table test.availability"""
engine.execute(sql)


# In[6]:


sql = """drop table test.station"""
engine.execute(sql)


# In[7]:


sql ="""
CREATE TABLE IF NOT EXISTS station (
address VARCHAR(256),
banking int,
bike_stands int,
bonus int, 
contract_name varchar(256),
name varchar(256),
number int primary key,
position_lat real,
position_lng real,
status varchar(256))"""

try:
    res = engine.execute("drop table if exists station")
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)


# In[9]:


sql = """
Create table if not exists availability (
number int primary key,
available_bikes int,
available_bike_stands int,
last_update bigint
)"""

try:
    
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)


# In[10]:


import requests 
import traceback
import datetime 
import time
import json

url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=d56dfda32709850e6f9e533857176f085c22106e"
r = requests.get(url)
def write_to_file(text):
    now = datetime.datetime.now()
    with open(f"data/bikes_{now}".replace(" ", "_"), "w") as f:
        f.write(r.text)

def stations_to_db(text):
    
    stations = json.loads(text)
    print(type(stations), len(stations))
    for station in stations:
        print(station)
        vals = (
            station.get('address'),
            int(station.get('banking')),
            station.get('bike_stands'),
            int(station.get('bonus')),
            station.get('contract_name'),
            station.get('name'),
            station.get('number'),
            station.get('position').get('lat'),
            station.get('position').get('lng'),
            station.get('status')
        )

        engine.execute("insert into station values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
    return
stations_to_db(r.text)


# In[11]:


url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=d56dfda32709850e6f9e533857176f085c22106e"
r = requests.get(url)
def write_to_file(text):
    now = datetime.datetime.now()
    with open(f"data/bikes_{now}".replace(" ", "_"), "w") as f:
        f.write(r.text)
        
def availability_to_db(text):
    availability = json.loads(text)
    print(type(availability), len(availability))
    for available in availability:
        print(available)
        vals = (
            available.get("number"),
            available.get("available_bikes"),
            available.get("available_bike_stands"),
            available.get("last_update"))
 

        engine.execute("insert into availability values (%s, %s, %s, %s)", vals)
        
    return
availability_to_db(r.text)


# In[ ]:



url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=d56dfda32709850e6f9e533857176f085c22106e"
r = requests.get(url)



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
    while True:
        try:
            r = requests.get(url)
            print(r, datetime.datetime.now())
            write_to_file(r.text)
            update_availability(r.text)
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    main()


# In[ ]:




