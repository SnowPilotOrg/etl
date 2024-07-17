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


# Now here are the Iterable-specific models


class ProjectType(str, Enum):
    user_id_based = "user_id_based"
    # email_based = "email_based" # TODO: Support this in the future


class Region(str, Enum):
    us = "us"
    # eu = "eu" # TODO: Support this in the future


class Config(BaseModel):
    api_key: str
    project_type: ProjectType
    region: Region


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    user_id: str
    email: Optional[str] = None
    data_fields: Dict[str, Any] = {}
