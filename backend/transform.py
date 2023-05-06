import json
from typing import Any
from collections import defaultdict


def transform_openapi_to_json_schema(openapi_json: dict[str, Any]) -> dict[str, Any]:
    paths = openapi_json["paths"]
    subject_to_paths = defaultdict(dict)
    for path, params in paths.items():
        subject = path.split("/")[2]
        subject_to_paths[subject][path] = params
    components = remove_builtins_from_components(openapi_json["components"])

    subject_schemas = []
    for subject, paths in subject_to_paths.items():
        subject_schema = transform_subject_to_json_schema(paths)
        subject_schema["properties"]["type"] = {
            "type": "string",
            "const": subject
        }
        subject_schemas.append(subject_schema)

    return {
        "components": components,
        "oneOf": subject_schemas
    }

def transform_subject_to_json_schema(subject_paths: list[dict[str, Any]]):
    schema_builder = {
        "type": "object",
        "properties": {
            "question_validations": {
                "type": "object",
                "properties": {}
            },
            "test_validations": {
                "type": "object",
                "properties": {}
            },
        },
        "required": ["question_validations", "test_validations", "check"],
        "additionalProperties": False
    }
    for path, params in subject_paths.items():
        schema = transform_post_to_json_schema(params["post"])
        match path.split("/")[1:]:
            case "api", subject, "validate", "question", name:
                schema_builder["properties"]["question_validations"]["properties"][name] = schema
            case "api", subject, "validate", "test", name:
                schema_builder["properties"]["test_validations"]["properties"][name] = schema
            case "api", subject, "check", "teacher":
                schema_builder["properties"]["check"] = schema
    return schema_builder

def transform_post_to_json_schema(post_params: dict[str, Any]):
    schema = post_params["requestBody"]["content"]["application/json"]["schema"]
    schema["additionalProperties"] = False
    return schema


def remove_builtins_from_components(components):
    new_components = components.copy()
    for schema in new_components["schemas"].values():
        if "test" in schema.get("required", []) or "q" in schema.get("required", []):
            schema["required"] = [r for r in schema["required"] if r != "test" and r != "q"]
            schema["properties"].pop("test", None)
            schema["properties"].pop("q", None)
    return new_components
