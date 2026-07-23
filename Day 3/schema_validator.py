import re

# ISO 8601 regex: YYYY-MM-DDThh:mm:ss
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")

# Type checks table mapping schema type names to Python types
TYPE_CHECKS = {
    "str": str,
    "int": int,
    "float": (float, int),  # float fields accept int or float (e.g. 50 or 50.0)
    "date": str,            # date slots are validated as ISO strings
}

# Full Schema for all six Week-2 intents
SCHEMA = {
    "create_task": {
        "required": {"text": "str"},
        "optional": {"due": "date", "priority": "str"},
    },
    "place_call": {
        "required": {"contact": "str"},
        "optional": {"app": "str"},
    },
    "answer_question": {
        "required": {"query": "str"},
        "optional": {"topic": "str"},
    },
    "save_memory": {
        "required": {"note": "str"},
        "optional": {"category": "str", "amount": "float"},
    },
    "set_timer": {
        "required": {"duration_seconds": "int"},
        "optional": {"label": "str"},
    },
    "out_of_scope": {
        "required": {},
        "optional": {"raw_text": "str"},
    },
}


def validate(action: str, slots: dict) -> tuple[bool, list[str]]:
    """
    Validates an (action, slots) record against the SCHEMA gate contract.

    Validation rules applied in dependency order:
    1. Unknown-intent rejection: Action must exist in SCHEMA.
    2. Required-field presence: All required slots must be present.
    3. Type checks: Slot values must match declared types (excluding bools for numeric/string types).
    4. ISO-date format check: Date slots must match ISO 8601 format (YYYY-MM-DDThh:mm:ss).
    5. Range & value constraints: duration_seconds > 0, amount >= 0.

    Returns:
        (ok, errors): ok is True if errors is empty; errors is a sorted list of error strings.
    """
    errors = []

    # Rule 1: Unknown-intent rejection
    if action not in SCHEMA:
        return False, [f"{action}: unknown action (not in schema)"]

    intent_schema = SCHEMA[action]
    required_slots = intent_schema.get("required", {})
    optional_slots = intent_schema.get("optional", {})
    all_known_slots = {**required_slots, **optional_slots}

    # Rule 2: Required-field presence check
    for req_slot in required_slots:
        if req_slot not in slots or slots[req_slot] is None:
            errors.append(f"{action}: missing required slot {req_slot}")

    # Rule 3, 4, 5: Check each provided slot
    for slot, val in slots.items():
        if val is None:
            continue

        if slot in all_known_slots:
            expected_type_str = all_known_slots[slot]
            expected_type = TYPE_CHECKS.get(expected_type_str)

            # Rule 3: Type checks (Exclude bool in Python since bool inherits from int)
            type_ok = False
            if type(val) is not bool:
                if isinstance(expected_type, tuple):
                    type_ok = isinstance(val, expected_type)
                elif expected_type and isinstance(val, expected_type):
                    type_ok = True

            if not type_ok:
                errors.append(f"{action}: slot {slot} must be {expected_type_str}")
                continue  # Skip format & constraint checks if type is invalid

            # Rule 4: ISO-date format check
            if expected_type_str == "date":
                if not ISO_RE.match(val):
                    errors.append(
                        f"{action}: slot {slot} must be ISO-8601 datetime (YYYY-MM-DDThh:mm:ss)"
                    )

            # Rule 5: Range & Constraint checks
            if action == "set_timer" and slot == "duration_seconds":
                if val <= 0:
                    errors.append("set_timer: duration_seconds must be > 0")

            if action == "save_memory" and slot == "amount":
                if val < 0:
                    errors.append("save_memory: amount must be >= 0")

    # Sort errors for deterministic output
    errors.sort()
    return len(errors) == 0, errors
