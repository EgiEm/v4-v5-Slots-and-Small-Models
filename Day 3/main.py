from schema_validator import SCHEMA, validate


def main():
    test_cases = [
        # --- VALID RECORDS ---
        {
            "action": "create_task",
            "slots": {
                "text": "buy groceries",
                "due": "2026-06-25T18:00:00",
                "priority": "high",
            },
        },
        {
            "action": "place_call",
            "slots": {"contact": "Sarah", "app": "WhatsApp"},
        },
        {
            "action": "answer_question",
            "slots": {"query": "What is the capital of France?", "topic": "geography"},
        },
        {
            "action": "save_memory",
            "slots": {"note": "team lunch", "amount": 45.50, "category": "food"},
        },
        {
            "action": "set_timer",
            "slots": {"duration_seconds": 300, "label": "pasta"},
        },
        {
            "action": "out_of_scope",
            "slots": {"raw_text": "play some music"},
        },
        # --- BROKEN / REJECTED RECORDS ---
        {
            "action": "create_task",
            "slots": {"text": "call mom", "due": "next Tuesday at 6"},
        },
        {
            "action": "place_call",
            "slots": {},
        },
        {
            "action": "set_timer",
            "slots": {"duration_seconds": -5},
        },
        {
            "action": "save_memory",
            "slots": {"note": "team lunch", "amount": -10.0, "category": "food"},
        },
        {
            "action": "set_timer",
            "slots": {"duration_seconds": "300"},
        },
        {
            "action": "set_tax_rate",
            "slots": {"rate": 0.077},
        },
    ]

    print("======================================================================")
    print(" DAY 3: SCHEMA GATE VALIDATOR TEST SUITE")
    print("======================================================================")

    passed_count = 0
    rejected_count = 0

    for idx, case in enumerate(test_cases, 1):
        action = case["action"]
        slots = case["slots"]
        ok, errors = validate(action, slots)

        if ok:
            passed_count += 1
            print(f"[{idx:02d}] {action} {slots} -> OK")
        else:
            rejected_count += 1
            err_str = "; ".join(errors)
            print(f"[{idx:02d}] {action} {slots} -> ERROR: {err_str}")

    print("----------------------------------------------------------------------")
    print(f"Summary: {passed_count} PASSED | {rejected_count} REJECTED | Total: {len(test_cases)}")
    print("======================================================================")


if __name__ == "__main__":
    main()
