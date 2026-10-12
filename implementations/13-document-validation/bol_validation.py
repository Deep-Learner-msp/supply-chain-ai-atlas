"""
Bill of lading extraction: simple validation rules catch most extraction errors.

We generate 3,000 ground-truth ocean bills of lading, then run them through
a simulated extractor (think OCR plus a language model) that makes the
mistakes real extractors make:
  weight digits  : two adjacent digits swapped in the gross weight
  pieces digit   : a digit dropped from the piece count
  date day/month : 03/04 read as 4 March instead of 3 April
  container      : one character misread, or the check digit cut off
  SCAC typo      : one letter of the carrier code wrong

Then four cheap, deterministic rules check every extracted document:
  1. container number: format AAAU1234567 and ISO 6346 check digit
  2. SCAC is on the known carrier list
  3. weight per piece is plausible (3 to 30 kg) and weight <= 28,000 kg
  4. dates in order (pickup <= on board <= ETA) with sane gaps

A document that passes every rule goes straight through; one that fails goes
to a person. All documents are synthetic and illustrative.

Run: python bol_validation.py
"""

import datetime as dt
import random
import re

random.seed(13)
N_DOCS = 3000
SCACS = ["MAEU", "MSCU", "CMDU", "HLCU", "ONEY", "EGLV", "COSU", "OOLU", "YMLU", "ZIMU"]
ERROR_RATES = {"weight digits": 0.04, "pieces digit": 0.02, "date day/month": 0.06,
               "container": 0.04, "SCAC typo": 0.03}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def letter_values():
    # ISO 6346: A=10, B=12, ... skipping 11, 22 and 33 (multiples of 11)
    values, v = {}, 10
    for ch in LETTERS:
        if v % 11 == 0:
            v += 1
        values[ch] = v
        v += 1
    return values


VALUES = letter_values()


def check_digit(first10):
    total = sum((VALUES[c] if c.isalpha() else int(c)) * 2 ** i for i, c in enumerate(first10))
    return total % 11 % 10


def container_ok(code):
    return bool(re.fullmatch(r"[A-Z]{3}[UJZ]\d{7}", code)) and check_digit(code[:10]) == int(code[10])


def make_bol():
    owner = "".join(random.choices(LETTERS, k=3)) + "U"
    body = owner + f"{random.randint(0, 999999):06d}"
    pieces = random.randint(40, 1200)
    heavy = random.random() < 0.02  # real but unusual cargo: machinery parts
    per_piece = random.uniform(30, 45) if heavy else random.uniform(4, 22)
    pickup = dt.date(2026, 1, 1) + dt.timedelta(days=random.randint(0, 300))
    onboard = pickup + dt.timedelta(days=random.randint(1, 7))
    return {"scac": random.choice(SCACS), "container": body + str(check_digit(body)), "pieces": pieces,
            "weight": min(round(pieces * per_piece), 27500), "pickup": pickup, "onboard": onboard,
            "eta": onboard + dt.timedelta(days=random.randint(12, 38))}


def extract(bol):
    """Simulated extractor: returns the extracted record and the error types it introduced."""
    out, errors = dict(bol), []
    if random.random() < ERROR_RATES["weight digits"]:
        s = str(bol["weight"])
        i = random.randrange(len(s) - 1)
        if s[i] != s[i + 1]:
            out["weight"] = int(s[:i] + s[i + 1] + s[i] + s[i + 2:])
            errors.append("weight digits")
    if random.random() < ERROR_RATES["pieces digit"]:
        s = str(bol["pieces"])
        i = random.randrange(len(s))
        out["pieces"] = int(s[:i] + s[i + 1:])
        errors.append("pieces digit")
    if random.random() < ERROR_RATES["date day/month"]:
        field = random.choice(["pickup", "onboard", "eta"])
        d = bol[field]
        if d.day <= 12 and d.day != d.month:
            out[field] = d.replace(month=d.day, day=d.month)
            errors.append("date day/month")
    if random.random() < ERROR_RATES["container"]:
        c = bol["container"]
        if random.random() < 0.3:
            out["container"] = c[:10]  # check digit cut off
        else:
            i = random.randrange(11)
            pool = LETTERS if i < 4 else "0123456789"
            out["container"] = c[:i] + random.choice(pool.replace(c[i], "")) + c[i + 1:]
        errors.append("container")
    if random.random() < ERROR_RATES["SCAC typo"]:
        s = bol["scac"]
        i = random.randrange(4)
        out["scac"] = s[:i] + random.choice(LETTERS.replace(s[i], "")) + s[i + 1:]
        if out["scac"] != s:
            errors.append("SCAC typo")
    return out, errors


def validate(doc):
    fails = []
    if not container_ok(doc["container"]):
        fails.append("container check")
    if doc["scac"] not in SCACS:
        fails.append("unknown SCAC")
    if doc["pieces"] == 0 or not 3 <= doc["weight"] / doc["pieces"] <= 30 or doc["weight"] > 28000:
        fails.append("weight vs pieces")
    gap_board, gap_sea = (doc["onboard"] - doc["pickup"]).days, (doc["eta"] - doc["onboard"]).days
    if not (0 <= gap_board <= 14 and 5 <= gap_sea <= 60):
        fails.append("date order")
    return fails


def main():
    assert check_digit("CSQU305438") == 3  # worked example from ISO 6346
    docs = [extract(make_bol()) for _ in range(N_DOCS)]
    per_type = {k: [0, 0] for k in ERROR_RATES}
    bad = caught = passed = passed_bad = false_alarm = 0
    for doc, errors in docs:
        flagged = bool(validate(doc))
        bad += bool(errors)
        caught += bool(errors) and flagged
        passed += not flagged
        passed_bad += bool(errors) and not flagged
        false_alarm += (not errors) and flagged
        for e in errors:
            per_type[e][0] += 1
            per_type[e][1] += flagged
    print(f"{N_DOCS:,} synthetic bills of lading, {bad} ({bad / N_DOCS:.1%}) with at least one extraction error\n")
    print(f"{'Error type':<16} {'Injected':>8} {'Caught':>8}")
    print("-" * 34)
    for name, (n, c) in per_type.items():
        print(f"{name:<16} {n:>8} {c / n:>8.0%}")
    print(f"\nDocuments with an error that the rules caught : {caught / bad:.1%}")
    print(f"Clean documents flagged anyway (false alarms) : {false_alarm} ({false_alarm / (N_DOCS - bad):.1%})")
    print(f"Straight-through rate (pass every rule)       : {passed / N_DOCS:.1%}")
    print(f"Errors left in straight-through documents     : {passed_bad / passed:.1%} "
          f"(vs {bad / N_DOCS:.1%} with no rules)")
    print("Check digits, code lists and date logic catch almost every error they cover; swapped weight "
          "digits that still look plausible need a second source, like the booking or packing list.")


if __name__ == "__main__":
    main()
