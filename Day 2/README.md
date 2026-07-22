# Day 2: Deterministic Date-Time Resolver

A deterministic relative date-time phrase resolver built from scratch to normalize relative date-time inputs (supporting English and German) to clean ISO 8601 strings.

## Resolution Table

Reference Clock (NOW): `2026-06-24T12:00:00` (Wednesday)

| # | Phrase | Resolved ISO 8601 | Ambiguity & Deciding Rule |
|---|--------|-------------------|---------------------------|
| 1 | `in 30 minutes` | `2026-06-24T12:30:00` | None (Unambiguous) |
| 2 | `this evening` | `2026-06-24T18:00:00` | Ambiguity: "evening" is vague. Decided: `18:00:00` (evening-default). |
| 3 | `next week` | `2026-07-01T18:00:00` | Ambiguity: "next week" does not specify day/time. Decided: `same-day-next-week` and `evening-default`. |
| 4 | `on Friday` | `2026-06-26T12:00:00` | Ambiguity: "Friday" does not specify time. Decided: `same-time-default`. |
| 5 | `at 6` | `2026-06-24T18:00:00` | Ambiguity: "6" could be AM or PM. Decided: `18:00:00` (evening-default). |
| 6 | `naechsten Dienstag um 6` | `2026-06-30T18:00:00` | Ambiguity: "next tuesday" current or next week. Decided: `strictly-future`. Ambiguity: "6" could be AM/PM. Decided: PM (evening-default). |
| 7 | `heute Abend um 8` | `2026-06-24T20:00:00` | Ambiguity: "8" could be AM/PM. Decided: PM (evening-default). |
| 8 | `tomorrow at 5pm` | `2026-06-25T17:00:00` | None (Unambiguous) |
| 9 | `in 2 hours` | `2026-06-24T14:00:00` | None (Unambiguous) |
| 10 | `tomorrow` | `2026-06-25T18:00:00` | Ambiguity: No time specified. Decided: `18:00:00` (evening-default). |

## Part A: Date-Time Resolver Rules

1. **Deterministic Clock**: Never call `datetime.now()` inside the resolver. The reference datetime `now` is passed in explicitly. Kjo garanton determinizëm absolut (i njëjti input gjithmonë prodhon të njëjtin output).
2. **Evening Default**: When a naked hour (e.g. "at 6" or "um 6") is provided, or a vague relative time like "this evening" or just "tomorrow" without time, the resolver defaults to `18:00:00` (6 PM) for single-digit hours <= 11 or time defaults, because users rarely schedule tasks for early morning unless specified.
3. **Strictly Future Weekday**: Resolving weekday references (e.g. "next Tuesday" or "naechsten Dienstag") evaluates to the closest future occurrence of that weekday (e.g. Wednesday -> next Tuesday = +6 days).
4. **German Language Support**: German phrases are cleaned and mapped to their English logical counterparts (e.g., `heute` -> `today`, `morgen` -> `tomorrow`, `naechsten Dienstag` -> `next tuesday`, `um 6` -> `at 6`) prior to processing.

> [!NOTE]
> The German output-only rule for translating Eszett `ß -> ss` is handled at the UI/output boundary and is never applied during parsing to avoid corrupting raw string patterns.

## Worst Ambiguity Resolution Note

The worst ambiguity encountered is resolving naked hours like "at 6" or "um 6" without an AM/PM designation. A human or system cannot determine if this refers to early morning (06:00) or evening (18:00). We resolved this by applying the **evening-default** rule (assuming PM/18:00 for any single-digit hour <= 11), aligning with standard scheduling habits.

## How to Run

```bash
python "Day 2/main.py"
```
