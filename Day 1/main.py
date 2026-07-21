"""
Day 1 Challenge Runner: Slot Schema & Entity Extractor.
Executes entity extraction across 14 sample sentences (including 2 German rows with inline English gloss).
"""

import json
from slot_schema import print_schema_table
from entity_extractor import extract_entities


def main():
    print("=" * 70)
    print(" PART A: TYPED SLOT SCHEMA FOR ALL SIX INTENTS")
    print("=" * 70)
    print_schema_table()
    print()

    print("=" * 70)
    print(" PART B: EXTRACTOR RUN OVER WEEK-2 TEST SENTENCES")
    print("=" * 70)

    # List of test utterances: (sentence, intent, optional comment/gloss)
    test_cases = [
        ("Remind me to buy groceries tomorrow at 5pm", "create_task"),
        ("Don't forget to submit the weekly financial report", "create_task"),
        ("Erinnere mich daran den Arzt anzurufen", "create_task"),  # = remind me to call the doctor
        ("Call Sarah on WhatsApp right now", "place_call"),
        ("Phone Alex regarding the project update", "place_call"),
        ("Ruf Mama an", "place_call"),  # = call mom
        ("Set a timer for 10 minutes", "set_timer"),
        ("Start a 45 second timer for pasta", "set_timer"),
        ("Set timer for 2 hours", "set_timer"),
        ("Save note: spent $50 on team lunch at Downtown Diner", "save_memory"),
        ("Remember that the garage door code is 4921", "save_memory"),
        ("What is the capital of France?", "answer_question"),
        ("How much does a pizza subscription cost per month?", "answer_question"),
        ("Can you play some rap music on Spotify?", "out_of_scope"),
    ]

    for idx, (text, intent) in enumerate(test_cases, 1):
        extracted_slots = extract_entities(text, intent)
        print(f"[{idx:02d}] Text  : \"{text}\"")
        print(f"     Intent: {intent}")
        print(f"     Slots : {json.dumps(extracted_slots, ensure_ascii=False)}")
        print("-" * 70)


if __name__ == "__main__":
    main()
