import json
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, field_serializer
from typing_extensions import Literal


class Config(BaseModel):
    csv_path: str


# TODO: types below are not specific to CSV, but are used for all connectors
# we should extract this out into a package.

# should this be Type[BaseModel] or Type[Dict[str, Any]]?
Schema = Type[BaseModel]


class CollectionMetadata(BaseModel):
    id: str
    label: str
    row: Optional[Schema] = None
    insert: Optional[Schema] = None
    update: Optional[Schema] = None
    upsert: Optional[Schema] = None
    delete: Optional[Schema] = None

    @field_serializer("row", "insert", "update", "upsert", "delete", when_used="json")
    def serialize_schema(value: Optional[Schema]):
        if value is None:
            return None
        return value.model_json_schema()


class Discovery(BaseModel):
    collections: list[CollectionMetadata]
