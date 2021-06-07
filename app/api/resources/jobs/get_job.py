from app.io.mongo import MongoDBClient
from typing import Dict

from app.api.dependencies import projection_query
from app.api.mongodb import mongodb as db
from app.api.schemas.jobs import Job
from fastapi import Depends, Path
from fastapi.exceptions import HTTPException
from app.config import settings


async def get_job(job_id: int = Path(..., alias="id"),
                  projection: Dict[str, int] = Depends(projection_query)):
    mongo = MongoDBClient(db.client, db.dbname)
    mongo.set_rename_mapping({"id": "_id.id"})
    collection_name = settings.mongodb_collections["jobs"]
    document = await mongo.find_one(resource=collection_name,
                                    resource_id=job_id,
                                    projection=projection)
    if not document:
        raise HTTPException(404, detail="Not found")
    job = Job(**document)
    return job
