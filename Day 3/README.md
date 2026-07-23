# Day 3: Validate the Slots — The Schema Gate

A typed schema gate validator implemented from scratch to ensure malformed slot records are intercepted before reaching the executor.

## Part A: Full Intent Schema Contract

| Intent | Required Slots | Optional Slots | Types & Constraints |
|---|---|---|---|
| `create_task` | `text` | `due, priority` | `text: str`, `due: date (ISO 8601)`, `priority: str` |
| `place_call` | `contact` | `app` | `contact: str`, `app: str` |
| `answer_question` | `query` | `topic` | `query: str`, `topic: str` |
| `save_memory` | `note` | `category, amount` | `note: str`, `category: str`, `amount: float (>= 0)` |
| `set_timer` | `duration_seconds` | `label` | `duration_seconds: int (> 0)`, `label: str` |
| `out_of_scope` | `-` | `raw_text` | `raw_text: str` |

---

## Part B: The 5 Validation Rules

The `validate(action, slots)` function evaluates records strictly in dependency order:

1. **Unknown Intent Rejection:** Rejects immediately if `action` is not defined in `SCHEMA`.
2. **Required Slot Presence:** Checks that every mandatory slot for the given intent is present and non-null.
3. **Type Enforcement:** Verifies that slot values match expected Python types (`str`, `int`, `float`), explicitly guarding against Python's `bool` subclassing `int`.
4. **ISO 8601 Date Check:** Verifies date slots match strict ISO 8601 format (`YYYY-MM-DDThh:mm:ss`) via regex pattern matching.
5. **Range & Value Constraints:** Validates domain logic constraints such as `duration_seconds > 0` for timers and `amount >= 0` for expense/memory entries.

The validator returns a tuple `(ok: bool, errors: list[str])`, where `errors` is deterministically sorted.

---

## Test Output & Stressed Validation Suite

Running `python "Day 3/main.py"` executes 12 test cases (6 valid, 6 broken):

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

## How to Run

```bash
python "Day 3/main.py"
```
