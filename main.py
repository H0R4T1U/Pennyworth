import json 
from typing import Annotated
from reservation_model import Reservation
from fastapi import FastAPI,Form
from repository import Repo
app = FastAPI()
repository = Repo()
@app.get("/fetch")
async def fetch():
    data = json.load(open("data.json"))
    return data

@app.post("/add")
async def add(rsv: Reservation):
    try:
        Reservation.model_validate(rsv)
        repository.add(rsv)
        repository.save_data()
    except:
        print("Invalid Data!")
    

@app.post("/delete")
async def delete(rsv:Reservation):
    try:
        Reservation.model_validate(rsv)
        repository.delete(rsv)
        repository.save_data();
    except:
        print("Invalid Data!")
