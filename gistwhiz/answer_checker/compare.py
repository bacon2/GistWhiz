import re
from .units_prefixes import UNIT_PREFIXES
from .units_bases import UNIT_BASES
FILLER_WORDS = {"the", "of", "a", "an"}

def remove_parentheticals(s: str) -> str:
    return re.sub(r'\([^)]*\)', '', s)

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
    return tokens_match(a.split(), b.split())

def tokens_match(tokens_a, tokens_b):
    matches = 0
    for word_a in tokens_a:
        if any(simple_fuzzy_match(word_a, word_b) for word_b in tokens_b):
            matches += 1
    # Require at least 95% of the longer list to match
    return matches >= max(len(tokens_a), len(tokens_b)) * 0.95


def strip_fillers(s: str) -> str:
    return ' '.join(w for w in s.split() if w not in FILLER_WORDS)

def normalize_text(s: str) -> str:
    s = remove_parentheticals(s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9.\s-]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = strip_fillers(s)
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
    # Exact match
    if a == b:
        return True

    # If one of them is empty
    if not a or not b:
        return False

    # Quick reject if lengths are too different
    if abs(len(a) - len(b)) > 2:
        return False

    # For very short strings (1–2 chars), require exact match
    if len(a) < 3 or len(b) < 3:
        return False

    # Count mismatches up to the shorter length
    mismatches = sum(c1 != c2 for c1, c2 in zip(a, b))
    ratio = mismatches / max(len(a), len(b))

    # Allow up to 20% difference
    return ratio <= 0.2

if __name__ == "__main__":
    # print(answers_match("5 grams", "5 g"))
    # print(answers_match("5g", "5 grams"))
    # print(answers_match("stomach", "skomach"))
    print(answers_match("2 mg intranasal, 1 mg intramuscular", "2 mg intranasal, 1 mg intramuscular"))