# v4+v5 Slots & Small Models

Day 1 implementation of intent slot schemas and entity extraction.

## Part A: Slot Schema Table

| intent | required slots | optional slots | type |
| --- | --- | --- | --- |
| `create_task` | `text` | `due, priority` | `text: str, due: datetime, priority: str` |
| `place_call` | `contact` | `app` | `contact: str, app: str` |
| `set_timer` | `duration_seconds` | `label` | `duration_seconds: int, label: str` |
| `save_memory` | `note` | `category, amount` | `note: str, category: str, amount: str` |
| `answer_question` | `query` | `topic` | `query: str, topic: str` |
| `out_of_scope` | `-` | `raw_text` | `raw_text: str` |

## Part B: Extractor Features

Rule-based entity extractor (`Day 1/entity_extractor.py`) for parsing raw utterances:
- `contact`: recipient names for calls ("Call Sarah on WhatsApp", "Ruf Mama an")
- `duration_seconds`: natural time expressions converted to integer seconds ("10 minutes" -> `600`, "45 secs" -> `45`, "2 hours" -> `7200`)
- `amount`: monetary amounts ("$50", "€20")
- `text`: task action payload ("remind me to buy groceries")

## Repository Structure

```
.
├── README.md
└── Day 1/
    ├── slot_schema.py
    ├── entity_extractor.py
    └── main.py
```

## Running the Code

```bash
python "Day 1/main.py"
```

### Output Example

```text
======================================================================
 PART A: TYPED SLOT SCHEMA FOR ALL SIX INTENTS
======================================================================
| intent | required slots | optional slots | type |
| --- | --- | --- | --- |
| `create_task` | `text` | `due, priority` | `text: str, due: datetime, priority: str` |
| `place_call` | `contact` | `app` | `contact: str, app: str` |
| `set_timer` | `duration_seconds` | `label` | `duration_seconds: int, label: str` |
| `save_memory` | `note` | `category, amount` | `note: str, category: str, amount: str` |
| `answer_question` | `query` | `topic` | `query: str, topic: str` |
| `out_of_scope` | `-` | `raw_text` | `raw_text: str` |

======================================================================
 PART B: EXTRACTOR RUN OVER WEEK-2 TEST SENTENCES
======================================================================
[01] Text  : "Remind me to buy groceries tomorrow at 5pm"
     Intent: create_task
     Slots : {"text": "buy groceries tomorrow at 5pm", "due": "tomorrow"}
----------------------------------------------------------------------
[03] Text  : "Erinnere mich daran den Arzt anzurufen"
     Intent: create_task
     Slots : {"text": "den Arzt anzurufen"}
----------------------------------------------------------------------
[04] Text  : "Call Sarah on WhatsApp right now"
     Intent: place_call
     Slots : {"contact": "Sarah", "app": "WhatsApp"}
----------------------------------------------------------------------
[06] Text  : "Ruf Mama an"
     Intent: place_call
     Slots : {"contact": "Mama"}
----------------------------------------------------------------------
[07] Text  : "Set a timer for 10 minutes"
     Intent: set_timer
     Slots : {"duration_seconds": 600}
----------------------------------------------------------------------
[10] Text  : "Save note: spent $50 on team lunch at Downtown Diner"
     Intent: save_memory
     Slots : {"note": "spent $50 on team lunch at Downtown Diner", "amount": "$50"}
----------------------------------------------------------------------
```
