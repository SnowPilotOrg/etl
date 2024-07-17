import json
from enum import Enum, IntEnum
from typing import Any, Dict, Optional, Type

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    model_serializer,
)
from pydantic.alias_generators import to_camel
from typing_extensions import Literal

# TODO: types below are not specific to any one connector, but are used for all connectors
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

    # @model_serializer()
    # def serialize_model(self, when_used="json-unless-none"):
    #     return self.model_dump_json()

    @field_serializer(
        "row", "insert", "update", "upsert", "delete", when_used="json-unless-none"
    )
    def serialize_schema(value: Optional[Schema]):
        if value is None:
            return None
        return value.model_json_schema()


class Catalog(BaseModel):
    collections: list[CollectionMetadata]


# Now here are the Snowflake-specific models


class Config(BaseModel):
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    schema: str
