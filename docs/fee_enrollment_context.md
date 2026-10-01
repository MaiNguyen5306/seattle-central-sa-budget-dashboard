# S&A Fee and Enrollment Context

## Purpose

This research adds student-level context to the Seattle Central S&A Budget Explorer.

The main budget data shows how Services and Activities (S&A) funds were allocated. This supporting analysis helps answer two additional questions:

1. How much do full-time students pay in S&A fees?
2. How many students does Seattle Central serve each academic year?

The current dashboard period covers academic years 2023–24 through 2025–26. Data for 2026–27 is retained where available for future updates.

---

## S&A Fee Data

S&A fees are included within Seattle Colleges tuition rather than listed as a separate additional student fee.

The analysis currently focuses on full-time credit loads from 12 through 21 credits.

### Full-Time Quarterly S&A Fees

| Academic Year | 12 Credits | 15 Credits | Maximum Fee | Maximum Reached At |
|---|---:|---:|---:|---:|
| 2023–24 | $141.82 | $163.90 | $185.98 | 18 credits |
| 2024–25 | $146.38 | $169.15 | $191.92 | 18 credits |
| 2025–26 | $151.40 | $174.95 | $198.50 | 18 credits |
| 2026–27 | $156.20 | $180.50 | $204.80 | 18 credits |

The fee reaches its maximum at 18 credits and remains capped for 19–21 credits.

A 15-credit load is retained as a useful reference point, but it should not be interpreted as the amount paid by every full-time student.

---

## Enrollment Context

The enrollment measure used in this project is **annual student headcount**.

Headcount represents individual students served during the academic year. FTE is not currently used in the project because the purpose of this analysis is to communicate the number of students rather than institutional enrollment workload.

### Annual Headcount

| Academic Year | Students | Year-over-Year Change |
|---|---:|---:|
| 2023–24 | 12,088 | — |
| 2024–25 | 12,378 | +2.40% |
| 2025–26 | 11,672 | -5.70% |

Across the current three-year dashboard period, annual headcount changed from 12,088 students in 2023–24 to 11,672 in 2025–26.

This is a net change of:

- 416 fewer students
- approximately -3.4%

The SBCTC enrollment dashboard labels the institution as **Seattle Central/SVI**. That source terminology is preserved in the underlying data.

---

## Interpretation

S&A budget totals and student enrollment can be viewed together for context, but they measure different things.

For example, enrollment declined across the full three-year period while total S&A allocations increased. This does not by itself explain why funding increased or indicate whether funding per student increased in practice.

Additional analysis would be required to evaluate factors such as:

- actual S&A fee revenue collected;
- student credit loads;
- number of quarters attended;
- fee waivers or exemptions;
- actual program expenditures;
- carryforward balances;
- enrollment composition; and
- institutional budgeting decisions.

---

## Important Limitation

Annual student headcount should **not** be multiplied by the maximum quarterly S&A fee to estimate annual S&A revenue.

Students may:

- take different numbers of credits;
- attend one, two, or three quarters;
- pay different S&A fee amounts based on credit load; or
- fall under different enrollment or fee circumstances.

Therefore, the headcount and fee datasets are currently used as descriptive context rather than as a revenue-estimation model.

---

## Data Files

### Manual Source Data

- `data/manual/sa_fee_rates.csv`
- `data/manual/enrollment_context.csv`

### Processed Data

- `data/processed/sa_fee_summary.csv`
- `data/processed/enrollment_summary.csv`

### Source Documents

Official tuition and fee schedules are stored in:

`data/raw/tuition_fees/`

Enrollment figures are documented from Seattle Colleges and the Washington State Board for Community and Technical Colleges (SBCTC).

---

## Analysis Notebook

The supporting validation and analysis are contained in:

`notebooks/04_fee_enrollment_context.ipynb`

The notebook validates:

- academic-year coverage;
- credit-level coverage;
- duplicate records;
- missing required fields;
- the 18-credit S&A fee cap;
- enrollment measure consistency;
- year-over-year enrollment changes; and
- the full-period enrollment change.