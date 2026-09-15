# Data Discrepancies and Historical Restatements

This document records inconsistencies found across the official Seattle Central College S&A budget source documents.

Values are not automatically overwritten or corrected. Differences are preserved and investigated before selecting values for analysis.

---

## 1. FY 2023–24 Total Allocation

The FY 2023–24 allocation is reported differently across the source documents.

| Source document | Reported FY 2023–24 allocation |
|---|---:|
| 2023–24 S&A Fee Memo | $1,500,000.00 |
| 2024–25 S&A Fee Memo | $1,513,171.18 |
| 2025–26 S&A Budget Summary | $1,513,171.18 |

### Difference

Later documents report an additional:

**$13,171.18**

compared with the original FY 2023–24 memo.

### Current treatment

The original FY 2023–24 value will remain preserved in the raw dataset.

The later value of **$1,513,171.18** appears consistently in two subsequent official documents and may represent a later adjustment or restatement.

The reason for the difference has not yet been confirmed.

Until supporting documentation is found, the dashboard should clearly identify this as a historical restatement rather than silently replacing the original figure.

---

## 2. FY 2024–25 Allocation

The FY 2024–25 total allocation is consistent across the two documents that report it.

| Source document | Reported FY 2024–25 allocation |
|---|---:|
| 2024–25 S&A Fee Memo | $1,733,008.51 |
| 2025–26 S&A Budget Summary | $1,733,008.51 |

**Status:** Confirmed across sources.

---

## 3. FY 2024–25 Request Interpretation

FY 2024–25 was part of a biennial budget cycle.

The Request column represents adjustment requests rather than necessarily representing each program's entire annual funding requirement.

Therefore:

- `$0.00` request does not automatically mean a program requested no funding.
- Programs could retain an existing allocation without requesting an adjustment.
- FY 2024–25 request values should not be compared directly with full-budget request years without explanation.

The dashboard should display a note or tooltip explaining this difference.

---

## 4. Merged Programs in FY 2025–26

The FY 2025–26 budget summary explicitly identifies some programs as combined into SSP, including:

- Child Assist Program
- Student Resource Support

Values such as `--` should be treated as non-numeric source values rather than automatically converted to zero during raw-data preservation.

Program mergers will be handled through a separate program crosswalk during data processing.