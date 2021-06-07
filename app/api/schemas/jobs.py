from datetime import datetime
from typing import List, Optional
from .base import MongoDBModel, ListResourceResponse


class Job(MongoDBModel):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    title: Optional[str] = None
    salary: Optional[int] = None
    address: Optional[str] = None
    description: Optional[str] = None
    employer_id: Optional[int] = None
    is_open: Optional[bool] = None

class ListJobsResponse(ListResourceResponse):
    items: List[Job] = []