from fastapi import FastAPI
from app.api.mongodb import mongodb
from app.api.resources import jobs

app = FastAPI()


@app.on_event("startup")
def create_mongodb_client():
    mongodb.init()


@app.on_event("shutdown")
def close_mongodb():
    mongodb.disconnect()


app.include_router(jobs.router)