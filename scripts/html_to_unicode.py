"""Convert HTML tags to Unicode equivalents in publication titles."""

import re

SUPERSCRIPT_MAP = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
    'n': 'ⁿ', 'i': 'ⁱ'
}

SUBSCRIPT_MAP = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
    'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ', 'h': 'ₕ',
    'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'p': 'ₚ',
    's': 'ₛ', 't': 'ₜ'
}

def convert_html_to_unicode(text: str) -> str:
    """
    Convert HTML tags to Unicode equivalents.

    Handles:
    - <SUP>content</SUP> → superscript characters
    - <sub>content</sub> → subscript characters
    - <i>content</i> → preserve as-is (no Unicode italic)

    Returns converted string, logs warnings for unmapped characters.
    """
    if not text:
        return text

    def convert_superscript(match):
        content = match.group(1)
        result = ''.join(SUPERSCRIPT_MAP.get(c, c) for c in content)
        unconverted = [c for c in content if c not in SUPERSCRIPT_MAP and not c.isspace()]
        if unconverted:
            print(f"⚠️  Warning: No superscript mapping for: {unconverted} in '{content}'")
        return result

    def convert_subscript(match):
        content = match.group(1)
        result = ''.join(SUBSCRIPT_MAP.get(c, c) for c in content)
        unconverted = [c for c in content if c not in SUBSCRIPT_MAP and not c.isspace()]
        if unconverted:
            print(f"⚠️  Warning: No subscript mapping for: {unconverted} in '{content}'")
        return result

    # Convert <SUP>...</SUP> (case insensitive)
    text = re.sub(r'<SUP>([^<]+)</SUP>', convert_superscript, text, flags=re.IGNORECASE)

    # Convert <sub>...</sub> (case insensitive)
    text = re.sub(r'<sub>([^<]+)</sub>', convert_subscript, text, flags=re.IGNORECASE)

    # Remove <i>...</i> tags but keep content
    text = re.sub(r'</?i>', '', text, flags=re.IGNORECASE)

    return text
