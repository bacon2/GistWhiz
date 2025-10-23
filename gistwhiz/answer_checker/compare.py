import re
from .units_prefixes import UNIT_PREFIXES
from .units_bases import UNIT_BASES


def answers_match(a: str, b: str) -> bool:
    a, b = normalize_text(a), normalize_text(b)
    a, b = word_to_number(a), word_to_number(b)
    a, b = replace_synonyms(a), replace_synonyms(b)

    # Direct equality
    if a == b:
        return True

    # Try quantity-unit comparison
    qa, qb = parse_quantity(a), parse_quantity(b)
    if qa and qb:
        (va, ua), (vb, ub) = qa, qb
        if ua == ub and abs(va - vb) < 1e-6:
            return True

    # Token-based fuzzy match
    tokens_a, tokens_b = a.split(), b.split()
    for word_a in tokens_a:
        if any(simple_fuzzy_match(word_a, word_b) for word_b in tokens_b):
            continue
        # allow filler words like “the”, “of”, etc.
        if word_a in {"the", "of", "a", "an"}:
            continue
        return False
    return True

def normalize_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9.\s-]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_quantity(s: str):
    match = re.match(r'^([0-9.]+)\s*([a-z]+)?$', s)
    if not match:
        return None
    value, unit = match.groups()
    value = float(value)
    if unit:
        prefix, base = unit[0], unit[1:]
        if base in UNIT_BASES:
            base_unit = UNIT_BASES[base]
            scale = UNIT_PREFIXES.get(prefix, 1)
            return value * scale, base_unit
        elif unit in UNIT_BASES:
            return value, UNIT_BASES[unit]
    return value, None
WORD_NUMS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def word_to_number(s: str) -> str:
    words = s.split()
    return ' '.join(str(WORD_NUMS.get(w, w)) for w in words)
SYNONYMS = {
    "heart": "cardiac",
    "photo": "picture",
    "picture": "photo",  # two-way
}

def replace_synonyms(s: str) -> str:
    words = s.split()
    return ' '.join(SYNONYMS.get(w, w) for w in words)

def simple_fuzzy_match(a: str, b: str) -> bool:
    if a == b:
        return True
    if abs(len(a) - len(b)) > 2:
        return False
    mismatches = sum(c1 != c2 for c1, c2 in zip(a, b))
    return mismatches / max(len(a), 1) <= 0.2  # ≤20% difference tolerated

if __name__ == "__main__":
    # print(answers_match("5 grams", "5 g"))
    # print(answers_match("5g", "5 grams"))
    print(answers_match("stomach", "skomach"))