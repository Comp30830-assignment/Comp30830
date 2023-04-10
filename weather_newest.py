from sqlalchemy import create_engine
import traceback
import json
import requests
import time

url = "dbikes.cznzccwi0urk.us-east-1.rds.amazonaws.com"
user = "admin"
database = "dbikes"
port = "3306"
password = "Foryiuxing18!"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{url}:{port}/{database}", echo=True)

url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&units=metric&appid=925fb7d8a523499058239184ca7054d9"


def update_db(text):
    weather = json.loads(text)
    print(type(weather), len(weather))
    print(text)
    vals = (
        weather.get("weather")[0].get("icon"),
        weather.get("weather")[0].get("description"),
        weather.get("main").get("temp"),
        weather.get("dt"))

    print("\n\n\nVALS:{}\n\n\n".format(vals))
    engine.execute("delete from weather_newest limit 1")
    engine.execute("insert into weather_newest values(%s, %s, %s, %s)", vals)


def weather_newest_main():
    url = "https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&units=metric&appid=925fb7d8a523499058239184ca7054d9"
    sql = """
            CREATE TABLE IF NOT EXISTS weather_newest (
            icon VARCHAR(256),
            description VARCHAR(256),
            temp INTEGER,
            dt INTEGER
            )
            """
    engine.execute(sql)
    while True:
        try:
            weather = requests.get(url)
            update_db(weather.text)
            time.sleep(1 * 60 * 60)
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    weather_newest_main()
