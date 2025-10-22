import hashlib
import collections
from datetime import datetime, timezone


def sha256_hash(value: str) -> str:
    """Generate SHA-256 hash of the given string."""
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def character_frequency_map(value: str) -> dict:
    """Generate a character frequency map for the given string."""
    freq = {}
    for char in value:
        freq[char] = freq.get(char, 0) + 1
    return freq


def analyze_string(value: str) -> dict:
    """Analyze the given string and return various attributes."""
    _id = sha256_hash(value)
    length = len(value)
    normalized_value = value.lower()
    # For palindrome check, remove spaces and non-alphanumeric characters
    cleaned_value = ''.join(
        char for char in normalized_value if char.isalnum()
    )
    is_palindrome = cleaned_value == cleaned_value[::-1]
    unique_characters = len(set(value))
    word_count = len(value.split())
    freq_map = character_frequency_map(value)
    created_at = datetime.now(timezone.utc).isoformat()
    properties = {
        'length': length,
        'is_palindrome': is_palindrome,
        'unique_characters': unique_characters,
        'word_count': word_count,
        'sha256_hash': _id,
        'character_frequency_map': freq_map
    }
    return {
        'id': _id,  # Changed from '_id' to 'id'
        'value': value,
        'properties': properties,
        'created_at': created_at
    }
