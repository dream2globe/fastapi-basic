import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = []
URL = "http://worldtimeapi.org/api/timezone"


class City(BaseModel):
    name: str
    timezone: str


@app.get("/")
def root():
    return {"Hello": "World!"}


@app.get("/cities")
def get_cities():
    results = []
    for city in db:
        url = f"{URL}/{city['timezone']}"
        r = requests.get(url)
        cur_time = r.json()["datetime"]
        results.append(
            {"name": city["name"], "timezon": city["timezone"], "current_time": cur_time}
        )
    return results


@app.get("/cities/{citi_id}")
def get_city(city_id: int):
    city = db[city_id - 1]
    url = f"{URL}/{city['timezone']}"
    r = requests.get(url)
    cur_time = r.json()["datetime"]
    return {"name": city["name"], "timezon": city["timezone"], "current_time": cur_time}


@app.post("/cities")
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete("/cities/{citi_id}")
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}
