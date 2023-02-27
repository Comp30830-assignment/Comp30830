import requests
import traceback
import datetime
import time
import json
import createDatabase

APIKEY = "43320d58946b9083c60d5f540941c6249d9884a4"
NAME = "dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"


def write_to_file(text):
    now = datetime.datetime.now()
    with open("data/bikes_{}".format(now).replace(" ", "_").replace(":", "-"), "w") as f:
        f.write(text)
    with open("stations.json", "w") as json_data:
        json_data.write(text)


def availability_fix_keys(availability):
    availability['number'] = availability['number']
    availability['available_bikes'] = availability['available_bikes']
    availability['available_bike_stands'] = availability['available_bike_stands']
    availability['last_update'] = availability['last_update']
    return availability

def stations_fix_keys(station):
    station['position_lat'] = station['position']['lat']
    station['position_lng'] = station['position']['lng']
    return station

def write_to_db(text):
    availabilities = json.loads(open('stations.json', 'r').read())
    createDatabase.engine.execute(createDatabase.availability.insert(), *map(availability_fix_keys, availabilities))
    stations = json.loads(open('stations.json', 'r').read())
    createDatabase.engine.execute(createDatabase.station.insert(), *map(stations_fix_keys, stations))


def main():
    while True:
        try:
            r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
            print(r, datetime.datetime.now())
            write_to_file(r.text)
            write_to_db(r.text)
            time.sleep(5*60)
        except:

            print(traceback.format_exc())

if __name__ == '__main__':
    main()