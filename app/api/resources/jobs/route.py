from app.api.schemas.jobs import Job, ListJobsResponse
from fastapi import APIRouter

from .get_job import get_job
from .list_jobs import list_jobs

router = APIRouter(tags=["jobs"])

router.add_api_route("/jobs/{id}",
                     get_job,
                     methods=["GET"],
                     response_model=Job,
                     response_model_exclude_none=True)

router.add_api_route("/jobs",
                     list_jobs,
                     methods=["GET"],
                     response_model=ListJobsResponse,
                     response_model_exclude_none=True)
