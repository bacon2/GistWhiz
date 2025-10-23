# Basic and extended SI prefixes for scaling numeric units
UNIT_PREFIXES = {
    # --- Standard SI prefixes ---
    'y': 1e-24,   # yocto
    'z': 1e-21,   # zepto
    'a': 1e-18,   # atto
    'f': 1e-15,   # femto
    'p': 1e-12,   # pico
    'n': 1e-9,    # nano
    'μ': 1e-6,    # micro (Greek mu)
    'u': 1e-6,    # ASCII micro
    'm': 1e-3,    # milli
    'c': 1e-2,    # centi
    'd': 1e-1,    # deci
    'da': 1e1,    # deka
    'h': 1e2,     # hecto
    'k': 1e3,     # kilo
    'M': 1e6,     # mega
    'G': 1e9,     # giga
    'T': 1e12,    # tera
    'P': 1e15,    # peta
    'E': 1e18,    # exa
    'Z': 1e21,    # zetta
    'Y': 1e24,    # yotta

    # --- Long-form text aliases (non-SI but human-friendly) ---
    'hundred': 1e2,
    'thousand': 1e3,
    'million': 1e6,
    'billion': 1e9,
    'trillion': 1e12,
    'quadrillion': 1e15,
    'quintillion': 1e18,

    # --- Binary prefixes (for data) ---
    'Ki': 1024,                  # kibi
    'Mi': 1024**2,               # mebi
    'Gi': 1024**3,               # gibi
    'Ti': 1024**4,               # tebi
    'Pi': 1024**5,               # pebi
    'Ei': 1024**6,               # exbi

    # --- Deprecated or rare but seen in real data ---
    'mc': 1e-6,   # alternate for micro (esp. in med/US)
    'meg': 1e6,   # spoken 'meg' (informal)
    'kilo': 1e3,
    'mega': 1e6,
    'giga': 1e9,
    'tera': 1e12,
    'micro': 1e-6,
    'nano': 1e-9,
    'milli': 1e-3,
    'centi': 1e-2,
}
