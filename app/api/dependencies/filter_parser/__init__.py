from typing import Any, Dict, Optional

from app.api.constants.pagination import DEFAULT_LIMIT, DEFAULT_PAGE
from fastapi import Query
from pydantic import Json

from .utils import parse_sort_query


def filter_query(where: Optional[Json] = Query(None)) -> Dict[str, Any]:
    if not where:
        return {}
    return where


def sort_query(sort: Optional[str] = Query(None)) -> Dict[str, int]:
    if not sort:
        return {}
    return parse_sort_query(sort)


def projection_query(projection: Optional[Json] = Query(None)) -> Dict[str,
                                                                       int]:
    if not projection:
        return dict()
    return projection


def pagination_query(limit: Optional[int] = Query(None),
                     page: Optional[int] = Query(None)) -> Dict[str, int]:
    query = {}
    if not limit:
        limit = DEFAULT_LIMIT
    if not page:
        page = DEFAULT_PAGE

    query["limit"] = limit
    query["page"] = page
    if page > 1:
        query["skip"] = (page - 1) * limit
    return query
