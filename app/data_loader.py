from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CANONICAL_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sa_budget_canonical.csv"
)


DASHBOARD_YEARS = [
    "2023-24",
    "2024-25",
    "2025-26",
]


@st.cache_data
def load_budget_data():
    df = pd.read_csv(CANONICAL_PATH)

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    # Main dashboard scope:
    # three fiscal years from 2023-24 through 2025-26.
    df = df[
        df["fiscal_year"].isin(
            DASHBOARD_YEARS
        )
    ].copy()

    return df