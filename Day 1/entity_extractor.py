"""
Entity Extractor for Intent Slot Filling.
Extracts contact names, duration in seconds, monetary amounts, and task text.
Supports both English and German intent patterns.
"""

import re
from typing import Dict, Any, Optional


def parse_duration_seconds(text: str) -> Optional[int]:
    """Extracts duration from text and converts to seconds integer."""
    pattern = r'(\d+)\s*(seconds?|secs?|sekunden?|minutes?|mins?|minuten?|hours?|hrs?|stunden?|std)'
    match = re.search(pattern, text, re.IGNORECASE)
    if not match:
        return None
    
    amount = int(match.group(1))
    unit = match.group(2).lower()

    if unit.startswith(('second', 'sec', 'sekunde')):
        return amount
    elif unit.startswith(('minute', 'min')):
        return amount * 60
    elif unit.startswith(('hour', 'hr', 'stunde', 'std')):
        return amount * 3600
    
    return None


def extract_contact(text: str) -> Optional[str]:
    """Extracts contact names from calling intents in English or German."""
    # German pattern: "Ruf Mama an", "Ruf Alex an", "Ruf Sarah"
    de_match = re.search(r'\bruf\s+([a-zA-Z\s]+?)(?:\s+an)?$', text, re.IGNORECASE)
    if de_match:
        contact = de_match.group(1).strip()
        if contact:
            return contact

    # English pattern: "call Sarah on WhatsApp", "phone Alex regarding...", "call Mom"
    en_match = re.search(r'\b(?:call|phone|ring|dial|contact)\s+([A-Z][a-z]+|[a-zA-Z]+)', text, re.IGNORECASE)
    if en_match:
        contact = en_match.group(1).strip()
        # Exclude common non-contact words
        if contact.lower() not in ['me', 'a', 'the', 'up', 'back', 'on']:
            return contact
            
    return None


def extract_amount(text: str) -> Optional[str]:
    """Extracts currency values or monetary amounts."""
    # Matches $50, €20, £10, 50 USD, 100 EUR, 50 dollars, etc.
    pattern = r'(\$\d+(?:\.\d{2})?|€\d+(?:\.\d{2})?|£\d+(?:\.\d{2})?|\d+\s*(?:dollars?|euros?|usd|eur|gbp|chf))'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def extract_task_text(text: str) -> Optional[str]:
    """Extracts crude task description from task creation prompts."""
    # English patterns
    en_patterns = [
        r"(?:remind me to|don't forget to|remember to|add task|todo:?)\s+(.+)",
    ]
    for pat in en_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
    # German patterns: "erinnere mich daran...", "vergiss nicht..."
    de_patterns = [
        r"(?:erinnere mich daran|vergiss nicht|aufgabe:?)\s+(.+)",
    ]
    for pat in de_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
    return None


def extract_entities(text: str, intent: str) -> Dict[str, Any]:
    """
    Main entity extraction pipeline filling typed slot dictionaries based on predicted intent.
    """
    slots: Dict[str, Any] = {}

    if intent == "create_task":
        task_text = extract_task_text(text)
        slots["text"] = task_text if task_text else text
        
        # Check optional due date / time indicator
        if "tomorrow" in text.lower():
            slots["due"] = "tomorrow"
        elif "today" in text.lower():
            slots["due"] = "today"

    elif intent == "place_call":
        contact = extract_contact(text)
        slots["contact"] = contact
        
        # Optional app extraction
        if "whatsapp" in text.lower():
            slots["app"] = "WhatsApp"
        elif "telegram" in text.lower():
            slots["app"] = "Telegram"

    elif intent == "set_timer":
        duration = parse_duration_seconds(text)
        slots["duration_seconds"] = duration

    elif intent == "save_memory":
        # Extract crude note text
        note_match = re.search(r'(?:save note:?|remember that|note:?)\s+(.+)', text, re.IGNORECASE)
        slots["note"] = note_match.group(1).strip() if note_match else text
        
        # Extract optional amount if present
        amount = extract_amount(text)
        if amount:
            slots["amount"] = amount

    elif intent == "answer_question":
        slots["query"] = text

    elif intent == "out_of_scope":
        slots["raw_text"] = text

    return slots
