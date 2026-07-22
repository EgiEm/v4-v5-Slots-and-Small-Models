"""
Deterministic Date-Time Resolver.
Normalizes relative date-time phrases (English & German) to ISO 8601 strings.
Tracks and surfaces any ambiguities.
"""

import datetime
import re
from typing import Tuple, List

# Note: The ß -> ss rule is output-only and is never applied to parse input.

def resolve_datetime(phrase: str, now: datetime.datetime) -> Tuple[str, List[str]]:
    """
    Resolves a relative date-time phrase into a clean ISO 8601 string.
    Supports English and German phrases and surfaces ambiguities.
    
    :param phrase: The input relative datetime string (e.g. "tomorrow at 5pm")
    :param now: The reference clock datetime object
    :return: A tuple of (resolved_iso_string, list_of_ambiguities)
    """
    phrase_clean = phrase.lower().strip()
    
    # German to English mapping for easy parsing
    german_mappings = [
        (r'\bheute\b', 'today'),
        (r'\bmorgen\b', 'tomorrow'),
        (r'\bnaechste woche\b', 'next week'),
        (r'\bnaechsten\b', 'next'),
        (r'\bam\b', 'on'),
        (r'\bum\b', 'at'),
        (r'\babend\b', 'evening'),
        (r'\bsekunden\b', 'seconds'),
        (r'\bminuten\b', 'minutes'),
        (r'\bstunden\b', 'hours'),
        (r'\bdienstag\b', 'tuesday'),
        (r'\bfreitag\b', 'friday'),
    ]
    
    for de_pat, en_sub in german_mappings:
        phrase_clean = re.sub(de_pat, en_sub, phrase_clean)
        
    ambiguities = []
    
    target_date = None
    target_time = None
    
    # 1. Parse durations like "in 30 minutes", "in 2 hours"
    duration_match = re.search(r'\bin\s+(\d+)\s*(minute|hour|day|second|sec|min|hr)s?\b', phrase_clean)
    if duration_match:
        amount = int(duration_match.group(1))
        unit = duration_match.group(2)
        if unit.startswith(('min', 'minute')):
            delta = datetime.timedelta(minutes=amount)
        elif unit.startswith(('hr', 'hour')):
            delta = datetime.timedelta(hours=amount)
        elif unit.startswith(('sec', 'second')):
            delta = datetime.timedelta(seconds=amount)
        else:
            delta = datetime.timedelta(days=amount)
            
        resolved_dt = now + delta
        return resolved_dt.replace(microsecond=0).isoformat(), ambiguities

    # 2. Parse relative days: "today", "tomorrow", "next week"
    if 'tomorrow' in phrase_clean:
        target_date = now.date() + datetime.timedelta(days=1)
    elif 'next week' in phrase_clean:
        target_date = now.date() + datetime.timedelta(days=7)
        ambiguities.append("Ambiguity: 'next week' doesn't specify a day. Decided: Same day next week (same-day-next-week).")
    elif 'today' in phrase_clean:
        target_date = now.date()
        
    # 3. Parse weekday references: "on friday", "next tuesday"
    weekday_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    for day_name, day_num in weekday_map.items():
        if f'on {day_name}' in phrase_clean or f'next {day_name}' in phrase_clean or day_name in phrase_clean:
            current_wkday = now.weekday()
            offset = day_num - current_wkday
            if offset <= 0:
                offset += 7
            target_date = now.date() + datetime.timedelta(days=offset)
            if 'next' in phrase_clean:
                ambiguities.append(f"Ambiguity: 'next {day_name}' could mean current week or next week. Decided: strictly-future occurrence.")
            break

    # Default to today if no date reference found
    if target_date is None:
        target_date = now.date()
        
    # 4. Parse time references: "at 5pm", "at 6", "this evening"
    time_match = re.search(r'\bat\s+(\d+)(?::(\d+))?\s*(am|pm)?\b', phrase_clean)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3)
        
        if ampm:
            if ampm == 'pm' and hour < 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
        else:
            # Naked hour ambiguity
            if hour <= 11:
                ambiguities.append(f"Ambiguity: '{hour}' has no AM/PM specified. Decided: {hour + 12} (PM) via evening-default.")
                hour += 12
            else:
                ambiguities.append(f"Ambiguity: '{hour}' has no AM/PM specified. Decided: {hour} (24h default).")
        target_time = datetime.time(hour=hour, minute=minute)
    elif 'evening' in phrase_clean:
        ambiguities.append("Ambiguity: 'evening' is vague. Decided: 18:00:00 (evening-default).")
        target_time = datetime.time(hour=18, minute=0)
        
    # 5. Default time if no time reference found
    if target_time is None:
        if 'tomorrow' in phrase_clean or 'next week' in phrase_clean:
            ambiguities.append("Ambiguity: No time specified. Decided: 18:00:00 (evening-default).")
            target_time = datetime.time(hour=18, minute=0)
        else:
            ambiguities.append("Ambiguity: No time specified. Decided: Current clock time (same-time-default).")
            target_time = now.time().replace(microsecond=0)
            
    resolved_dt = datetime.datetime.combine(target_date, target_time)
    return resolved_dt.isoformat(), ambiguities
