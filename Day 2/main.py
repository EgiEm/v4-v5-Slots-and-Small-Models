"""
Day 2 Challenge Runner: Deterministic Date-Time Resolver.
Runs 10 English and German relative date-time phrases against a fixed NOW clock.
"""

import datetime
from date_resolver import resolve_datetime

def main():
    # Fixed NOW reference clock (Wednesday, June 24, 2026 at 12:00:00 PM)
    now = datetime.datetime(2026, 6, 24, 12, 0, 0)
    
    # 10 test phrases (including English and German relative/ambiguous forms)
    test_phrases = [
        "in 30 minutes",
        "this evening",
        "next week",
        "on Friday",
        "at 6",
        "naechsten Dienstag um 6",  # = next Tuesday at 6
        "heute Abend um 8",         # = tonight at 8
        "tomorrow at 5pm",
        "in 2 hours",
        "tomorrow"
    ]
    
    print("=" * 105)
    print(f" Reference Clock (NOW) : {now.isoformat()}")
    print("=" * 105)
    print(f"{'#':<3} | {'Phrase':<28} | {'Resolved ISO 8601':<20} | {'Ambiguity & Deciding Rule'}")
    print("-" * 105)
    
    for idx, phrase in enumerate(test_phrases, 1):
        iso_str, ambiguities = resolve_datetime(phrase, now)
        ambiguity_desc = ambiguities[0] if ambiguities else "None (Unambiguous)"
        print(f"{idx:<3} | {phrase:<28} | {iso_str:<20} | {ambiguity_desc}")
        # Print subsequent ambiguities if any exist
        for extra in ambiguities[1:]:
            print(f"{'':<3} | {'':<28} | {'':<20} | {extra}")
            
    print("=" * 105)
    print("\n[WORST AMBIGUITY NOTE]")
    print("The worst ambiguity encountered is resolving naked hours like 'at 6' or 'um 6'.")
    print("Without an AM/PM indicator, this is mathematically ambiguous (06:00 vs 18:00).")
    print("We resolved it using the 'evening-default' rule: hours <= 11 default to PM (18:00) as users")
    print("almost always schedule tasks for daytime or evening hours rather than early morning.")

if __name__ == "__main__":
    main()
