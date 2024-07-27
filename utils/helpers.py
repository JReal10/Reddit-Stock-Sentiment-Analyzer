# utils/helpers.py

import re
from datetime import datetime

def clean_text(text):
    """Remove special characters and extra whitespace from text."""
    return re.sub(r'[^\w\s]', '', text).strip()

def convert_unix_time(unix_time):
    """Convert Unix timestamp to human-readable date."""
    return datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text, max_length=100):
    """Truncate text to a specified length."""
    return text[:max_length] + '...' if len(text) > max_length else text

def safe_divide(numerator, denominator):
    """Perform division, returning 0 if denominator is 0."""
    return numerator / denominator if denominator != 0 else 0

def format_number(number):
    """Format large numbers with K, M, B suffixes."""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return str(number)

# You might also include more complex utilities here, like:
# - Custom exceptions
# - Decorators
# - Data validation functions
# - File handling utilities