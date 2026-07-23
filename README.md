# v4+v5 Slots & Small Models

Build Your Own AI Router — Week 5: Slots & Small Models implementation repository.

---

## 📌 Repository Overview

This repository contains the full source code and documentation for Week 5 tasks:

- 🟢 **Day 1:** Slot Schemas & Rule-Based Entity Extraction (`Day 1/`)
- 🔵 **Day 2:** Deterministic Relative Date-Time Resolver (`Day 2/`)
- 🟣 **Day 3:** Validate the Slots — The Schema Gate (`Day 3/`)

---

## 🛡️ Day 3: Validate the Slots — The Schema Gate

A from-scratch typed schema validator and safety checkpoint positioned between the slot extractor and tool executor. It intercepts and rejects malformed candidate `(action, slots)` records before they can reach the executor or trigger real-world tool failures.

### Intent Schema Contract

| Intent | Required Slots | Optional Slots | Types & Constraints |
|---|---|---|---|
| `create_task` | `text` | `due, priority` | `text: str`, `due: date (ISO 8601)`, `priority: str` |
| `place_call` | `contact` | `app` | `contact: str`, `app: str` |
| `answer_question` | `query` | `topic` | `query: str`, `topic: str` |
| `save_memory` | `note` | `category, amount` | `note: str`, `category: str`, `amount: float (>= 0)` |
| `set_timer` | `duration_seconds` | `label` | `duration_seconds: int (> 0)`, `label: str` |
| `out_of_scope` | `-` | `raw_text` | `raw_text: str` |

---

### The 5 Validation Rules

The `validate(action, slots)` gate enforces rules in strict dependency order:

1. **Unknown Intent Rejection:** Immediately rejects any `action` not present in `SCHEMA`.
2. **Required-Field Presence:** Ensures mandatory slots exist and are non-null.
3. **Type Enforcement:** Verifies slot values match Python types (`str`, `int`, `float`), guarding against Python's `bool` subclassing `int`.
4. **ISO 8601 Format Check:** Validates date fields against strict `YYYY-MM-DDThh:mm:ss` pattern (`ISO_RE`).
5. **Range & Value Constraints:** Enforces business logic (`duration_seconds > 0`, `amount >= 0`).

Returns `(ok: bool, errors: list[str])` where `errors` is deterministically sorted.

---

### Test Suite Execution & Output

```bash
python "Day 3/main.py"
```

```text
======================================================================
 DAY 3: SCHEMA GATE VALIDATOR TEST SUITE
======================================================================
[01] create_task {'text': 'buy groceries', 'due': '2026-06-25T18:00:00', 'priority': 'high'} -> OK
[02] place_call {'contact': 'Sarah', 'app': 'WhatsApp'} -> OK
[03] answer_question {'query': 'What is the capital of France?', 'topic': 'geography'} -> OK
[04] save_memory {'note': 'team lunch', 'amount': 45.5, 'category': 'food'} -> OK
[05] set_timer {'duration_seconds': 300, 'label': 'pasta'} -> OK
[06] out_of_scope {'raw_text': 'play some music'} -> OK
[07] create_task {'text': 'call mom', 'due': 'next Tuesday at 6'} -> ERROR: create_task: slot due must be ISO-8601 datetime (YYYY-MM-DDThh:mm:ss)
[08] place_call {} -> ERROR: place_call: missing required slot contact
[09] set_timer {'duration_seconds': -5} -> ERROR: set_timer: duration_seconds must be > 0
[10] save_memory {'note': 'team lunch', 'amount': -10.0, 'category': 'food'} -> ERROR: save_memory: amount must be >= 0
[11] set_timer {'duration_seconds': '300'} -> ERROR: set_timer: slot duration_seconds must be int
[12] set_tax_rate {'rate': 0.077} -> ERROR: set_tax_rate: unknown action (not in schema)
----------------------------------------------------------------------
Summary: 6 PASSED | 6 REJECTED | Total: 12
======================================================================
```

---

## 📁 Repository Structure

```
.
├── README.md
├── Day 1/
│   ├── slot_schema.py
│   ├── entity_extractor.py
│   └── main.py
├── Day 2/
│   ├── date_resolver.py
│   └── main.py
└── Day 3/
    ├── schema_validator.py
    └── main.py
```

---

## 🚀 Running All Days

```bash
# Day 1 - Entity Extraction
python "Day 1/main.py"

# Day 2 - Date Resolver
python "Day 2/main.py"

# Day 3 - Schema Gate Validator
python "Day 3/main.py"
```
