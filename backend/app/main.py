from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "sportsdb")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

app = FastAPI(title="Football Standings API")

@app.get("/api/standings/{league_name}")
def get_standings(league_name: str):
    """Retrieve standings for the given league_name from MongoDB."""
    collection = db[league_name]

   
    try:
        standings = list(collection.find({}, {"_id": 0}))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error: unable to retrieve standings")

    if not standings:
        raise HTTPException(status_code=404, detail="League not found or no standings data available")

    return standings
