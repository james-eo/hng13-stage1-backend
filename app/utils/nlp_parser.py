import re


def parse_natural_language(query: str) -> dict:
    """Parse natural language query into structured filters"""
    query_lower = query.lower().strip()
    filters = {}

    # Palindrome detection
    if any(word in query_lower for word in ["palindrom", "palindromic"]):
        filters["is_palindrome"] = True

    # Word count detection
    if "single word" in query_lower or "one word" in query_lower:
        filters["word_count"] = 1
    elif "two word" in query_lower:
        filters["word_count"] = 2

    # Length detection
    length_match = re.search(r"longer than (\d+)", query_lower)
    if length_match:
        filters["min_length"] = int(length_match.group(1)) + 1

    # Character detection
    letter_match = re.search(
        r"contain(?:s|ing)?\s+(?:the\s+)?(?:letter\s+)?([a-z])",
        query_lower
    )
    if letter_match:
        filters["contains_character"] = letter_match.group(1)

    # Special case: "first vowel"
    if "first vowel" in query_lower:
        filters["contains_character"] = "a"

    return filters
