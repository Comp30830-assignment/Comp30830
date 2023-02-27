import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display

URI = "dbikes.cizsqkc3mbbs.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "sys"
USER = "admin"
PASSWORD = "niuzhaozhong"
# database driver is mysqlconnector
engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# sql = """
# CREATE DATABASE IF NOT EXISTS dbikes;
# """
# engine.execute(sql)

# sql = """
# use dbikes
# """
# engine.execute(sql)
#
# sql = """
# CREATE TABLE IF NOT EXISTS station (
# address VARCHAR(256),
# banking INTEGER,
# bike_stands INTEGER,
# bonus INTEGER,
# contract_name VARCHAR(256),
# name VARCHAR(256),
# number INTEGER,
# position_lat REAL,
# position_lng REAL,
# status VARCHAR(256)
# )
# """
# try:
#     res = engine.execute(sql)
#     print(res.fetchall())
# except Exception as e:
#     print(e)
#
# sql = """
# use dbikes
# """
# engine.execute(sql)
#
# sql = """
# CREATE TABLE IF NOT EXISTS availability (
# number INTEGER,
# available_bikes INTEGER,
# available_bike_stands INTEGER,
# last_update INTEGER
# )
# """
# try:
#     res = engine.execute(sql)
#     print(res.fetchall())
# except Exception as e:
#     print(e)

DB = "dbikes"
engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

metadata = sqla.MetaData()

station = sqla.Table("station", metadata,
    sqla.Column('address', sqla.String(256), nullable=False),
    sqla.Column('banking', sqla.Integer),
    sqla.Column('bike_stands', sqla.Integer),
    sqla.Column('bonus', sqla.Integer),
    sqla.Column('contract_name', sqla.String(256)),
    sqla.Column('name', sqla.String(256)),
    sqla.Column('number', sqla.Integer),
    sqla.Column('position_lat', sqla.REAL),
    sqla.Column('position_lng', sqla.REAL),
    sqla.Column('status', sqla.BigInteger)
)

availability = sqla.Table("availability", metadata,
    sqla.Column('available_bikes', sqla.Integer),
    sqla.Column('available_bike_stands', sqla.Integer),
    sqla.Column('number', sqla.Integer),
    sqla.Column('last_update', sqla.Integer),
)

try:
    station.drop(engine)
    availability.drop(engine)
except:
    pass

metadata.create_all(engine)