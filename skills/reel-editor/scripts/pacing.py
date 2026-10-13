"""Pacing presets: how hard the edit trims. One place, so cut.py, tighten.py and the review page agree.
brand.json "pacing": "natural" (default) | "tight" | "fast". An explicit brand.json "speed" still wins."""

PRESETS = {
    # pauses longer than pause_min get shortened, leaving `air` seconds either side of the cut
    "natural": {"speed": 1.0, "pause_min": 0.6, "air": 0.15, "fillers": ["um", "uh", "umm", "uhm", "erm", "hmm", "mm"]},
    "tight":   {"speed": 1.1, "pause_min": 0.25, "air": 0.06, "fillers": ["um", "uh", "umm", "uhm", "erm", "er", "ah", "hmm", "mm"]},
    "fast":    {"speed": 1.15, "pause_min": 0.2, "air": 0.05, "fillers": ["um", "uh", "umm", "uhm", "erm", "er", "ah", "hmm", "mm"]},
}

def whisper_args(brand):
    """Model + language flags for `hyperframes transcribe`. English uses the small English-only model (fast);
    any other brand.json "language" (e.g. "ru") needs the multilingual large-v3 model, which the .en models cannot do."""
    lang = (brand.get("language") or "en").lower()
    if lang.startswith("en"): return ["--model", "small.en"]
    return ["--model", "large-v3", "--language", lang]

def pacing(brand):
    p = dict(PRESETS.get(brand.get("pacing", "natural"), PRESETS["natural"]))
    if brand.get("speed"): p["speed"] = float(brand["speed"])
    if brand.get("fillers") is not None: p["fillers"] = list(brand["fillers"])   # [] = keep every filler
    return p
