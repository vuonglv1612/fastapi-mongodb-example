from pydantic import BaseModel
from typing import Any, List, Optional


class MongoDBModel(BaseModel):

    def __init__(self, **data: Any) -> None:
        # TODO: Refactor is required
        _id = self._get_mongodb_id_object(data)
        model_id = self._get_model_id()
        if isinstance(_id, dict):
            data[model_id] = _id[model_id]
            for k in _id.keys():
                if k != model_id:
                    data[k] = _id.get(k)
        super().__init__(**data)

    def _get_model_id(self) -> str:
        return "id"

    def _get_mongodb_id_object(self, data: Any) -> Any:
        return data.get("_id")


class ListResourceMeta(BaseModel):
    limit: int
    page: int
    total: int


class ListResourceResponse(BaseModel):
    items: List[BaseModel] = []
    meta: ListResourceMeta