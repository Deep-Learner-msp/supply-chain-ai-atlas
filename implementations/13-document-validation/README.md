# 13: Bill of lading extraction, and how four cheap rules catch 80% of errors

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Deep-Learner-msp/supply-chain-ai-atlas/blob/main/notebooks/13-document-validation.ipynb)

3,000 synthetic ocean bills of lading go through a simulated extractor that makes realistic mistakes (swapped weight digits, a dropped piece-count digit, day/month swaps, misread container numbers, SCAC typos). Four deterministic rules then check each document. Synthetic, illustrative documents.

```bash
python bol_validation.py
```

| Error type | Injected | Caught by rules |
|---|---|---|
| Weight digits swapped | 110 | 28% |
| Piece-count digit dropped | 64 | 98% |
| Date day/month swapped | 65 | 100% |
| Container number misread | 112 | 98% |
| SCAC typo | 87 | 100% |

| Result | Value |
|---|---|
| Documents with at least one extraction error | 412 (13.7%) |
| Documents with an error that the rules caught | 80.1% |
| Clean documents flagged anyway (false alarms) | 36 (1.4%) |
| Straight-through rate (pass every rule) | 87.8% |
| Errors left in straight-through documents | 3.1% (vs 13.7% with no rules) |

The rules:

1. Container number format and [ISO 6346](https://en.wikipedia.org/wiki/ISO_6346) check digit (the script asserts the standard's worked example, CSQU305438 gives 3; compare with the [BIC calculator](https://www.bic-code.org/check-digit-calculator/)).
2. SCAC on a known carrier list.
3. Weight per piece between 3 and 30 kg, gross weight at most 28,000 kg.
4. Dates in order (pickup, on board, ETA) with sane gaps.

## What to notice

- A check digit is free accuracy. It catches 98% of misread container numbers; the misses are letter misreads whose values differ by a multiple of 11 (Y read as E, E read as O) and one digit error where the remainder 10 is written as check digit 0.
- Date logic catches every day/month swap here because a swap moves a date by weeks or months. On documents with short or loose date gaps, expect some to slip through.
- Swapped weight digits are the hard case: 1,284 kg read as 1,248 kg still looks plausible. Only a second source (booking, packing list, scale weight) catches those.
- The false alarms are real but unusual cargo (heavy machinery parts). Rules need an override path, not just a reject.
- Validate before you buy a better extractor: the rules cut errors in auto-accepted documents from 13.7% to 3.1%.
