from typing import Any, Dict, List, Optional, Tuple, Union
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
import copy


class MongoDBClient:
    def __init__(self, client: AsyncIOMotorClient, dbname: str) -> None:
        self._client = client
        self._db = self._client[dbname]
        self._rename_mapping = dict()
        self._id_type = str
        self._id_key = "id"

    def set_id_type(self, id_type: Any) -> None:
        self._id_type = id_type

    def set_id_key(self, key: str) -> None:
        self._id_key = key

    def _cast_id(self, resource_id) -> Any:
        return self._id_type(resource_id)

    def _get_collection(self, resource: str) -> AsyncIOMotorCollection:
        return self._db[resource]

    def set_rename_mapping(self, rename_mapping: Dict[str, str]) -> None:
        if not isinstance(rename_mapping, dict):
            raise ValueError("Rename mapping is a dictionary")
        self._rename_mapping = rename_mapping

    def _mongotize(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        # TODO
        return self._rename_fields(filters)

    def _rename_fields(self, document: Dict[str, Any]) -> Dict[str, Any]:
        doc = copy.deepcopy(document)
        for k in doc.keys():
            value = doc.get(k)
            if k in self._rename_mapping:
                new_name = self._rename_mapping[k]
                if isinstance(value, dict):
                    doc[new_name] = self._rename_fields(value)
                else:
                    doc[new_name] = value
                doc.pop(k)
            else:
                if isinstance(value, dict):
                    doc[k] = self._rename_fields(value)
        return doc

    async def find(self,
                resource: str,
                filters: Optional[Dict[str, Any]] = None,
                sort: Optional[Dict[str, int]] = None,
                projection: Optional[Dict[str, int]] = None,
                limit: Optional[int] = None,
                skip: int = 0):
        collection = self._get_collection(resource=resource)
        options = dict()
        if filters:
            options["filter"] = self._mongotize(filters=filters)
        if projection:
            options["projection"] = self._mongotize(projection)
        if limit and limit > 0:
            options["limit"] = limit
        if skip and skip > 0:
            options["skip"] = skip
        cursor = collection.find(**options)
        if sort:
            for k, v in self._mongotize(sort).items():
                cursor.sort(k, v)
        return await cursor.to_list(length=None)

    async def find_one(self, resource: str,
                       resource_id: Any,
                       projection: Optional[Dict[str, Any]] = None
                       ) -> Dict[str, Any]:
        collection = self._get_collection(resource)
        filters = {
            "id": resource_id
        }
        args = {"filter": self._mongotize(filters)}
        if projection:
            args["projection"] = self._mongotize(projection)
        document = await collection.find_one(**args)
        if not document:
            return dict()
        return document

    async def count(self, resource: str, filters: Optional[Dict[str, Any]] =  None) -> int:
        collection = self._get_collection(resource=resource)
        if filters:
            return await collection.count_documents(self._mongotize(filters))
        return await collection.count_documents({})
