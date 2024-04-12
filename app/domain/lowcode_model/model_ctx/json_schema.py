import json
from dataclasses import dataclass
from typing import Optional, List, Dict, Union

import jsonschema
from jsonschema.validators import Draft202012Validator


def remove_required_key(json_schema: dict) -> dict:
    if "required" in json_schema:
        del json_schema["required"]
        return json_schema
    else:
        return json_schema


def get_key_from_json_path(json_path: str) -> str:
    if not json_path.startswith("$."):
        return json_path
    str_list = json_path[len('$.'):]
    # split str_list with "."
    key_list = str_list.split('.')
    if len(key_list) == 0:
        return json_path
    else:
        return key_list[0]


@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str]


error_template = "key = '{0}', error info : {1}"


def __get_err_msg(validation_error: jsonschema.exceptions.ValidationError) -> str:
    emsg = validation_error.message
    json_path = validation_error.json_path
    if json_path == "$":
        return emsg
    key = get_key_from_json_path(json_path)
    error_msg = error_template.format(key, emsg)
    return error_msg


def _validate_on_create_fail_first(data: Union[List, Dict], json_schema: dict, format_checker) -> ValidationResult:
    try:
        jsonschema.validate(instance=data, schema=json_schema, format_checker=format_checker)
        return ValidationResult(is_valid=True, error_message=None)
    except jsonschema.exceptions.ValidationError as e:
        error_msg = __get_err_msg(e)
        return ValidationResult(is_valid=False, error_message=error_msg)


def _validate_on_create_all(data: Union[List, Dict], validator):
    rtn_list = []
    error_list = validator.iter_errors(instance=data)
    for e in sorted(error_list, key=str):
        error_msg = __get_err_msg(e)
        rtn_list.append(error_msg)
    if len(rtn_list) == 0:
        return ValidationResult(is_valid=True, error_message=None)
    else:
        return ValidationResult(is_valid=False, error_message="\n".join(rtn_list))


def _get_many_schema(json_schema:dict) -> dict:
    new_json_schema = {}
    properties = json_schema.get("properties")
    required = json_schema.get("required")
    new_json_schema["properties"] = properties
    new_json_schema["type"] = "object"
    new_json_schema["required"] = required
    json_schema.pop("properties", None)
    json_schema.pop("required", None)
    json_schema["type"] = "array"
    json_schema["items"] = new_json_schema

    return json_schema

class JsonSchemaChecker:

    def __init__(self, json_schema: dict, fail_first: bool = True):
        self.fail_first = fail_first
        self.format_checker = Draft202012Validator.FORMAT_CHECKER
        self.json_schema = json_schema.copy()
        self.json_schema_create_many = _get_many_schema(json_schema.copy())
        # Remove required field
        self.json_schema_update = remove_required_key(json_schema.copy())

        self.validator = jsonschema.Draft202012Validator(self.json_schema)
        self.validator_create_many = jsonschema.Draft202012Validator(self.json_schema_create_many)
        self.validator.format_checker = self.format_checker
        self.update_validator = jsonschema.Draft202012Validator(self.json_schema_update)
        self.update_validator.format_checker = self.format_checker

    def validate_on_create(self, data: dict) -> ValidationResult:
        if self.fail_first:
            return _validate_on_create_fail_first(data, self.json_schema, self.format_checker)
        else:
            return _validate_on_create_all(data, self.validator)

    def validate_on_create_many(self, data: list) -> ValidationResult:
        if self.fail_first:
            return _validate_on_create_fail_first(data, self.json_schema_create_many, self.format_checker)
        else:
            return _validate_on_create_all(data, self.validator_create_many)

    def validate_on_update(self, data: dict):
        if self.fail_first:
            return _validate_on_create_fail_first(data, self.json_schema_update, self.format_checker)
        else:
            return _validate_on_create_all(data, self.update_validator)
