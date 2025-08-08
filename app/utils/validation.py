from typing import Any, Dict, Optional
from jsonschema import validate, Draft202012Validator
from jsonschema.exceptions import ValidationError


def validate_payload(payload: Dict[str, Any], schema: Optional[Dict[str, Any]]):
    if not schema:
        return
    # Will raise ValidationError if invalid
    Draft202012Validator.check_schema(schema)
    validate(instance=payload, schema=schema)