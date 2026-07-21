"""
Typed Slot Schema Definition for NLP Intents.
Defines required and optional slots with explicit data types for all six intents.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class SlotSpec:
    intent: str
    required_slots: Dict[str, str]  # slot_name -> type_name
    optional_slots: Dict[str, str]  # slot_name -> type_name


SLOT_SCHEMAS: Dict[str, SlotSpec] = {
    "create_task": SlotSpec(
        intent="create_task",
        required_slots={"text": "str"},
        optional_slots={"due": "datetime", "priority": "str"}
    ),
    "place_call": SlotSpec(
        intent="place_call",
        required_slots={"contact": "str"},
        optional_slots={"app": "str"}
    ),
    "set_timer": SlotSpec(
        intent="set_timer",
        required_slots={"duration_seconds": "int"},
        optional_slots={"label": "str"}
    ),
    "save_memory": SlotSpec(
        intent="save_memory",
        required_slots={"note": "str"},
        optional_slots={"category": "str", "amount": "str"}
    ),
    "answer_question": SlotSpec(
        intent="answer_question",
        required_slots={"query": "str"},
        optional_slots={"topic": "str"}
    ),
    "out_of_scope": SlotSpec(
        intent="out_of_scope",
        required_slots={},
        optional_slots={"raw_text": "str"}
    ),
}


def print_schema_table() -> None:
    """Prints the slot schema as a Markdown-formatted table."""
    headers = ["intent", "required slots", "optional slots", "type"]
    print(f"| {' | '.join(headers)} |")
    print(f"| {' | '.join(['---'] * len(headers))} |")

    for intent, spec in SLOT_SCHEMAS.items():
        req = ", ".join(spec.required_slots.keys()) or "-"
        opt = ", ".join(spec.optional_slots.keys()) or "-"
        
        # Combine types
        all_types = {**spec.required_slots, **spec.optional_slots}
        types_str = ", ".join([f"{k}: {v}" for k, v in all_types.items()]) if all_types else "-"
        
        print(f"| `{intent}` | `{req}` | `{opt}` | `{types_str}` |")


if __name__ == "__main__":
    print_schema_table()
