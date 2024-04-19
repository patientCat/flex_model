from typing import TypedDict


class SchemaKey(TypedDict, total=False):
    format: str  # noqa
    type: str
    xRelation: str  # noqa


SCHEMA_KEYS: SchemaKey = {
    "format": "format",
    "type": "type",
    "xRelation": "xRelation"
}
