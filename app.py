from datetime import datetime

from fastapi import FastAPI, HTTPException
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
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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


# Convert year and month to a sortable format
def parse_date(year, month):
    return datetime.strptime(f"{year}-{month}", "%Y-%m")


@app.get("/api/v1/current_ma_enrollments")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "current_year_plan_filter"})
    if result:
        # Sort the data by year and month
        sorted_data = sorted(result['data'], key=lambda x: parse_date(x['year'], x['month']))

        # Extract the latest total_enrollment
        latest_enrollment = sorted_data[-1]['total_enrollment']

        return {"latest_enrollment": latest_enrollment}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/v1/total_medicare_enrollments")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "current_year_no_plan_filter"})
    if result:
        # Sort the data by year and month
        sorted_data = sorted(result['data'], key=lambda x: parse_date(x['year'], x['month']))

        # Extract the latest total_enrollment
        latest_enrollment = sorted_data[-1]['total_enrollment']

        return {"latest_enrollment": latest_enrollment}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/v1/current_month_state_plan")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "current_month_state_plan"})
    if result:
        current_month_state_plan = result.get("data")

        return {"current_month_state_plan": current_month_state_plan}
    else:
        raise HTTPException(status_code=404, detail="Item not found")



@app.get("/api/v1/trend_over_time")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "trend_over_time"})
    if result:
        trend_over_time = result.get("data")

        return {"trend_over_time": trend_over_time}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/v1/plan_with_parent_org_filter")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "plan_with_parent_org_filter"})
    if result:
        plan_with_parent_org_filter = result.get("data")

        return {"plan_with_parent_org_filter": plan_with_parent_org_filter}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/api/v1/plan")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "plan"})
    if result:
        plan = result.get("data")

        return {"plan": plan}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/v1/state_enrollment")
async def get_current_ma_enrollments():
    collection = database.enrollment
    result = await collection.find_one({"type": "state_enrollment"})
    if result:
        state_enrollment = result.get("data")

        return {"state_enrollment": state_enrollment}
    else:
        raise HTTPException(status_code=404, detail="Item not found")