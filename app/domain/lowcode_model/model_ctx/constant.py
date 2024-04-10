from typing import TypedDict


class SchemaKey(TypedDict, total=False):
    FORMAT: str  # noqa
    TYPE: str


SCHEMA_KEYS = {
    "FORMAT": "format",
    "TYPE": "type",
}
