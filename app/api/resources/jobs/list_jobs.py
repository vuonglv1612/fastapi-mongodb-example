from app.io.mongo import MongoDBClient
from typing import Dict

from app.api.dependencies import (filter_query, pagination_query,
                                  projection_query, sort_query)
from app.api.mongodb import mongodb as db
from app.api.schemas.jobs import Job, ListJobsResponse
from fastapi import Depends
from pydantic import Json
from app.config import settings


async def list_jobs(filters: Dict[str, str] = Depends(filter_query),
                    sort: Dict[str, int] = Depends(sort_query),
                    projection: Json = Depends(projection_query),
                    pagination: Dict[str, int] = Depends(pagination_query)):
    mongo = MongoDBClient(db.client, db.dbname)
    mongo.set_rename_mapping({"id": "_id.id"})

    options = {
        "resource": settings.mongodb_collections["jobs"],
        "filters": filters,
        "sort": sort,
        "projection": projection
    }
    if pagination:
        options["limit"] = pagination["limit"]
        options["skip"] = pagination.get("skip", 0)
    documents = await mongo.find(**options)
    jobs = []
    for document in documents:
        job = Job(**document)
        jobs.append(job)
    total = await mongo.count(resource=settings.mongodb_collections["jobs"],
                               filters=filters)
    meta = {
        "total": total,
        **pagination
    }
    response = ListJobsResponse(items=documents, meta=meta)
    return response
