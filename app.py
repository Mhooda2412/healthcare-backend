from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

MONGO_DETAILS = "mongodb+srv://healtcare-db-wr:UHo5NmJA3jhr1UOx@cluster0.6w7jv.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.healtcare
collection = database.query_result


class QueryResult(BaseModel):
    query: str
    result: list


class Enrollment(BaseModel):
    type: str
    data: list


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/enrollment_geo_data")
async def get_contract_info_count():
    result = await collection.find_one({"query": "enrollment_geo_data"})

    if result:
        return QueryResult(**result)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/v1/trends_over_time")
async def get_enrolment_group_state():
    result = await collection.find_one({"query": "trends_over_time"})

    if result:
        return QueryResult(**result)
    else:
        raise HTTPException(status_code=404, detail="Item not found")
